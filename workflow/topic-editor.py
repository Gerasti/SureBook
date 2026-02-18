#!/usr/bin/env python3

import argparse
import os
import locale
import re
from pathlib import Path

TOPICS_TOML_PATH = os.path.expanduser("~/surebook/info/topics.toml")

# =======================
# Locale
# =======================
def init_locale(use_ru: bool):
    locales = (
        ("ru_RU.UTF-8", "ru_RU.utf8") if use_ru
        else ("en_US.UTF-8", "en_US.utf8")
    )
    for loc in locales:
        try:
            locale.setlocale(locale.LC_COLLATE, loc)
            return
        except locale.Error:
            continue
    locale.setlocale(locale.LC_COLLATE, "C")


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
            if not line or line.endswith("list:"):
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
    with open(toml_path, "w", encoding="utf-8") as f:
        f.write("[paths]\n")
        for k, v in defaults.items():
            f.write(f'{k} = "{v}"\n')


# =======================
# Save Topics to TOML + MD
# =======================
def save_topics_to_toml(toml_path: str, topics: list[str], base_dir: str):
    existing = set()
    lines = []

    if os.path.exists(toml_path):
        with open(toml_path, encoding="utf-8") as f:
            lines = f.read().splitlines()
            for l in lines:
                if l.startswith('[topics."'):
                    existing.add(l.split('"')[1])

    with open(toml_path, "a", encoding="utf-8") as f:
        if "[topics]" not in "\n".join(lines):
            f.write("\n[topics]\n")

        os.makedirs(base_dir, exist_ok=True)

        for topic in topics:
            key = normalize_topic(topic)
            if key in existing:
                continue

            md_path = os.path.join(base_dir, f"{key}.md")

            f.write(f'\n[topics."{key}"]\n')
            f.write(f'title = "{topic}"\n')
            f.write(f'path = "{md_path}"\n')

            if not os.path.exists(md_path):
                Path(md_path).touch()

# Adding and remove
def add_topics(topics_to_add: list[str], toml_path: str, base_dir: str):
    if not topics_to_add:
        return

    existing = {}
    lines = []
    if os.path.exists(toml_path):
        with open(toml_path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
            section = None
            key = None
            for l in lines:
                if l.startswith("[") and l.endswith("]"):
                    section = l[1:-1].strip()
                    if section.startswith("topics."):
                        key = section.split('"')[1]
                elif section and section.startswith("topics.") and "=" in l:
                    k, v = l.split("=", 1)
                    existing[key] = v

    os.makedirs(base_dir, exist_ok=True)

    with open(toml_path, "a", encoding="utf-8") as f:
        if "[topics]" not in "\n".join(lines):
            f.write("\n[topics]\n")

        for topic in topics_to_add:
            topic = topic.strip('"')
            key = normalize_topic(topic)
            if key in existing:
                continue
            md_path = os.path.join(base_dir, f"{key}.md")
            f.write(f'\n[topics."{key}"]\n')
            f.write(f'title = "{topic}"\n')
            f.write(f'path = "{md_path}"\n')
            Path(md_path).touch()


def del_topics(topics_to_del: list[str], toml_path: str):
    if not topics_to_del or not os.path.exists(toml_path):
        return

    with open(toml_path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    new_lines = []
    skip = 0
    for i, line in enumerate(lines):
        if line.startswith("[topics."):
            key = line.split('"')[1]
            title_line_index = i + 1
            title_line = lines[title_line_index] if title_line_index < len(lines) else ""
            title = title_line.split("=",1)[1].strip().strip('"') if "=" in title_line else ""
            if key in [normalize_topic(t.strip('"')) for t in topics_to_del] or title in topics_to_del:
                skip = 3
                md_path_line = lines[i+2] if i+2 < len(lines) else ""
                md_path = md_path_line.split("=",1)[1].strip().strip('"') if "=" in md_path_line else None
                if md_path and os.path.exists(md_path):
                    os.remove(md_path)
                continue
        if skip > 0:
            skip -= 1
            continue
        new_lines.append(line)

    with open(toml_path, "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines) + "\n")



# =======================
# CLI
# =======================
def main():
    parser = argparse.ArgumentParser(description="Topics tool")

    parser.add_argument("-i", "--input", help="Topics file (overrides default)")
    parser.add_argument("-l", "--list", help="Topic-lists file (overrides default)")
    parser.add_argument("--sh", "--show", dest="show", type=int, nargs='?', const=-1, help="Show first N topics (default: all)")
    parser.add_argument("--count", action="store_true", help="Show count of topics")
    parser.add_argument("--ab", action="store_true", help="Sort topics alphabetically AND rewrite input/list")
    parser.add_argument("--ru", action="store_true", help="set Russian locale (used with --edit)")
    parser.add_argument("--en", action="store_true", help="set English locale (default; used with --edit)")
    parser.add_argument("--compare", action="store_true", help="Show differences between input and list")
    parser.add_argument("--sources", action="store_true", help="Show current input and list files")
    parser.add_argument("--edit", action="store_true", help="Edit default paths")
    parser.add_argument("--default-input", help="Set new default input path (used with --edit)")
    parser.add_argument("--default-list", help="Set new default list path (used with --edit)")
    parser.add_argument("--default-topic-save", help="Set default directory for topic markdown files")
    parser.add_argument("--add-topic", nargs="+", help="Add topics to topics.toml")
    parser.add_argument("--del-topic", nargs="+", help="Delete topics from topics.toml")

    args = parser.parse_args()
    init_locale(args.ru)

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
    current_topic_save_path = args.list or defaults.get("topic_save")

    if args.sources:
        print(f"Current input file: {current_input_path}")
        print(f"Current list file: {current_list_path}")
        print(f"Current topic save dir: {current_topic_save_path}")

    topics_i = read_non_empty(current_input_path)
    topics_l = read_list_file(current_list_path)

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
        for path in (current_input_path, current_list_path):
            if path:
                write_files(path, topics)

    if args.count:
        count_input = len(topics_i)
        count_list = len(topics_l)
        count_union_uniq = len(topics)
        print(f"Union uniq topics: {count_union_uniq}")
        print(f"Input topics:  {count_input}")
        print(f"List topics:   {count_list}")

    if args.show is not None:
        display = topics if args.show == -1 else topics[:args.show]
        for t in display:
            print(t)

    # =======================
    # Save topics to TOML + create .md
    # =======================
    default_save = defaults.get("topic_save")
    if args.add_topic:
        add_topics(args.add_topic, TOPICS_TOML_PATH, default_save)

    if args.del_topic:
        del_topics(args.del_topic, TOPICS_TOML_PATH)

    if default_save:
        save_topics_to_toml(TOPICS_TOML_PATH, topics, default_save)

    if not (args.show or args.count or args.ab or args.compare or args.sources or args.add_topic or args.del_topic):
        parser.print_help()


if __name__ == "__main__":
    main()
