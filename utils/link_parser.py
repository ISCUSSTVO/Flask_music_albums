import re
from urllib.parse import urlparse, parse_qs


def parse_link(url: str):
    parsed = urlparse(url)
    query = parse_qs(parsed.query)

    # =========================
    # YOUTUBE
    # =========================
    if "youtube.com" in parsed.netloc or "youtu.be" in parsed.netloc:

        # 🎧 ПЛЕЙЛИСТ
        if "list" in query:
            playlist_id = query["list"][0]
            return {
                "service": "youtube",
                "media_type": "playlist",
                "embed": f"https://www.youtube.com/embed/videoseries?list={playlist_id}"
            }

        # 🎵 ТРЕК
        video_id = None

        if "v" in query:
            video_id = query["v"][0]

        elif "youtu.be" in parsed.netloc:
            video_id = parsed.path.strip("/")

        if video_id and len(video_id) == 11:
            return {
                "service": "youtube",
                "media_type": "track",
                "embed": f"https://www.youtube.com/embed/{video_id}"
            }

    return None
