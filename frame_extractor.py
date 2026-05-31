
import os
import subprocess
import json
from pathlib import Path

def download_and_extract_frames(youtube_url, output_dir="painting_frames", fps=1):
    os.makedirs(output_dir, exist_ok=True)
    video_path = os.path.join(output_dir, "video.mp4")

    print("Downloading video...")
    result = subprocess.run([
        "yt-dlp",
        "-f", "best[ext=mp4]/best",
        "-o", video_path,
        youtube_url
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print("Download error:", result.stderr)
        return None
    print("Download complete.")

    frames_dir = os.path.join(output_dir, "frames")
    os.makedirs(frames_dir, exist_ok=True)

    print("Extracting frames at {}fps...".format(fps))
    subprocess.run([
        "ffmpeg", "-i", video_path,
        "-vf", "fps={}".format(fps),
        "-q:v", "2",
        os.path.join(frames_dir, "frame_%05d.jpg"),
        "-y", "-loglevel", "quiet"
    ])

    frame_files = sorted(Path(frames_dir).glob("*.jpg"))
    catalog = []
    for i, f in enumerate(frame_files):
        catalog.append({
            "index": i,
            "path":  str(f),
            "label": None
        })

    catalog_path = os.path.join(output_dir, "catalog.json")
    with open(catalog_path, "w") as f:
        json.dump(catalog, f, indent=2)

    print("Extracted {} frames".format(len(frame_files)))
    print("Catalog saved to {}".format(catalog_path))
    print("Ready for labeling!")
    return catalog
