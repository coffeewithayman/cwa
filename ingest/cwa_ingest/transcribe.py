"""WhisperX on the GPU: transcribe -> align (word timestamps) -> diarize.

Models are loaded once per process and reused, so the watcher can process a
whole backlog without reloading ~5 GB of weights per talk.
"""

from __future__ import annotations

import gc
import json
from functools import lru_cache
from pathlib import Path

from . import config

DEVICE = config.DEVICE
COMPUTE = config.COMPUTE_TYPE


@lru_cache(maxsize=4)
def _asr(prompt: str, hotwords: str):
    import whisperx
    opts = {**config.WHISPER_ASR_OPTIONS, "initial_prompt": prompt or None, "hotwords": hotwords or None}
    return whisperx.load_model(config.WHISPER_MODEL, DEVICE, compute_type=COMPUTE,
                               language="en", asr_options=opts)


@lru_cache(maxsize=1)
def _aligner():
    import whisperx
    return whisperx.load_align_model(language_code="en", device=DEVICE)


@lru_cache(maxsize=1)
def _diarizer():
    from whisperx.diarize import DiarizationPipeline
    token = config.hf_token()
    if not token:
        raise RuntimeError(
            "HF_TOKEN missing: add it to ingest/.env and accept the model terms at "
            f"https://huggingface.co/{config.DIARIZATION_MODEL}")
    pipe = DiarizationPipeline(model_name=config.DIARIZATION_MODEL, token=token, device=DEVICE)
    pipe.model.segmentation_batch_size = config.DIARIZATION_BATCH
    pipe.model.embedding_batch_size = config.DIARIZATION_BATCH
    return pipe


class GPUBusy(RuntimeError):
    pass


def ensure_gpu() -> None:
    """Refuse to start when another process (e.g. llama-server) holds the VRAM."""
    if DEVICE != "cuda":
        return
    import torch
    free, total = torch.cuda.mem_get_info()
    if free / 2**30 < config.GPU_MIN_FREE_GB:
        raise GPUBusy(f"only {free / 2**30:.1f} of {total / 2**30:.0f} GB VRAM free")


def release() -> None:
    """Unload every model and hand the VRAM back (low-VRAM profile, between stages)."""
    _asr.cache_clear()
    _aligner.cache_clear()
    _diarizer.cache_clear()
    gc.collect()
    if DEVICE == "cuda":
        import torch
        torch.cuda.empty_cache()


def _align(segments: list[dict], model, meta, audio) -> dict:
    """Word-align in slices so VRAM stays flat however long the recording is.

    Segments are aligned independently, so slicing doesn't change the result.
    """
    import torch
    import whisperx
    out: dict = {"segments": [], "word_segments": []}
    step = config.ALIGN_SLICE
    for i in range(0, len(segments), step):
        part = whisperx.align(segments[i:i + step], model, meta, audio, DEVICE, return_char_alignments=False)
        out["segments"] += part["segments"]
        out["word_segments"] += part.get("word_segments", [])
        if DEVICE == "cuda":
            torch.cuda.empty_cache()
    return out


def vocab_prompt(terms: list[str]) -> tuple[str, str]:
    """Initial prompt + hotwords that bias Whisper toward Ayman's vocabulary."""
    if not terms:
        return "", ""
    joined = ", ".join(terms)
    return f"A talk on information security covering {joined}.", joined


def transcribe(workdir: Path, terms: list[str]) -> dict:
    import whisperx

    ensure_gpu()
    audio = whisperx.load_audio(str(workdir / "audio.wav"))
    prompt, hotwords = vocab_prompt(terms)
    result = _asr(prompt, hotwords).transcribe(audio, batch_size=config.WHISPER_BATCH_SIZE, language="en")
    if config.LOW_VRAM:
        release()

    model, meta = _aligner()
    result = _align(result["segments"], model, meta, audio)
    if config.LOW_VRAM:
        release()

    diarize_df = _diarizer()(audio)
    result = whisperx.assign_word_speakers(diarize_df, result)
    result["diarization"] = [
        {"start": float(r.start), "end": float(r.end), "speaker": r.speaker}
        for r in diarize_df.itertuples()
    ]
    (workdir / "whisper.json").write_text(json.dumps(result, indent=1))
    if config.LOW_VRAM:
        release()
    return result
