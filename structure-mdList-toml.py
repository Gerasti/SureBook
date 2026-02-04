#!/usr/bin/env python3
import argparse
import re
import locale

# =======================
# Locale initialization
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
# MD -> internal dict
# =======================

def parse_md(md_path):
    data = {}
    current_category = None

    with open(md_path, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue

            # level 0
            if re.match(r"^- ", line):
                current_category = line[2:].strip()
                data[current_category] = []

            # level 1
            elif re.match(r"^\s+- ", line) and current_category:
                topic = line.strip()[2:].strip()
                data[current_category].append(topic)

    return data


# =======================
# TOML -> internal dict
# =======================

def parse_toml(toml_path):
    data = {}
    current_category = None
    in_topics = False

    with open(toml_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            if line.startswith("[") and line.endswith("]"):
                current_category = line[1:-1]
                data[current_category] = []
                in_topics = False

            elif line.startswith("topics"):
                in_topics = True

            elif in_topics:
                if line == "]":
                    in_topics = False
                else:
                    data[current_category].append(line.strip('",'))

    return data


# =======================
# Sorting
# =======================

def sort_data(data, sort_tags=False, sort_topics=False):
    key_fn = locale.strxfrm

    items = data.items()
    if sort_tags:
        items = sorted(items, key=lambda x: key_fn(x[0]))

    result = {}
    for category, topics in items:
        if sort_topics:
            topics = sorted(topics, key=key_fn)
        result[category] = topics

    return result


# =======================
# Writers
# =======================

def write_toml(data, out_path):
    with open(out_path, "w", encoding="utf-8") as f:
        for category, topics in data.items():
            f.write(f"[{category}]\n")
            f.write("topics = [\n")
            for t in topics:
                t = t.replace('"', '\\"')
                f.write(f'    "{t}",\n')
            f.write("]\n\n")


def write_md(data, out_path):
    with open(out_path, "w", encoding="utf-8") as f:
        for category, topics in data.items():
            f.write(f"- {category}\n")
            for t in topics:
                f.write(f"\t- {t}\n")
            f.write("\n")


# =======================
# CLI
# =======================

def main():
    parser = argparse.ArgumentParser(
        description="Convert or sort Markdown <-> TOML (topics based)"
    )

    parser.add_argument("--md-f", "--markdown-file", dest="md_file")
    parser.add_argument("--toml-f", "--toml-file", dest="toml_file")

    parser.add_argument(
        "--ab-tag", "--alphabet-tag",
        action="store_true",
        help="Sort level-0 categories alphabetically"
    )

    parser.add_argument(
        "--ab-topic", "--alphabet-topic",
        action="store_true",
        help="Sort level-1 topics alphabetically"
    )

    parser.add_argument(
        "--en", "--english",
        action="store_true",
        help="Use English alphabetical order (default)"
    )

    parser.add_argument(
        "--ru", "--russian",
        action="store_true",
        help="Use Russian alphabetical order"
    )

    parser.add_argument(
        "--inplace",
        action="store_true",
        help="Keep input format (md->md or toml->toml), only sort"
    )

    parser.add_argument(
        "-o", "--output",
        help="Output file (optional with --inplace)"
    )

    args = parser.parse_args()

    if args.md_file and args.toml_file:
        raise SystemExit("Use only one of --md-f or --toml-f")

    if not args.md_file and not args.toml_file:
        raise SystemExit("Specify --md-f or --toml-f")

    # Parse input
    if args.md_file:
        data = parse_md(args.md_file)
    else:
        data = parse_toml(args.toml_file)

    # Init locale only if sorting requested
    if args.ab_tag or args.ab_topic:
        init_locale(use_ru=args.ru)

    # Sort
    data = sort_data(
        data,
        sort_tags=args.ab_tag,
        sort_topics=args.ab_topic
    )

    # Determine output path
    if args.inplace:
        if args.md_file:
            output_path = args.output or args.md_file
        else:
            output_path = args.output or args.toml_file
    else:
        if not args.output:
            raise SystemExit("--output is required unless --inplace is used")
        output_path = args.output

    # Write result
    if args.md_file:
        if args.inplace:
            write_md(data, output_path)
            print(f"Renew {args.md_file}")
        else:
            write_toml(data, output_path)
            print(f"Create {args.md_file}")
    else:
        if args.inplace:
            write_toml(data, output_path)
            print(f"Renew {args.toml_file}")
        else:
            write_md(data, output_path)
            print(f"Create {args.toml_file}")


if __name__ == "__main__":
    main()
