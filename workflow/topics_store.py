import os
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

from fileutils import (
    normalize_topic, normalize_for_compare, strip_link, extract_link,
    read_non_empty, write_files, parse_section_name, read_list_lines,
)
from config import update_toml_paths_key


def load_existing_topic_keys(toml_path: str) -> Set[str]:
    """Return the set of topic keys already present in the TOML file."""
    existing: Set[str] = set()
    if not os.path.exists(toml_path):
        return existing
    with open(toml_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith('[topics."'):
                key = line.split('"')[1]
                existing.add(key)
    return existing


def load_toml_topics(toml_path: str) -> List[Dict]:
    """Load all topics from TOML as list of dicts: key, title, path, lists."""
    import re
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
            current = {"key": key, "title": "", "path": "", "lists": []}
        elif current is not None and "=" in stripped:
            k, v = stripped.split("=", 1)
            k = k.strip()
            v = v.strip()
            if k == "title":
                current["title"] = v.strip('"')
            elif k == "path":
                current["path"] = v.strip('"')
            elif k == "lists":
                current["lists"] = []
                for m in re.finditer(r'\{([^}]+)\}', v):
                    entry = {}
                    for pair in m.group(1).split(","):
                        if "=" in pair:
                            ek, ev = pair.split("=", 1)
                            entry[ek.strip()] = ev.strip().strip('"')
                    if "list" in entry:
                        current["lists"].append(entry)
    if current is not None:
        topics.append(current)
    return topics

def load_list_links_by_section(list_paths: List[str]) -> Dict[Tuple[str, str], Tuple[Optional[str], Optional[str]]]:
    """Return dict: (topic_title, section) -> (link_look, url)."""
    result: Dict[Tuple[str, str], Tuple[Optional[str], Optional[str]]] = {}
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


def save_topics_to_toml(
    toml_path: str,
    topics: List[str],
    base_dir: str,
    input_topics: Optional[List[str]] = None,
    list_paths: Optional[List[str]] = None,
) -> None:
    from datetime import datetime

    existing = load_existing_topic_keys(toml_path)

    lines = []
    if os.path.exists(toml_path):
        with open(toml_path, encoding="utf-8") as f:
            lines = f.read().splitlines()

    topic_sections: Dict[str, List[str]] = {}
    topic_links_by_section: Dict[Tuple[str, str], Tuple[Optional[str], Optional[str]]] = {}
    if list_paths:
        topic_sections = load_list_topics_with_sections(list_paths)
        topic_links_by_section = load_list_links_by_section(list_paths)

    seen_keys: Dict[str, str] = {}
    for t in topics:
        key = normalize_topic(strip_link(t))
        if key in existing:
            continue
        if key not in seen_keys or extract_link(t)[1] is not None:
            seen_keys[key] = t

    new_topics = list(seen_keys.values())
    if not new_topics:
        print("Nothing to save — all topics already in TOML")
        return

    os.makedirs(base_dir, exist_ok=True)

    with open(toml_path, "a", encoding="utf-8") as f:
        if "[topics]" not in "\n".join(lines):
            f.write("\n[topics]\n")

        for topic in new_topics:
            clean_topic = strip_link(topic)
            link_look, link_url = extract_link(topic)
            key = normalize_topic(clean_topic)
            md_path = os.path.join(base_dir, f"{key}.md")

            sections = topic_sections.get(clean_topic, [])

            section_links = []
            for sec in sections:
                ll, url = topic_links_by_section.get((clean_topic, sec), (None, None))
                if url:
                    entry: Dict = {"list": sec, "link": url}
                    if ll and ll != clean_topic:
                        entry["link_look"] = ll
                    section_links.append(entry)
                else:
                    section_links.append({"list": sec})

            f.write(f'\n[topics."{key}"]\n')
            f.write(f'title = "{clean_topic}"\n')
            f.write(f'path = "{md_path}"\n')
            if section_links:
                parts = []
                for sl in section_links:
                    kv_pairs = [f'list = "{sl["list"]}"']
                    if "link" in sl:
                        kv_pairs.append(f'link = "{sl["link"]}"')
                    if "link_look" in sl:
                        kv_pairs.append(f'link_look = "{sl["link_look"]}"')
                    parts.append("{" + ", ".join(kv_pairs) + "}")
                f.write(f'lists = [{", ".join(parts)}]\n')
            else:
                f.write('lists = []\n')

            if not os.path.exists(md_path):
                Path(md_path).touch()
            print(f"Saved: {clean_topic}")

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    update_toml_paths_key(toml_path, "last_saved", now_str)
    print(f"Total saved: {len(new_topics)}")

def del_topics(
    topics_to_del: List[str],
    toml_path: str,
    input_path: Optional[str] = None,
    list_path: Optional[str] = None,
    input_paths: Optional[List[str]] = None,
    list_paths: Optional[List[str]] = None,
) -> None:
    all_input_paths = list(input_paths or ([input_path] if input_path else []))
    all_list_paths  = list(list_paths  or ([list_path]  if list_path  else []))

    if not topics_to_del or not os.path.exists(toml_path):
        return

    keys_to_del   = {normalize_topic(t.strip('"')) for t in topics_to_del}
    titles_to_del = {t.strip('"') for t in topics_to_del}

    def canonical(name: str) -> str:
        if name in titles_to_del:
            return name
        return next((t for t in titles_to_del if normalize_topic(t) == normalize_topic(name)), name)

    # --- 1. scan what exists where ---
    sources: Dict[str, List[str]] = {t: [] for t in titles_to_del}

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

    toml_titles: Dict[str, str] = {}
    lines_to_skip: Set[int] = set()
    for idx, (start, key, title) in enumerate(section_starts):
        if key not in keys_to_del and title not in titles_to_del:
            continue
        toml_titles[key] = title
        c = canonical(title)
        sources[c].append(toml_path)
        for j in range(start + 1, start + 4):
            if j < len(lines) and lines[j].strip().startswith("path"):
                md_path = lines[j].split("=", 1)[1].strip().strip('"')
                if os.path.exists(md_path):
                    sources[c].append(f"{md_path}")
                break
        end = section_starts[idx + 1][0] if idx + 1 < len(section_starts) else len(lines)
        for j in range(start, end):
            lines_to_skip.add(j)

    for ip in all_input_paths:
        if not os.path.exists(ip):
            continue
        for t in read_non_empty(ip):
            if t in titles_to_del or normalize_topic(t) in keys_to_del:
                c = canonical(t)
                label = f"input ({ip})"
                if label not in sources[c]:
                    sources[c].append(label)

    for lp in all_list_paths:
        if not os.path.exists(lp):
            continue
        current_section = None
        for line in read_list_lines(lp):
            sn = parse_section_name(line)
            if sn is not None:
                current_section = sn
                continue
            stripped = line.strip()
            if not stripped or not current_section:
                continue
            plain = strip_link(stripped)
            if plain in titles_to_del or normalize_topic(plain) in keys_to_del:
                c = canonical(plain)
                label = ("list", lp, current_section)
                if label not in sources[c]:
                    sources[c].append(label)

    # --- 2. delete ---
    new_lines = [line for i, line in enumerate(lines) if i not in lines_to_skip]
    with open(toml_path, "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines) + "\n")

    for key in toml_titles:
        for i, line in enumerate(lines):
            if line.startswith(f'[topics."{key}"]'):
                for j in range(i + 1, min(i + 4, len(lines))):
                    if lines[j].strip().startswith("path"):
                        md_path = lines[j].split("=", 1)[1].strip().strip('"')
                        if os.path.exists(md_path):
                            os.remove(md_path)
                        break
                break

    for ip in all_input_paths:
        if not os.path.exists(ip):
            continue
        write_files(ip, [
            t for t in read_non_empty(ip)
            if t not in titles_to_del and normalize_topic(t) not in keys_to_del
        ])

    from lists_store import remove_from_list_file
    for lp in all_list_paths:
        remove_from_list_file(lp, keys_to_del, titles_to_del)

    # --- 3. report ---
    def fmt_sources(srcs):
        parts = []
        # non-list entries first (strings)
        for s in srcs:
            if isinstance(s, str):
                parts.append(s)
        # list entries: group sections by file
        from collections import defaultdict
        by_file = defaultdict(list)
        for s in srcs:
            if isinstance(s, tuple) and s[0] == "list":
                _, lp, sec = s
                by_file[lp].append(sec)
        for lp, secs in by_file.items():
            parts.append(f"list:{', '.join(secs)} ({lp})")
        return ', '.join(parts)

    for topic in topics_to_del:
        t = topic.strip('"')
        srcs = sources.get(t, [])
        if srcs:
            print(f"Deleted: {t}  [{fmt_sources(srcs)}]")
        else:
            print(f"Not found: {t}")

def wipe_topics(toml_path: str) -> None:
    if not os.path.exists(toml_path):
        return
    with open(toml_path, encoding="utf-8") as f:
        lines = f.readlines()
    new_lines = []
    skip = False
    for line in lines:
        if line.strip() == "[topics]":
            skip = True
            continue
        if skip and line.strip().startswith("[") and not line.strip().startswith('[topics."'):
            skip = False
        if not skip:
            new_lines.append(line)
    with open(toml_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    print(f"Wiped all topics from {toml_path}")
