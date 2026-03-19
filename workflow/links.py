from typing import List, Optional

from fileutils import (
    strip_link, extract_link, parse_section_name, read_list_lines,
)
from lists_store import read_list_headers


def set_add_link(
    topic: str,
    list_paths: List[str],
    list_names: Optional[List[str]],
    link: str,
    link_look: Optional[str] = None,
) -> None:
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

    if list_names:
        all_headers = [h for p in list_paths for h in read_list_headers(p)]
        for name in list_names:
            if name not in all_headers:
                print(f"List not found: {name}")

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


def del_add_link(
    topic: str,
    list_paths: List[str],
    list_names: Optional[List[str]],
) -> None:
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

    if list_names:
        all_headers = [h for p in list_paths for h in read_list_headers(p)]
        for name in list_names:
            if name not in all_headers:
                print(f"List not found: {name}")
