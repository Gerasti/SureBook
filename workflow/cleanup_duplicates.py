#!/usr/bin/env python3
"""Clean up duplicate topics in TOML file."""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from file_manager import FileManager


def cleanup_duplicates(toml_path: str) -> None:
    """Remove duplicate topic entries from TOML file."""
    if not FileManager.exists(toml_path):
        print(f"File not found: {toml_path}")
        return

    content = FileManager.read_text(toml_path)
    lines = content.split("\n")

    seen_topics = set()
    new_lines = []
    skip = False
    current_topic = None
    duplicates_removed = 0

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Check for topic header
        if stripped.startswith('[topics."') and stripped.endswith('"]'):
            # Extract topic key
            topic_key = stripped[9:-2]  # Remove [topics." and "]

            if topic_key in seen_topics:
                # This is a duplicate, skip it
                skip = True
                current_topic = topic_key
                duplicates_removed += 1
                print(f"Removing duplicate: {topic_key}")
                continue
            else:
                # First occurrence, keep it
                seen_topics.add(topic_key)
                skip = False
                current_topic = topic_key
                new_lines.append(line)
                continue

        # Check if we're entering a new section
        if stripped.startswith("[") and not stripped.startswith('[topics."'):
            skip = False
            current_topic = None

        # Add line if not skipping
        if not skip:
            new_lines.append(line)

    # Write cleaned content
    if duplicates_removed > 0:
        FileManager.write_text(toml_path, "\n".join(new_lines))
        print(f"\nRemoved {duplicates_removed} duplicate(s)")
        print(f"Cleaned file saved to: {toml_path}")
    else:
        print("No duplicates found")


if __name__ == "__main__":
    toml_path = os.path.expanduser("~/SureBook/info/topics.toml")

    if len(sys.argv) > 1:
        toml_path = sys.argv[1]

    print(f"Cleaning duplicates in: {toml_path}")
    cleanup_duplicates(toml_path)
