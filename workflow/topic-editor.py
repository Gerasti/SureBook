#!/usr/bin/env python3

import argparse
import os
import re
from pathlib import Path

TOPICS_TOML_PATH = os.path.expanduser("~/surebook/info/topics.toml")

# =======================
# File Utils
# =======================
def read_non_empty(path: str) -> list[str]:
    if not os.path.isfile(path):
        return []
    with open(path, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def read_list_file(path: str) -> list[str]:
    if not os.path.isfile(path):
        return []
    result = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.endswith("list:") or line.startswith("#"):
                continue
            result.append(line)
    return result

def write_files(path: str, items: list[str]):
    with open(path, "w", encoding="utf-8") as f:
        for i in items:
            f.write(i + "\n")

def uniq_keep_order(items: list[str]) -> list[str]:
    return list(dict.fromkeys(items))

def diff_lists(list1: list[str], list2: list[str]) -> list[str]:
    return [x for x in list1 if x not in list2]

def normalize_topic(name: str) -> str:
    return re.sub(r"\s+", "_", name.strip())

def paths_to_list(val: str) -> list[str]:
    return [os.path.expanduser(p.strip()) for p in val.split(":") if p.strip()]

def paths_to_str(paths: list[str]) -> str:
    return ":".join(paths)

def read_list_lines(path: str) -> list[str]:
    if not path or not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return f.readlines()

def parse_section_name(line: str) -> str | None:
    stripped = line.strip()
    if stripped.startswith("##") and stripped.endswith("list:"):
        return stripped[3:-6].strip()
    return None

def find_section_header(lines: list[str], section: str) -> bool:
    header = f"## {section} list:"
    return any(line.strip() == header for line in lines)

def sort_list_file(path: str):
    if not path or not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    current_header = None
    current_section = []

    def flush_section():
        if current_header is not None:
            new_lines.append(current_header)
            for t in sorted(current_section, key=str.casefold):
                new_lines.append(t + "\n")
                new_lines.append("\n")

    for line in lines:
        section_name = parse_section_name(line)
        if section_name is not None:
            flush_section()
            current_header = line
            current_section = []
        elif line.strip():
            current_section.append(line.strip())

    flush_section()

    with open(path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

def print_section(name: str, items: list[str], solid: bool = False):
    if not solid:
        print(f"\n[{name}] ({len(items)}):")
    for t in items:
        print(f"  {t}" if not solid else t)

def strip_link(topic: str) -> str:
    """Remove markdown link from topic, keeping only the topic name."""
    return re.sub(r'\s+\[.*?\]\(.*?\)', '', topic).strip()

def extract_link(topic: str) -> tuple[str | None, str | None]:
    """Extract (link_look, url) from topic with markdown link, or (None, None)."""
    m = re.search(r'\[([^\]]+)\]\(([^)]+)\)', topic)
    if m:
        return m.group(1), m.group(2)
    return None, None

def is_topic_duplicate(line: str, existing_lines: list[str]) -> bool:
    """True if plain topic already exists in lines (with or without link)."""
    plain = strip_link(line.strip())
    for l in existing_lines:
        if strip_link(l.strip()) == plain:
            return True
    return False

# =======================
# TOML-like Defaults
# =======================
def load_defaults(toml_path: str) -> dict:
    defaults_to_write = {
        "input": os.path.expanduser("~/surebook/info/topics.md"),
        "list": os.path.expanduser("~/surebook/info/topic-lists.md"),
        "topic_save": os.path.expanduser("~/surebook/topics"),
        "auto_alphabetic_sort": "false",
        "auto_save": "false",
    }
    defaults = {}
    updated = False
    section = None

    if os.path.exists(toml_path):
        try:
            with open(toml_path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if line.startswith("[") and line.endswith("]"):
                        section = line[1:-1].strip()
                        continue
                    if "=" in line and section == "paths":
                        key, val = line.split("=", 1)
                        defaults[key.strip()] = os.path.expanduser(val.strip().strip('"'))
        except Exception:
            pass
    else:
        updated = True

    for k, v in defaults_to_write.items():
        if k not in defaults:
            defaults[k] = v
            updated = True

    if updated:
        save_defaults(toml_path, defaults)

    return defaults

def save_defaults(toml_path: str, defaults: dict):
    os.makedirs(os.path.dirname(toml_path), exist_ok=True)
    other_lines = []
    if os.path.exists(toml_path):
        with open(toml_path, encoding="utf-8") as f:
            in_paths = False
            for line in f:
                stripped = line.strip()
                if stripped == "[paths]":
                    in_paths = True
                    continue
                if in_paths and stripped.startswith("["):
                    in_paths = False
                if not in_paths:
                    other_lines.append(line)

    with open(toml_path, "w", encoding="utf-8") as f:
        f.write("[paths]\n")
        for k, v in defaults.items():
            f.write(f'{k} = "{v}"\n')
        if other_lines:
            f.write("\n")
            f.writelines(other_lines)


# =======================
# Save Topics to TOML + MD
# =======================
def load_existing_topic_keys(toml_path: str) -> set[str]:
    """Return the set of topic keys already present in the TOML file."""
    existing = set()
    if not os.path.exists(toml_path):
        return existing
    with open(toml_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith('[topics."'):
                key = line.split('"')[1]
                existing.add(key)
    return existing


def save_topics_to_toml(toml_path: str, topics: list[str], base_dir: str):
    existing = load_existing_topic_keys(toml_path)

    lines = []
    if os.path.exists(toml_path):
        with open(toml_path, encoding="utf-8") as f:
            lines = f.read().splitlines()

    # дедуплицировать по clean key — предпочитать версию со ссылкой
    seen_keys: dict[str, str] = {}
    for t in topics:
        key = normalize_topic(strip_link(t))
        if key in existing:
            continue
        # если уже есть версия этой темы — предпочесть ту, что содержит ссылку
        if key not in seen_keys or extract_link(t)[1] is not None:
            seen_keys[key] = t

    new_topics = list(seen_keys.values())
    if not new_topics:
        print("Nothing to save — all topics already in TOML")
        return

    with open(toml_path, "a", encoding="utf-8") as f:
        if "[topics]" not in "\n".join(lines):
            f.write("\n[topics]\n")

        os.makedirs(base_dir, exist_ok=True)

        for topic in new_topics:
            clean_topic = strip_link(topic)
            link_look, link_url = extract_link(topic)
            key = normalize_topic(clean_topic)
            md_path = os.path.join(base_dir, f"{key}.md")

            f.write(f'\n[topics."{key}"]\n')
            f.write(f'title = "{clean_topic}"\n')
            f.write(f'path = "{md_path}"\n')
            if link_url:
                f.write(f'link = "{link_url}"\n')
            if link_look and link_look != clean_topic:
                f.write(f'link-look = "{link_look}"\n')

            if not os.path.exists(md_path):
                Path(md_path).touch()
            print(f"Saved: {clean_topic}")
    print(f"Total saved: {len(new_topics)}")


# =======================
# Add, Remove, Rename, and Linked
# =======================

def add_topics_to_input(topics_to_add: list[str], input_path: str):
    existing = read_non_empty(input_path)
    new = [t for t in topics_to_add if t not in existing]
    if not new:
        print("Topics already exist in input, skipping")
        return
    with open(input_path, "a", encoding="utf-8") as f:
        for t in new:
            f.write(t + "\n")
            print(f"Added to input: {t}")


def add_topics_to_list(topics_to_add: list[str], list_path: str, section: str):
    lines = read_list_lines(list_path)
    header = f"## {section} list:"
    section_found = find_section_header(lines, section)

    with open(list_path, "a" if not section_found else "r+", encoding="utf-8") as f:
        if not section_found:
            f.write(f"\n{header}\n")
            for t in topics_to_add:
                f.write(t + "\n\n")
                print(f"Added to list [{section}]: {t}")
            return

    new_lines = []
    i = 0
    while i < len(lines):
        new_lines.append(lines[i])
        if lines[i].strip() == header:
            existing_in_section = []
            j = i + 1
            while j < len(lines) and not lines[j].strip().startswith("##"):
                if lines[j].strip():
                    existing_in_section.append(lines[j].strip())
                j += 1
            for t in topics_to_add:
                if not is_topic_duplicate(t, existing_in_section):
                    new_lines.append(t + "\n")
                    new_lines.append("\n")
                    print(f"Added to list [{section}]: {t}")
                else:
                    print(f"Already exists in [{section}], skipping: {t}")
        i += 1

    with open(list_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

def add_topics(topics_to_add: list[str], toml_path: str, base_dir: str):
    if not topics_to_add:
        return

    existing = load_existing_topic_keys(toml_path)

    lines = []
    if os.path.exists(toml_path):
        with open(toml_path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()

    os.makedirs(base_dir, exist_ok=True)

    with open(toml_path, "a", encoding="utf-8") as f:
        if "[topics]" not in "\n".join(lines):
            f.write("\n[topics]\n")

        for topic in topics_to_add:
            topic = topic.strip('"')
            key = normalize_topic(topic)
            if key in existing:
                print(f"Topic already exists, skipping: {topic}")
                continue
            md_path = os.path.join(base_dir, f"{key}.md")
            f.write(f'\n[topics."{key}"]\n')
            f.write(f'title = "{topic}"\n')
            f.write(f'path = "{md_path}"\n')
            Path(md_path).touch()
            print(f"Added topic: {topic}")

def remove_from_list_file(path: str, keys_to_del: set[str], titles_to_del: set[str]):
    if not path or not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            new_lines.append(line)
            continue
        if stripped in titles_to_del or normalize_topic(stripped) in keys_to_del:
            if new_lines and new_lines[-1].strip() == "":
                new_lines.pop()
            continue
        new_lines.append(line)

    with open(path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
def del_topics(topics_to_del: list[str], toml_path: str, input_path: str, list_path: str):
    if not topics_to_del or not os.path.exists(toml_path):
        return

    keys_to_del = {normalize_topic(t.strip('"')) for t in topics_to_del}
    titles_to_del = {t.strip('"') for t in topics_to_del}

    with open(toml_path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    section_starts = []
    for i, line in enumerate(lines):
        if line.startswith('[topics."'):
            key = line.split('"')[1]
            title = ""
            if i + 1 < len(lines) and "=" in lines[i + 1]:
                title = lines[i + 1].split("=", 1)[1].strip().strip('"')
            section_starts.append((i, key, title))

    lines_to_skip = set()
    for idx, (start, key, title) in enumerate(section_starts):
        if key not in keys_to_del and title not in titles_to_del:
            continue

        for j in range(start + 1, start + 4):
            if j < len(lines) and lines[j].strip().startswith("path"):
                md_path = lines[j].split("=", 1)[1].strip().strip('"')
                if os.path.exists(md_path):
                    os.remove(md_path)
                    print(f"Deleted file: {md_path}")
                break

        end = section_starts[idx + 1][0] if idx + 1 < len(section_starts) else len(lines)
        for j in range(start, end):
            lines_to_skip.add(j)
        print(f"Deleted topic: {title or key}")

    new_lines = [line for i, line in enumerate(lines) if i not in lines_to_skip]

    with open(toml_path, "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines) + "\n")
    if input_path and os.path.exists(input_path):
        topics = read_non_empty(input_path)
        new_topics = [t for t in topics if t not in titles_to_del and normalize_topic(t) not in keys_to_del]
        write_files(input_path, new_topics)

    remove_from_list_file(list_path, keys_to_del, titles_to_del)

def remove_from_list_section(list_path: str, section: str, keys_to_del: set[str], titles_to_del: set[str]):
    lines = read_list_lines(list_path)
    if not lines:
        return

    header = f"## {section} list:"
    if not find_section_header(lines, section):
        print(f"List not found: {section}")
        return

    new_lines = []
    in_section = False
    for line in lines:
        stripped = line.strip()
        if stripped == header:
            in_section = True
            new_lines.append(line)
            continue
        if in_section and stripped.startswith("##"):
            in_section = False
        if in_section and (stripped in titles_to_del or normalize_topic(stripped) in keys_to_del):
            if new_lines and new_lines[-1].strip() == "":
                new_lines.pop()
            print(f"Deleted from [{section}]: {stripped}")
            continue
        new_lines.append(line)

    with open(list_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

def add_list(section: str, list_path: str):
    lines = []
    if os.path.exists(list_path):
        with open(list_path, encoding="utf-8") as f:
            lines = f.readlines()

    header = f"## {section} list:"
    for line in lines:
        if line.strip() == header:
            print(f"List already exists: {section}")
            return

    with open(list_path, "a", encoding="utf-8") as f:
        f.write(f"{header}\n")
    print(f"Added list: {section}")


def del_list(section: str, list_path: str):
    lines = read_list_lines(list_path)
    if not lines:
        return

    header = f"## {section} list:"
    section_found = False
    topics_in_section = []

    i = 0
    while i < len(lines):
        if lines[i].strip() == header:
            section_found = True
            j = i + 1
            while j < len(lines) and not lines[j].strip().startswith("##"):
                if lines[j].strip():
                    topics_in_section.append(lines[j].strip())
                j += 1
            break
        i += 1

    if not section_found:
        print(f"List not found: {section}")
        return

    if topics_in_section:
        print(f"List [{section}] contains {len(topics_in_section)} topics:")
        for t in topics_in_section:
            print(f"  {t}")
        answer = input("Delete list with all topics? [y/N]: ").strip().lower()
        if answer != "y":
            print("Cancelled")
            return

    new_lines = []
    skip = False
    for line in lines:
        if line.strip() == header:
            skip = True
            continue
        if skip and line.strip().startswith("##"):
            skip = False
        if not skip:
            new_lines.append(line)

    with open(list_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    print(f"Deleted list: {section}")

def read_list_sections(path: str, sections: list[str]) -> list[str]:
    lines = read_list_lines(path)
    result = []
    in_section = False

    for line in lines:
        section_name = parse_section_name(line)
        if section_name is not None:
            in_section = section_name in sections
            continue
        if in_section and line.strip():
            result.append(line.strip())

    return result

def read_list_headers(path: str) -> list[str]:
    lines = read_list_lines(path)
    result = []
    for line in lines:
        section_name = parse_section_name(line)
        if section_name is not None:
            result.append(section_name)
    return result

def rename_topic(old_name: str, new_name: str, toml_path: str,
                 input_paths: list[str], list_paths: list[str],
                 list_names: list[str] | None = None):
    # input files — всегда все
    for p in input_paths:
        topics = read_non_empty(p)
        if old_name in topics:
            write_files(p, [new_name if t == old_name else t for t in topics])
            print(f"Renamed in input [{p}]: {old_name} -> {new_name}")

    # list files — только указанные секции если есть --list-name, иначе все
    for p in list_paths:
            lines = read_list_lines(p)
            new_lines = []
            changed = False
            in_target_section = list_names is None
            current_section_topics = []
            # сначала собрать темы каждой секции для проверки дублей
            section_topics: dict[str, list[str]] = {}
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
                    in_target_section = list_names is None or sec in list_names
                    new_lines.append(line)
                    continue
                if in_target_section and stripped == old_name:
                    # если новое имя уже есть в этой секции — просто удалить старое
                    if new_name in section_topics.get(sec, []):
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

    # toml — всегда
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

def rename_list(old_name: str, new_name: str, list_paths: list[str]):
    old_header = f"## {old_name} list:"
    new_header = f"## {new_name} list:"

    for p in list_paths:
        lines = read_list_lines(p)
        if not any(line.strip() == old_header for line in lines):
            continue

        # check if new_name section already exists — need to merge
        new_exists = any(line.strip() == new_header for line in lines)

        if not new_exists:
            # simple rename
            new_lines = [new_header + "\n" if line.strip() == old_header else line for line in lines]
            with open(p, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
            print(f"Renamed list [{p}]: {old_name} -> {new_name}")
        else:
            # collect topics from old section
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

            # collect existing topics in new section to avoid dupes
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

            # rebuild: remove old section, append to_add after new_header
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

def set_add_link(topic: str, list_paths: list[str], list_names: list[str] | None,
                   link: str, link_look: str | None = None):
    display = link_look if link_look else topic
    md_link = f"{topic} [{display}]({link})"

    for p in list_paths:
        lines = read_list_lines(p)
        new_lines = []
        changed = False
        sec = None
        in_target = list_names is None

        for line in lines:
            stripped = line.strip()
            sn = parse_section_name(line)
            if sn is not None:
                sec = sn
                in_target = list_names is None or sec in list_names
                new_lines.append(line)
                continue
            if in_target and strip_link(stripped) == topic:
                new_lines.append(md_link + "\n")
                print(f"Set link in [{p}] section [{sec}]: {md_link}")
                changed = True
            else:
                new_lines.append(line)

        if changed:
            with open(p, "w", encoding="utf-8") as f:
                f.writelines(new_lines)

    # проверить что указанные листы существуют
        if list_names:
            all_headers = [h for p in list_paths for h in read_list_headers(p)]
            for name in list_names:
                if name not in all_headers:
                    print(f"List not found: {name}")

        # проверить что тема найдена хотя бы в одном из целевых листов
        found_in_any = False
        for p in list_paths:
            lines = read_list_lines(p)
            sec = None
            for line in lines:
                sn = parse_section_name(line)
                if sn is not None:
                    sec = sn
                    continue
                stripped = line.strip()
                in_target = list_names is None or sec in (list_names or [])
                if in_target and (stripped == topic or stripped.startswith(f"{topic} [")):
                    found_in_any = True
                    break
            if found_in_any:
                break

        if not found_in_any:
            print(f"Topic not found: {topic}")

def del_add_link(topic: str, list_paths: list[str], list_names: list[str] | None):
    for p in list_paths:
        lines = read_list_lines(p)
        new_lines = []
        changed = False
        sec = None
        in_target = list_names is None

        for line in lines:
            sn = parse_section_name(line)
            if sn is not None:
                sec = sn
                in_target = list_names is None or sec in list_names
                new_lines.append(line)
                continue
            stripped = line.strip()
            if in_target and stripped.startswith(f"{topic} ["):
                new_lines.append(topic + "\n")
                print(f"Removed link in [{p}] section [{sec}]: {stripped} -> {topic}")
                changed = True
            else:
                new_lines.append(line)

        if changed:
            with open(p, "w", encoding="utf-8") as f:
                f.writelines(new_lines)

    # проверить что листы существуют
    if list_names:
        all_headers = [h for p in list_paths for h in read_list_headers(p)]
        for name in list_names:
            if name not in all_headers:
                print(f"List not found: {name}")

def search_topic(query: str, topics_i: list[str], list_path: str, solid: bool = False) -> None:
    query_lower = query.casefold()
    matches_input = [t for t in topics_i if query_lower in t.casefold()]

    if matches_input:
        print_section("input", matches_input, solid)

    if not os.path.exists(list_path):
        return

    lines = read_list_lines(list_path)
    current_section = None
    section_matches = {}

    for line in lines:
        section_name = parse_section_name(line)
        if section_name is not None:
            current_section = section_name
        elif line.strip() and current_section is not None:
            if query_lower in line.strip().casefold():
                section_matches.setdefault(current_section, []).append(line.strip())

    for section, matches in section_matches.items():
        print_section(section, matches, solid)

    if not matches_input and not section_matches:
        print(f"Not found: {query}")


def load_toml_topics(toml_path: str) -> list[dict]:
    """Load all topics from TOML as list of dicts: key, title, path, link, link_look."""
    topics = []
    if not os.path.exists(toml_path):
        return topics
    with open(toml_path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    current = None
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('[topics."'):
            if current is not None:
                topics.append(current)
            key = stripped.split('"')[1]
            current = {"key": key, "title": "", "path": "", "link": None, "link_look": None}
        elif current is not None and "=" in stripped:
            k, v = stripped.split("=", 1)
            k = k.strip()
            v = v.strip().strip('"')
            if k == "title":
                current["title"] = v
            elif k == "path":
                current["path"] = v
            elif k == "link":
                current["link"] = v
            elif k == "link-look":
                current["link_look"] = v
    if current is not None:
        topics.append(current)
    return topics


def load_list_topics_with_sections(list_paths: list[str]) -> dict[str, list[str]]:
    """Return dict: topic_title -> list of section names it appears in."""
    topic_sections: dict[str, list[str]] = {}
    for p in list_paths:
        lines = read_list_lines(p)
        current_section = None
        for line in lines:
            sn = parse_section_name(line)
            if sn is not None:
                current_section = sn
                continue
            stripped = line.strip()
            if stripped and current_section:
                plain = strip_link(stripped)
                topic_sections.setdefault(plain, [])
                if current_section not in topic_sections[plain]:
                    topic_sections[plain].append(current_section)
    return topic_sections


def load_list_links_by_section(list_paths: list[str]) -> dict[tuple, tuple]:
    """Return dict: (topic_title, section) -> (link_look, url)."""
    result = {}
    for p in list_paths:
        lines = read_list_lines(p)
        current_section = None
        for line in lines:
            sn = parse_section_name(line)
            if sn is not None:
                current_section = sn
                continue
            stripped = line.strip()
            if stripped and current_section:
                plain = strip_link(stripped)
                link_look, url = extract_link(stripped)
                if url:
                    result[(plain, current_section)] = (link_look, url)
    return result


def generate_source_table(toml_path: str, list_paths: list[str], out_path: str):
    topics = load_toml_topics(toml_path)
    topic_sections = load_list_topics_with_sections(list_paths)
    section_links = load_list_links_by_section(list_paths)

    lines = []
    lines.append("| № | Topic | Sources (lists + links) |")
    lines.append("|---|-------|-------------------------|")

    for i, t in enumerate(topics, 1):
        title = t["title"]
        sections = topic_sections.get(title, [])

        sources_parts = []
        for sec in sections:
            link_data = section_links.get((title, sec))
            if link_data:
                look, url = link_data
                sources_parts.append(f"{sec} [{look}]({url})")
            else:
                sources_parts.append(sec)

        sources = ", ".join(sources_parts) if sources_parts else ""
        lines.append(f"|{i:>3} | {title} | {sources} |")

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Source table saved: {out_path} ({len(topics)} topics)")

# =======================
# CLI
# =======================
def main():
    parser = argparse.ArgumentParser(description="Topics tool")

    parser.add_argument("-i", "--input", nargs="+", help="Topics files (overrides default)")
    parser.add_argument("-l", "--list", nargs="+", help="Topic-lists files (overrides default)")
    parser.add_argument("--sh", "--show", dest="show", type=int, nargs='?', const=-1,
                        help="Show first N topics (default: all)")
    parser.add_argument("--count", action="store_true", help="Show count of topics")
    parser.add_argument("--ab", action="store_true",
                        help="Sort topics alphabetically AND rewrite input/list files")
    parser.add_argument("--compare", action="store_true",
                        help="Show differences between input and list")
    parser.add_argument("--settings", action="store_true",
                        help="Show current input and list files")
    parser.add_argument("--edit", action="store_true", help="Edit default paths")
    parser.add_argument("--default-input", nargs="+", help="Set default input paths (used with --edit)")
    parser.add_argument("--default-list", nargs="+", help="Set default list paths (used with --edit)")
    parser.add_argument("--default-topic-save",
                        help="Set default directory for topic markdown files")
    parser.add_argument("--add-topic", nargs="+", help="Add topics to input file (or list with --list-name)")
    parser.add_argument("--list-name", nargs="+", help="Section names in topic-lists.md to add topics to")
    parser.add_argument("--del-topic", nargs="+", help="Delete topics from topics.toml")
    parser.add_argument("--show-input", type=int, nargs='?', const=-1, help="Show all or first N topics from input file")
    parser.add_argument("--add-list", nargs="+", help="Add new sections to topic-lists.md")
    parser.add_argument("--del-list", nargs="+", help="Delete sections from topic-lists.md")
    parser.add_argument("--show-lists", type=int, nargs='?', const=-1, help="Show all or first N list section names")
    parser.add_argument("--solid", action="store_true", help="Disable section name headers in output")
    parser.add_argument("--search", help="Search topic across input and lists")
    parser.add_argument("--rename-topic", nargs=2, metavar=("OLD", "NEW"), help="Rename topic in input, list and TOML")
    parser.add_argument("--rename-list", nargs=2, metavar=("OLD", "NEW"), help="Rename list section in list files")
    parser.add_argument("--add-link", help="Topic name to set a link for (requires --list-name, --link-look, --link)")
    parser.add_argument("--del-link", help="Topic name to remove link from (requires --list-name)")
    parser.add_argument("--link", help="URL for the topic link (used with --add-link)")
    parser.add_argument("--link-look", help="Display text for the link (used with --add-link)")
    parser.add_argument("--save", action="store_true", help="Save topics to TOML and create .md files")
    parser.add_argument("--unsave", nargs="+", help="Remove topics from TOML (and delete .md files)")
    parser.add_argument("--show-save", action="store_true", help="Show topics that would be saved on --save")
    parser.add_argument("--auto-ab", choices=["true", "false"], help="Enable/disable auto alphabetic sort on every run")
    parser.add_argument("--auto-save", choices=["true", "false"], help="Enable/disable auto save to TOML on every run")
    parser.add_argument("--source-table", "--src-table", dest="source_table",
                        action="store_true", help="Generate markdown source table to ~/surebook/info/TEST-source-table.md")
    args = parser.parse_args()

    defaults = load_defaults(TOPICS_TOML_PATH)

    if args.edit:
        changed = False
        if args.default_input:
            defaults["input"] = paths_to_str([os.path.expanduser(p) for p in args.default_input])
            print(f"Default input set to: {defaults['input']}")
            changed = True
        if args.default_list:
            defaults["list"] = paths_to_str([os.path.expanduser(p) for p in args.default_list])
            print(f"Default list set to: {defaults['list']}")
            changed = True
        if args.default_topic_save:
            defaults["topic_save"] = os.path.expanduser(args.default_topic_save)
            print(f"Default topic save dir set to: {defaults['topic_save']}")
            changed = True
        if args.auto_ab:
            defaults["auto_alphabetic_sort"] = args.auto_ab
            print(f"Auto alphabetic sort set to: {args.auto_ab}")
            changed = True
        if args.auto_save:
            defaults["auto_save"] = args.auto_save
            print(f"Auto save set to: {args.auto_save}")
            changed = True
        if changed:
            save_defaults(TOPICS_TOML_PATH, defaults)
        else:
            print("Nothing to edit. Use --default-input, --default-list or --default-topic-save")
        return

    default_inputs = paths_to_list(defaults.get("input", ""))
    default_lists = paths_to_list(defaults.get("list", ""))
    current_input_paths = args.input or default_inputs
    current_list_paths = args.list or default_lists
    current_input_path = current_input_paths[0] if current_input_paths else None
    current_list_path = current_list_paths[0] if current_list_paths else None
    current_topic_save_path = defaults.get("topic_save")

    if args.settings:
        print(f"Input files:          {', '.join(current_input_paths)}")
        print(f"List files:           {', '.join(current_list_paths)}")
        print(f"Topic save dir:       {current_topic_save_path}")
        print(f"Auto alphabetic sort: {defaults.get('auto_alphabetic_sort')}")
        print(f"Auto save:            {defaults.get('auto_save', 'false')}")

    topics_i = uniq_keep_order([t for p in current_input_paths for t in read_non_empty(p)])
    topics_l = uniq_keep_order([t for p in current_list_paths for t in read_list_file(p)])

    for p in current_input_paths:
        if not os.path.isfile(p):
            print(f"Warning: input file missing: {p}")
    for p in current_list_paths:
        if not os.path.isfile(p):
            print(f"Warning: list file missing: {p}")
    if not topics_i and not topics_l:
        print("Warning: both source files are empty or missing — nothing to save")

    if args.rename_topic:
        rename_topic(args.rename_topic[0], args.rename_topic[1],
                     TOPICS_TOML_PATH, current_input_paths, current_list_paths,
                     args.list_name)

    if args.rename_list:
        rename_list(args.rename_list[0], args.rename_list[1], current_list_paths)

    if args.add_link:
        missing = []
        if not args.list_name:
            missing.append("--list-name")
        if not args.link:
            missing.append("--link-look")
        if not args.link_look:
            missing.append("--link")
        if missing:
            print(f"Error: --add-link requires: {', '.join(missing)}")
        else:
            set_add_link(args.add_link, current_list_paths,
                           args.list_name, args.link, args.link_look)
    if args.del_link:
        missing = []
        if not args.list_name:
            missing.append("--list-name")
        if missing:
            print(f"Error: --del-link requires: {', '.join(missing)}")
        else:
            del_add_link(args.del_link, current_list_paths, args.list_name)

    if args.compare:
            all_files = (
                [(p, "input", read_non_empty(p)) for p in current_input_paths] +
                [(p, "list", read_list_file(p)) for p in current_list_paths]
            )
            for i, (p1, t1_type, t1) in enumerate(all_files):
                for p2, t2_type, t2 in all_files[i+1:]:
                    diff_1 = diff_lists(t1, t2)
                    diff_2 = diff_lists(t2, t1)
                    if not args.solid:
                        print(f"\n[{p1} ({t1_type})] vs [{p2} ({t2_type})]")
                    if diff_1:
                        if not args.solid:
                            print(f"  Only in {p1} ({len(diff_1)}):")
                        for t in diff_1:
                            print(f"    {t}" if not args.solid else t)
                    if diff_2:
                        if not args.solid:
                            print(f"  Only in {p2} ({len(diff_2)}):")
                        for t in diff_2:
                            print(f"    {t}" if not args.solid else t)
                    if not diff_1 and not diff_2:
                        if not args.solid:
                            print("  No differences found")

    topics = uniq_keep_order(topics_i + topics_l)

    auto_ab = defaults.get("auto_alphabetic_sort", "false") == "true"

    if args.ab or auto_ab:
        sorted_topics = sorted(topics, key=str.casefold)
        for p in current_input_paths:
            file_topics = read_non_empty(p)
            write_files(p, sorted(file_topics, key=str.casefold))
        for p in current_list_paths:
            sort_list_file(p)
        topics = sorted_topics

    if args.count:
            count_input = len(topics_i)
            count_list = len(topics_l)
            count_union_uniq = len(topics)
            count_common = len(set(topics_i) & set(topics_l))
            count_input_uniq = len(set(topics_i))
            count_list_uniq = len(set(strip_link(t) for t in topics_l))

            # темы со ссылками в листах
            list_link_topics = set()
            for lp in current_list_paths:
                for line in read_list_lines(lp):
                    stripped = line.strip()
                    if stripped and extract_link(stripped)[1] is not None:
                        list_link_topics.add(strip_link(stripped))

            # уникальные темы с учётом дублей (тема и тема со ссылкой — одна)
            union_clean = set(strip_link(t) for t in topics)

            print(f"Union uniq topics: {len(union_clean)}")
            print(f"Common topics:     {count_common}")
            print()
            print(f"All input topics:  {count_input}")
            print(f"Input uniq topics: {count_input_uniq}")
            print()
            print(f"All list topics:   {count_list}")
            print(f"List uniq topics:  {count_list_uniq}")
            print(f"List link topics:  {len(list_link_topics)}")

    if args.show is not None:
        if args.list_name:
            for section in args.list_name:
                section_topics = read_list_sections(current_list_path, [section])
                if args.show != -1:
                    section_topics = section_topics[:args.show]
                print_section(section, section_topics, args.solid)
        else:
            display = topics if args.show == -1 else topics[:args.show]
            for t in display:
                print(t)

    if args.search:
        for lp in current_list_paths:
            search_topic(args.search, topics_i, lp, args.solid)

    if args.add_topic:
        if args.list_name:
            for section in args.list_name:
                add_topics_to_list(args.add_topic, current_list_path, section)
        else:
            add_topics_to_input(args.add_topic, current_input_path)

    if args.del_topic:
        if args.list_name:
            keys_to_del = {normalize_topic(t.strip('"')) for t in args.del_topic}
            titles_to_del = {t.strip('"') for t in args.del_topic}
            for section in args.list_name:
                for lp in current_list_paths:
                    remove_from_list_section(lp, section, keys_to_del, titles_to_del)
        else:
            for ip in current_input_paths:
                del_topics(args.del_topic, TOPICS_TOML_PATH, ip, None)
            for lp in current_list_paths:
                del_topics(args.del_topic, TOPICS_TOML_PATH, None, lp)

    if args.show_input is not None:
        if not topics_i:
            print("Input file is empty or missing")
        else:
            display = topics_i if args.show_input == -1 else topics_i[:args.show_input]
            print(f"Input topics ({len(display)}/{len(topics_i)}):")
            for t in display:
                print(f"  {t}")

    if args.add_list:
        for section in args.add_list:
            add_list(section, current_list_path)

    if args.del_list:
        for section in args.del_list:
            del_list(section, current_list_path)

    if args.show_lists is not None:
        headers = read_list_headers(current_list_path)
        if not headers:
            print("No lists found")
        else:
            display = headers if args.show_lists == -1 else headers[:args.show_lists]
            if args.solid:
                for h in display:
                    print(h)
            else:
                print(f"Lists ({len(display)}/{len(headers)}):")
                for h in display:
                    print(f"  {h}")

    auto_save = defaults.get("auto_save", "false") == "true"

    if args.save or auto_save:
        if current_topic_save_path:
            save_topics_to_toml(TOPICS_TOML_PATH, topics, current_topic_save_path)
        else:
            print("Error: topic_save path is not set")

    if args.unsave:
        del_topics(args.unsave, TOPICS_TOML_PATH, input_path=None, list_path=None)

    if args.show_save:
            existing = load_existing_topic_keys(TOPICS_TOML_PATH)
            input_set = set(topics_i)

            topic_lists: dict[str, list[str]] = {}
            for lp in current_list_paths:
                lines = read_list_lines(lp)
                current_section = None
                seen_in_section: set[tuple] = set()
                for line in lines:
                    section_name = parse_section_name(line)
                    if section_name is not None:
                        current_section = section_name
                    elif line.strip() and current_section:
                        plain = strip_link(line.strip())
                        key = (plain, current_section)
                        if key not in seen_in_section:
                            seen_in_section.add(key)
                            topic_lists.setdefault(plain, [])
                            if current_section not in topic_lists[plain]:
                                topic_lists[plain].append(current_section)

            # дедуплицировать по clean key, предпочитать версию со ссылкой
            seen_keys: dict[str, str] = {}
            for t in topics:
                key = normalize_topic(strip_link(t))
                if key in existing:
                    continue
                if key not in seen_keys or extract_link(t)[1] is not None:
                    seen_keys[key] = t
            new_topics = list(seen_keys.values())

            if not new_topics:
                print("Nothing to save — all topics already in TOML")
            else:
                print(f"Would be saved ({len(new_topics)}):")
                for t in new_topics:
                    clean = strip_link(t)
                    parts = []
                    if clean in input_set:
                        parts.append("input")
                    if clean in topic_lists:
                        parts.extend(topic_lists[clean])
                    src = ", ".join(parts) if parts else "unknown"
                    print(f"  {clean}  [{src}]")

    if args.source_table:
        out_path = os.path.expanduser("~/surebook/info/TEST-source-table.md")
        generate_source_table(TOPICS_TOML_PATH, current_list_paths, out_path)

    any_action = any([
        args.show is not None,
        args.count,
        args.ab,
        args.rename_topic,
        args.rename_list,
        args.add_link,
        args.del_link,
        args.compare,
        args.settings,
        args.search,
        args.add_topic,
        args.del_topic,
        args.show_input is not None,
        args.add_list,
        args.del_list,
        args.show_lists is not None,
        args.save,
        args.unsave,
        args.show_save,
        args.source_table,
    ])
    if not any_action:
        parser.print_help()

if __name__ == "__main__":
    main()
