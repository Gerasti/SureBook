import os
import re
from typing import List, Optional, Tuple


def read_non_empty(path: str) -> List[str]:
    if not os.path.isfile(path):
        return []
    with open(path, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def read_list_file(path: str) -> List[str]:
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


def write_files(path: str, items: List[str]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for i in items:
            f.write(i + "\n")


def read_list_lines(path: Optional[str]) -> List[str]:
    if not path or not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return f.readlines()


def uniq_keep_order(items: List[str]) -> List[str]:
    return list(dict.fromkeys(items))


def normalize_topic(name: str) -> str:
    return re.sub(r"\s+", "_", name.strip())


def normalize_for_compare(topic: str) -> str:
    """Normalize topic for comparisons (ignores links, case, spacing)."""
    return normalize_topic(strip_link(topic)).casefold()


def diff_lists(list1: List[str], list2: List[str]) -> List[str]:
    norm2 = {normalize_for_compare(x) for x in list2}
    return [x for x in list1 if normalize_for_compare(x) not in norm2]


def paths_to_list(val: str) -> List[str]:
    return [os.path.expanduser(p.strip()) for p in val.split(":") if p.strip()]


def paths_to_str(paths: List[str]) -> str:
    return ":".join(paths)


def strip_link(topic: str) -> str:
    """Remove markdown link from topic, keeping only the topic name."""
    return re.sub(r'\s+\[.*?\]\(.*?\)', '', topic).strip()


def extract_link(topic: str) -> Tuple[Optional[str], Optional[str]]:
    """Extract (link_look, url) from topic with markdown link, or (None, None)."""
    m = re.search(r'\[([^\]]+)\]\(([^)]+)\)', topic)
    if m:
        return m.group(1), m.group(2)
    return None, None


def is_topic_duplicate(line: str, existing_lines: List[str]) -> bool:
    """True if plain topic already exists in lines (with or without link)."""
    norm = normalize_for_compare(line)
    for ln in existing_lines:
        if normalize_for_compare(ln) == norm:
            return True
    return False


def parse_section_name(line: str) -> Optional[str]:
    stripped = line.strip()
    if stripped.startswith("##") and stripped.endswith("list:"):
        return stripped[3:-6].strip()
    return None


def find_section_header(lines: List[str], section: str) -> bool:
    header = f"## {section} list:"
    return any(line.strip() == header for line in lines)


def sort_list_file(path: Optional[str]) -> None:
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


def print_section(name: str, items: List[str], pure: bool = False) -> None:
    if not pure:
        print(f"\n[{name}] ({len(items)}):")
    for t in items:
        print(f"  {t}" if not pure else t)
