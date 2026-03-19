import os
from typing import Dict, List

from fileutils import (
    normalize_for_compare, strip_link, extract_link,
    parse_section_name, read_list_lines, print_section,
)
from topics_store import load_toml_topics
from config import load_defaults


def build_topic_distribution(topics_i: List[str], list_paths: List[str]) -> Dict[str, Dict]:
    """Return mapping: normalized_topic -> {title, in_input, sections[]}"""
    dist: Dict[str, Dict] = {}

    for t in topics_i:
        norm = normalize_for_compare(t)
        dist.setdefault(norm, {
            "title": strip_link(t),
            "in_input": False,
            "sections": [],
        })
        dist[norm]["in_input"] = True

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
                norm = normalize_for_compare(plain)
                dist.setdefault(norm, {
                    "title": plain,
                    "in_input": False,
                    "sections": [],
                })
                if current_section not in dist[norm]["sections"]:
                    dist[norm]["sections"].append(current_section)

    return dist


def search_topic(
    query: str,
    topics_i: List[str],
    list_path: str,
    solid: bool = False,
) -> None:
    query_lower = query.casefold()
    matches_input = [t for t in topics_i if query_lower in normalize_for_compare(t)]
    if matches_input:
        print_section("input", matches_input, solid)

    if not os.path.exists(list_path):
        return

    lines = read_list_lines(list_path)
    current_section = None
    section_matches: Dict[str, List[str]] = {}

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


def generate_source_table(toml_path: str, out_path: str) -> None:
    topics = load_toml_topics(toml_path)
    defaults = load_defaults(toml_path)
    last_saved = defaults.get("last_saved", "")

    lines = []
    if last_saved:
        lines.append(f"> last saved: {last_saved}\n")
    lines.append("| № | Topic | Sources (lists + links) |")
    lines.append("|---|-------|-------------------------|")

    for i, t in enumerate(topics, 1):
        title = t["title"]
        sources_parts = []
        for sl in t.get("lists", []):
            sec = sl["list"]
            url = sl.get("link")
            link_look = sl.get("link_look")
            if url:
                display = link_look if link_look else title
                sources_parts.append(f"{sec} [{display}]({url})")
            else:
                sources_parts.append(sec)
        sources = ", ".join(sources_parts) if sources_parts else ""
        lines.append(f"| {i} | {title} | {sources} |")

    action = "renewed" if os.path.exists(out_path) else "created"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Source table {action}: {out_path} ({len(topics)} topics)")
