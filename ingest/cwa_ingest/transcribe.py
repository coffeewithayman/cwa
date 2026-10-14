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
COMPUTE = "float16" if DEVICE == "cuda" else "int8"


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
    return DiarizationPipeline(model_name=config.DIARIZATION_MODEL, token=token, device=DEVICE)


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

    model, meta = _aligner()
    result = whisperx.align(result["segments"], model, meta, audio, DEVICE, return_char_alignments=False)

    diarize_df = _diarizer()(audio)
    result = whisperx.assign_word_speakers(diarize_df, result)
    result["diarization"] = [
        {"start": float(r.start), "end": float(r.end), "speaker": r.speaker}
        for r in diarize_df.itertuples()
    ]
    (workdir / "whisper.json").write_text(json.dumps(result, indent=1))
    gc.collect()
    return result
