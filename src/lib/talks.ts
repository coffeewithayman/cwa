export const FORMAT_LABELS: Record<string, string> = {
  talk: "Talk",
  webinar: "Webinar",
  interview: "Interview",
  "podcast-guest": "Podcast guest",
  panel: "Panel",
  cohost: "Co-host",
};

export function formatLabel(format: string | null): string {
  return format ? (FORMAT_LABELS[format] ?? format) : "—";
}

/** 3725 -> "1:02:05", 125 -> "2:05" */
export function clock(seconds: number): string {
  const s = Math.floor(seconds);
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  const ss = String(s % 60).padStart(2, "0");
  return h ? `${h}:${String(m).padStart(2, "0")}:${ss}` : `${m}:${ss}`;
}

/** 3725 -> "1h 2m", 125 -> "2m" */
export function humanDuration(seconds: number | null): string {
  if (!seconds) return "—";
  const m = Math.round(seconds / 60);
  return m >= 60 ? `${Math.floor(m / 60)}h ${m % 60}m` : `${m}m`;
}

export function youtubeId(url: string | null): string | null {
  const m = url?.match(/(?:youtu\.be\/|v=|\/shorts\/|\/live\/|\/embed\/)([\w-]{11})/);
  return m ? m[1] : null;
}

/** Deep link into the source at a timestamp, when the platform supports it. */
export function linkAt(url: string | null, seconds: number): string | null {
  if (!url) return null;
  const id = youtubeId(url);
  if (id) return `https://www.youtube.com/watch?v=${id}&t=${Math.floor(seconds)}s`;
  if (/vimeo\.com/.test(url)) return `${url.split("#")[0]}#t=${Math.floor(seconds)}s`;
  return null;
}
