#!/usr/bin/env python

import sys
import os
import re
import ffmpeg


def parse_cuts_file(cuts_file):
    cuts = []
    with open(cuts_file, "r") as f:
        for i, line in enumerate(f):
            line = line.strip()

            # Skip empty lines and comments
            if not line or line.startswith("#"):
                continue

            times, *description = line.split()

            if len(times.split("-")) == 2:
                start, end = times.split("-")
            else:
                start = times
                end = None

            cuts.append(
                {
                    "index": len(cuts) + 1,
                    "start": start,
                    "end": end,
                    "description": " ".join(description),
                }
            )

    # Fill in missing end times and calculate seconds
    for i, cut in enumerate(cuts):
        if cut["end"] == None and i < len(cuts) - 1:
            cut["end"] = cuts[i + 1]["start"]

        cut["start_seconds"] = parse_timestamp(cut["start"])
        if cut["end"] is not None:
            cut["end_seconds"] = parse_timestamp(cut["end"])

    return cuts


def parse_timestamp(timestamp):
    parts = timestamp.split(":")
    if len(parts) == 1:
        return int(parts[0])
    elif len(parts) == 2:
        return int(parts[0]) * 60 + int(parts[1])
    elif len(parts) == 3:
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    else:
        raise ValueError("Invalid timestamp format")


def output_filename(input_file, cut):
    directory = os.path.splitext(input_file)[0]
    extension = os.path.splitext(input_file)[1]
    safe_description = re.sub(r"[^\w_. -]", "_", cut["description"])
    return f"{directory}/{cut['index']:02d} {safe_description}{extension}"


def main():
    if len(sys.argv) < 3:
        print("Usage: cut-video <input_file> <cuts-file>")
        sys.exit(1)

    input_file = sys.argv[1]
    cuts_file = sys.argv[2]
    overwrite = len(sys.argv) > 3 and sys.argv[3].lower() == "--overwrite"

    if not os.path.exists(input_file) or not os.path.isfile(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)

    if not os.path.exists(cuts_file) or not os.path.isfile(cuts_file):
        print(f"Error: Cuts file '{cuts_file}' not found.")
        sys.exit(1)

    cuts = parse_cuts_file(sys.argv[2])

    target_directory = os.path.splitext(input_file)[0]
    if not os.path.exists(target_directory):
        os.mkdir(target_directory)

    for cut in cuts:
        if cut["end"] is None:
            cut["end_seconds"] = ffmpeg.probe(input_file)["format"]["duration"]

        video = (
            ffmpeg.input(input_file)
            .trim(start=cut["start_seconds"], end=cut["end_seconds"])
            .setpts("PTS-STARTPTS")
        )

        audio = (
            ffmpeg.input(input_file)
            .filter_("atrim", start=cut["start_seconds"], end=cut["end_seconds"])
            .filter_("asetpts", "PTS-STARTPTS")
        )

        ffmpeg.output(video, audio, output_filename(input_file, cut)).run(
            overwrite_output=overwrite
        )
