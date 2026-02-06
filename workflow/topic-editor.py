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
    seen = set()
    result = []
    for i in items:
        if i not in seen:
            seen.add(i)
            result.append(i)
    return result


def write_file(path: str, items: list[str]):
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
        default=DEFAULT_INPUT,
        dest="input",
        help=f"Topics file (default: {DEFAULT_INPUT})"
    )

    parser.add_argument(
        "-l", "--list",
        default=DEFAULT_LIST,
        help=f"Topic-lists file (default: {DEFAULT_LIST})"
    )

    parser.add_argument(
        "--sh", "--show",
        dest="show",
        type=int,
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
#    if args.input:
    topics_i = read_non_empty(args.input)

#    if args.list:
    topics_l = read_list_file(args.list)

    if topics_i or topics_l:
        if topics_i and topics_l: 
            topics = uniq_keep_order(topics_i + topics_l)

    if args.ab:
        init_locale(use_ru=args.ru)
        topics = sorted(topics, key=locale.strxfrm)
        write_file(args.input, topics)

    if args.count:
        print(len(topics))
        return

    if args.show is not None:
        topics = topics[:args.show]

#    for t in topics:
#        print(t)


if __name__ == "__main__":
    main()
