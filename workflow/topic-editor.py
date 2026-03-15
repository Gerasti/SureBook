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
        stripped = line.strip()
        if stripped.startswith("##") and stripped.endswith("list:"):
            flush_section()
            current_header = line
            current_section = []
        elif stripped:
            current_section.append(stripped)

    flush_section()

    with open(path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

# =======================
# TOML-like Defaults
# =======================
def load_defaults(toml_path: str) -> dict:
    defaults_to_write = {
        "input": os.path.expanduser("~/surebook/info/topics.md"),
        "list": os.path.expanduser("~/surebook/info/topic-lists.md"),
        "topic_save": os.path.expanduser("~/surebook/topics"),
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

    new_topics = [t for t in topics if normalize_topic(t) not in existing]
    if not new_topics:
        return

    with open(toml_path, "a", encoding="utf-8") as f:
        if "[topics]" not in "\n".join(lines):
            f.write("\n[topics]\n")

        os.makedirs(base_dir, exist_ok=True)

        for topic in new_topics:
            key = normalize_topic(topic)
            md_path = os.path.join(base_dir, f"{key}.md")

            f.write(f'\n[topics."{key}"]\n')
            f.write(f'title = "{topic}"\n')
            f.write(f'path = "{md_path}"\n')

            if not os.path.exists(md_path):
                Path(md_path).touch()


# =======================
# Add and Remove
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
    lines = []
    if os.path.exists(list_path):
        with open(list_path, encoding="utf-8") as f:
            lines = f.readlines()

    header = f"## {section} list:"
    section_found = False
    for line in lines:
        if line.strip() == header:
            section_found = True
            break

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
                if t not in existing_in_section:
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


# =======================
# CLI
# =======================
def main():
    parser = argparse.ArgumentParser(description="Topics tool")

    parser.add_argument("-i", "--input", help="Topics file (overrides default)")
    parser.add_argument("-l", "--list", help="Topic-lists file (overrides default)")
    parser.add_argument("--sh", "--show", dest="show", type=int, nargs='?', const=-1,
                        help="Show first N topics (default: all)")
    parser.add_argument("--count", action="store_true", help="Show count of topics")
    parser.add_argument("--ab", action="store_true",
                        help="Sort topics alphabetically AND rewrite input/list files")
    parser.add_argument("--compare", action="store_true",
                        help="Show differences between input and list")
    parser.add_argument("--sources", action="store_true",
                        help="Show current input and list files")
    parser.add_argument("--edit", action="store_true", help="Edit default paths")
    parser.add_argument("--default-input", help="Set new default input path (used with --edit)")
    parser.add_argument("--default-list", help="Set new default list path (used with --edit)")
    parser.add_argument("--default-topic-save",
                        help="Set default directory for topic markdown files")
    parser.add_argument("--add-topic", nargs="+", help="Add topics to input file (or list with --list-name)")
    parser.add_argument("--list-name", help="Section name in topic-lists.md to add topics to")
    parser.add_argument("--del-topic", nargs="+", help="Delete topics from topics.toml")
    parser.add_argument("--save", action="store_true", help="Save topics to TOML and create .md files")
    parser.add_argument("--unsave", nargs="+", help="Remove topics from TOML (and delete .md files)")
    args = parser.parse_args()

    defaults = load_defaults(TOPICS_TOML_PATH)

    if args.edit:
        changed = False
        if args.default_input:
            defaults["input"] = os.path.expanduser(args.default_input)
            print(f"Default input set to: {defaults['input']}")
            changed = True
        if args.default_list:
            defaults["list"] = os.path.expanduser(args.default_list)
            print(f"Default list set to: {defaults['list']}")
            changed = True
        if args.default_topic_save:
            defaults["topic_save"] = os.path.expanduser(args.default_topic_save)
            print(f"Default topic save dir set to: {defaults['topic_save']}")
            changed = True
        if changed:
            save_defaults(TOPICS_TOML_PATH, defaults)
        else:
            print("Nothing to edit. Use --default-input, --default-list or --default-topic-save")
        return

    current_input_path = args.input or defaults.get("input")
    current_list_path = args.list or defaults.get("list")
    current_topic_save_path = defaults.get("topic_save")

    if args.sources:
        print(f"Current input file:     {current_input_path}")
        print(f"Current list file:      {current_list_path}")
        print(f"Current topic save dir: {current_topic_save_path}")

    topics_i = read_non_empty(current_input_path)
    topics_l = read_list_file(current_list_path)

    if not topics_i and not topics_l:
        print("Warning: both source files are empty or missing — nothing to save")
    elif not topics_i:
        print(f"Warning: input file is empty or missing: {current_input_path}")
    elif not topics_l:
        print(f"Warning: list file is empty or missing: {current_list_path}")

    if args.compare:
        diff_i = diff_lists(topics_i, topics_l)
        diff_l = diff_lists(topics_l, topics_i)
        if diff_i:
            print(f"Items in input but not in list ({len(diff_i)}):")
            print("\n".join(diff_i))
        if diff_l:
            print(f"Items in list but not in input ({len(diff_l)}):")
            print("\n".join(diff_l))
        if not diff_i and not diff_l:
            print("No differences found")

    topics = uniq_keep_order(topics_i + topics_l)

    if args.ab:
        sorted_topics = sorted(topics, key=str.casefold)
        if current_input_path:
            write_files(current_input_path, sorted_topics)
            sort_list_file(current_list_path)
            topics = sorted_topics

    if args.count:
        count_input = len(topics_i)
        count_list = len(topics_l)
        count_union_uniq = len(topics)
        count_common = len(set(topics_i) & set(topics_l))
        count_input_uniq = len(set(topics_i))
        count_list_uniq = len(set(topics_l))
        print(f"Union uniq topics: {count_union_uniq}")
        print(f"Common topics:     {count_common}")
        print()
        print(f"All input topics:  {count_input}")
        print(f"Input uniq topics: {count_input_uniq}")
        print()
        print(f"All list topics:   {count_list}")
        print(f"List uniq topics:  {count_list_uniq}")

    if args.show is not None:
        display = topics if args.show == -1 else topics[:args.show]
        for t in display:
            print(t)

    # =======================
    # Save topics to TOML + create .md
    # =======================
    if args.add_topic:
        if args.list_name:
            add_topics_to_list(args.add_topic, current_list_path, args.list_name)
        else:
            add_topics_to_input(args.add_topic, current_input_path)
        add_topics(args.add_topic, TOPICS_TOML_PATH, current_topic_save_path)

    if args.del_topic:
        del_topics(args.del_topic, TOPICS_TOML_PATH, current_input_path, current_list_path)

    if args.save:
        if current_topic_save_path:
            save_topics_to_toml(TOPICS_TOML_PATH, topics, current_topic_save_path)
        else:
            print("Error: topic_save path is not set")

    if args.unsave:
        del_topics(args.unsave, TOPICS_TOML_PATH, input_path=None, list_path=None)

    any_action = any([
        args.show is not None,
        args.count,
        args.ab,
        args.compare,
        args.sources,
        args.add_topic,
        args.del_topic,
        args.save,
        args.unsave,
    ])
    if not any_action:
        parser.print_help()


if __name__ == "__main__":
    main()
