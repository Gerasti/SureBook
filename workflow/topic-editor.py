#!/usr/bin/env python3

import argparse
import os
import sys
import locale

DEFAULT_INPUT = os.path.expanduser("~/surebook/info/topics.md")
DEFAULT_LIST = os.path.expanduser("~/surebook/info/topic-lists.md")


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
# Parsers
# =======================

def read_non_empty(path: str) -> list[str]:
    if not os.path.isfile(path):
        return []

    result = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                result.append(line)
    return result


def read_list_file(path: str) -> list[str]:
    if not os.path.isfile(path):
        return []

    result = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.endswith("list:"):
                continue
            result.append(line)
    return result


# =======================
# Utils
# =======================

def uniq_keep_order(items: list[str]) -> list[str]:
    return list(dict.fromkeys(items))


def write_files(path: str, items: list[str]):
    with open(path, "w", encoding="utf-8") as f:
        for i in items:
            f.write(i + "\n")


# =======================
# CLI
# =======================

def main():
    parser = argparse.ArgumentParser(
        description="Topics tool"
    )

    parser.add_argument(
        "-i", "--input",
        help=f"Topics file (default: {DEFAULT_INPUT})"
    )

    parser.add_argument(
        "-l", "--list",
        help=f"Topic-lists file (default: {DEFAULT_LIST})"
    )

    parser.add_argument(
        "--sh", "--show",
        dest="show",
        type=int,
        nargs='?',
        const=-1,
        help="Show first N topics (default: show all)"
    )

    parser.add_argument(
        "--count",
        action="store_true",
        help="Show count of topics"
    )

    parser.add_argument(
        "--ab",
        action="store_true",
        help="Sort topics alphabetically AND rewrite input file"
    )

    parser.add_argument(
        "--ru",
        action="store_true",
        help="Russian locale"
    )

    parser.add_argument(
        "--en",
        action="store_true",
        help="English locale (default)"
    )
    args = parser.parse_args()

    topics = []
    files_to_rewrite = []

    current_input_path = DEFAULT_INPUT
    current_list_path = DEFAULT_LIST

    if args.input and args.list:
        current_input_path = args.input
        current_list_path = args.list
    elif args.input:
        current_input_path = args.input
        current_list_path = None
    elif args.list:
        current_input_path = None
        current_list_path = args.list

    topics_i = read_non_empty(current_input_path) if current_input_path else []
    topics_l = read_list_file(current_list_path) if current_list_path else []

    topics = uniq_keep_order(topics_i + topics_l)

    if args.ab:
        for path in (current_input_path, current_list_path):
            if path:
                write_files(path, topics)


    if args.count:
        print(len(topics))
        return


    if args.show is not None:
        if args.show != -1:
            topics = topics[:args.show]
        for t in topics:
            print(t)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
