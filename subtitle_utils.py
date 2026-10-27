"""Small, dependency-free helpers for SubRip subtitles and caption lookup."""

import math


def format_time(seconds):
    """Format non-negative seconds as an SRT timestamp, rounding to milliseconds."""
    value = float(seconds)
    if not math.isfinite(value) or value < 0:
        raise ValueError("Timestamp must be a finite, non-negative number.")
    total_ms = int(round(value * 1000))
    hours, remainder = divmod(total_ms, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    whole_seconds, milliseconds = divmod(remainder, 1000)
    return f"{hours:02}:{minutes:02}:{whole_seconds:02},{milliseconds:03}"


def to_srt(segments):
    """Serialize timestamped text segments into UTF-8-ready SRT text."""
    blocks = []
    for index, segment in enumerate(segments, start=1):
        start = float(segment["start"])
        end = float(segment["end"])
        if end < start:
            raise ValueError(f"Subtitle segment {index} ends before it starts.")
        text = str(segment.get("text", "")).strip()
        blocks.append(
            f"{index}\n{format_time(start)} --> {format_time(end)}\n{text}"
        )
    return "\n\n".join(blocks) + ("\n\n" if blocks else "")


def get_caption_at(segments, timestamp):
    """Return the caption active at timestamp, or an empty string."""
    t = float(timestamp)
    for segment in segments:
        if segment["start"] <= t <= segment["end"]:
            return segment.get("text", "")
    return ""
