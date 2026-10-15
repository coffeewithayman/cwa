import static_ffmpeg

# Use the system ffmpeg if there is one, otherwise the bundled static build.
# Done at import so every entry point (whisperx, yt-dlp, ffprobe calls) sees it.
static_ffmpeg.add_paths(weak=True)
