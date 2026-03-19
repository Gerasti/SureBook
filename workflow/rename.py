import os
from typing import List, Optional

from fileutils import (
    normalize_topic, read_non_empty, write_files,
    parse_section_name, read_list_lines,
)


def rename_topic(
    old_name: str,
    new_name: str,
    toml_path: str,
    input_paths: List[str],
    list_paths: List[str],
    list_names: Optional[List[str]] = None,
) -> None:
    for p in input_paths:
        topics = read_non_empty(p)
        if old_name in topics:
            write_files(p, [new_name if t == old_name else t for t in topics])
            print(f"Renamed in input [{p}]: {old_name} -> {new_name}")

    for p in list_paths:
        lines = read_list_lines(p)
        new_lines = []
        changed = False
        in_target_section = list_names is None

        section_topics: dict = {}
        sec = None
        for line in lines:
            sn = parse_section_name(line)
            if sn is not None:
                sec = sn
            elif line.strip() and sec is not None:
                section_topics.setdefault(sec, []).append(line.strip())

        sec = None
        for line in lines:
            stripped = line.strip()
            sn = parse_section_name(line)
            if sn is not None:
                sec = sn
                in_target_section = list_names is None or (sec in list_names if list_names else True)
                new_lines.append(line)
                continue
            if in_target_section and stripped == old_name:
                if sec and new_name in (section_topics.get(sec) or []):
                    if new_lines and new_lines[-1].strip() == "":
                        new_lines.pop()
                    print(f"Removed duplicate in [{p}] section [{sec}]: {old_name}")
                else:
                    new_lines.append(new_name + "\n")
                    print(f"Renamed in list [{p}] section [{sec}]: {old_name} -> {new_name}")
                changed = True
                continue
            new_lines.append(line)

        if changed:
            with open(p, "w", encoding="utf-8") as f:
                f.writelines(new_lines)

    if not os.path.exists(toml_path):
        return
    old_key = normalize_topic(old_name)
    new_key = normalize_topic(new_name)
    with open(toml_path, "r", encoding="utf-8") as f:
        content = f.read()
    new_content = content.replace(f'[topics."{old_key}"]', f'[topics."{new_key}"]')
    new_content = new_content.replace(f'title = "{old_name}"', f'title = "{new_name}"')
    new_content = new_content.replace(f'{old_key}.md', f'{new_key}.md')
    if new_content != content:
        with open(toml_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Renamed in TOML: {old_name} -> {new_name}")
    else:
        print(f"Not found in TOML: {old_name}")


def rename_list(old_name: str, new_name: str, list_paths: List[str]) -> None:
    old_header = f"## {old_name} list:"
    new_header = f"## {new_name} list:"

    for p in list_paths:
        lines = read_list_lines(p)
        if not any(line.strip() == old_header for line in lines):
            continue

        new_exists = any(line.strip() == new_header for line in lines)

        if not new_exists:
            new_lines = [new_header + "\n" if line.strip() == old_header else line for line in lines]
            with open(p, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
            print(f"Renamed list [{p}]: {old_name} -> {new_name}")
        else:
            old_topics = []
            in_old = False
            for line in lines:
                if line.strip() == old_header:
                    in_old = True
                    continue
                if in_old and parse_section_name(line) is not None:
                    break
                if in_old and line.strip():
                    old_topics.append(line.strip())

            new_topics_existing = []
            in_new = False
            for line in lines:
                if line.strip() == new_header:
                    in_new = True
                    continue
                if in_new and parse_section_name(line) is not None:
                    break
                if in_new and line.strip():
                    new_topics_existing.append(line.strip())

            to_add = [t for t in old_topics if t not in new_topics_existing]

            new_lines = []
            skip_old = False
            for line in lines:
                if line.strip() == old_header:
                    skip_old = True
                    continue
                if skip_old and parse_section_name(line) is not None:
                    skip_old = False
                if skip_old:
                    continue
                new_lines.append(line)
                if line.strip() == new_header:
                    for t in to_add:
                        new_lines.append(t + "\n")
                        new_lines.append("\n")

            with open(p, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
            print(f"Merged list [{p}]: {old_name} -> {new_name} ({len(to_add)} topics added)")
