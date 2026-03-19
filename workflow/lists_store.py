import os
from typing import List, Optional, Set

from fileutils import (
    normalize_for_compare, normalize_topic, strip_link,
    parse_section_name, find_section_header,
    read_list_lines, is_topic_duplicate,
)


def add_topics_to_input(topics_to_add: List[str], input_path: str) -> None:
    from fileutils import read_non_empty
    existing = read_non_empty(input_path)
    existing_norm = {normalize_for_compare(t) for t in existing}
    new = [t for t in topics_to_add if normalize_for_compare(t) not in existing_norm]
    if not new:
        print("Topics already exist in input, skipping")
        return
    with open(input_path, "a", encoding="utf-8") as f:
        for t in new:
            f.write(t + "\n")
            print(f"Added to input: {t}")


def add_topics_to_list(topics_to_add: List[str], list_path: str, section: str) -> None:
    lines = read_list_lines(list_path)
    header = f"## {section} list:"
    section_found = find_section_header(lines, section)

    if not section_found:
        with open(list_path, "a", encoding="utf-8") as f:
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


def remove_from_list_file(
    path: Optional[str],
    keys_to_del: Set[str],
    titles_to_del: Set[str],
) -> None:
    if not path:
        return
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            new_lines.append(line)
            continue
        norm = normalize_for_compare(stripped)
        if norm in {normalize_for_compare(t) for t in titles_to_del}:
            if new_lines and new_lines[-1].strip() == "":
                new_lines.pop()
            continue
        new_lines.append(line)

    with open(path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)


def remove_from_list_section(
    list_path: Optional[str],
    section: str,
    keys_to_del: Set[str],
    titles_to_del: Set[str],
) -> None:
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
            print(f"Deleted: {strip_link(stripped)}  [list:{section} ({list_path})]")
            continue
        new_lines.append(line)

    with open(list_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)


def add_list(section: str, list_path: Optional[str]) -> None:
    if not list_path:
        return
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


def del_list(section: str, list_path: Optional[str], force: bool = False) -> bool:
    if not list_path:
        return False
    lines = read_list_lines(list_path)
    if not lines:
        return False

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
        return False

    if topics_in_section:
        print(f"List [{section}] contains {len(topics_in_section)} topics:")
        for t in topics_in_section:
            print(f"  {t}")
        if not force:
            print("Error: use --force to delete non-empty list")
            return False

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
    return True


def read_list_sections(path: Optional[str], sections: List[str]) -> List[str]:
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


def read_list_headers(path: Optional[str]) -> List[str]:
    lines = read_list_lines(path)
    result = []
    for line in lines:
        section_name = parse_section_name(line)
        if section_name is not None:
            result.append(section_name)
    return result
