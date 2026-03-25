#!/usr/bin/env python3

import argparse
import os

from config import TOPICS_TOML_PATH, load_defaults, save_defaults
from fileutils import (
    read_non_empty, read_list_file, uniq_keep_order,
    diff_lists, normalize_for_compare, normalize_topic,
    strip_link, extract_link, sort_list_file, write_files,
    paths_to_list, paths_to_str, read_list_lines, parse_section_name,slice_with_negative
)
from topics_store import (
    load_existing_topic_keys, save_topics_to_toml,
    del_topics, load_toml_topics, wipe_topics
)
from lists_store import (
    add_topics_to_input, add_topics_to_list, add_list, del_list,
    remove_from_list_section, read_list_sections, read_list_headers,
)
from links import set_add_link, del_add_link
from rename import rename_topic, rename_list
from reports import build_topic_distribution, search_topic, generate_source_table, search_saved


def main():
    parser = argparse.ArgumentParser(description="Topics tool")

    parser.add_argument("-i", "--input", nargs="+", help="Topics files (overrides default)")
    parser.add_argument("-l", "--list", nargs="+", help="Topic-lists files (overrides default)")
    parser.add_argument("--sh", "--show", dest="show", type=int, nargs='?', const=0,
            help="Show all or first N topics from inputs, lists (may use with --list-name, --pure)")
    parser.add_argument("--count", action="store_true", help="Show variety count of topics, lists")
    parser.add_argument("--ab", "--alphabetic", action="store_true",
            help="Sort topics alphabetically AND rewrite input/list files")
    parser.add_argument("--compare", action="store_true",
            help="Show differences between each input and list")
    parser.add_argument("--settings", action="store_true",
            help="Show current default settings of inputs, lists, source table, topic save dir")
    parser.add_argument("--edit", action="store_true", help="Edit settings mode")
    parser.add_argument("--default-editor", help="Set default editor command (used with --edit)")
    parser.add_argument("--editor", help="Editor command to use (overrides default for this run)")
    parser.add_argument("-w", "--write", metavar="TOPIC",
            help="Open (or create) a .unikey file for TOPIC in topic_save dir")
    parser.add_argument("-c", "--cast", metavar="TOPIC",
            help="Convert TOPIC's .unikey file via unikey.py into the format given by --format")
    parser.add_argument("-f", "--format", metavar="EXT",
            help="Output format/extension for --cast (e.g. md)")
    parser.add_argument("--auto-cast", choices=["true", "false"],
            help="Enable/disable auto cast after --write if file was modified")
    parser.add_argument("--auto-cast-format", metavar="EXT",
            help="Default format for auto cast (used with --edit)")
    parser.add_argument("-v", "--view", metavar="TOPIC",
            help="Open TOPIC's file in the viewer for the given format (requires -f)")
    parser.add_argument("--default-viewer", metavar="CMD",
            help="Set default viewer for a format (used with --edit and -f, --format)")
    parser.add_argument("--default-input", nargs="+", help="Set default input paths (used with --edit)")
    parser.add_argument("--default-list", nargs="+", help="Set default list paths (used with --edit)")
    parser.add_argument("--default-topic-save", help="Set default directory for topic files")
    parser.add_argument("--source-table-file", "--src-table-file", dest="source_table_file",
            help="Set default output path for source table (used with --edit)")
    parser.add_argument("--add-topic", nargs="+",
            help="Add topics to input file by default (or list with --list-name)")
    parser.add_argument("--list-name", nargs="+", help="Section names in using lists to add topics to")
    parser.add_argument("--del-topic", nargs="+", help="Delete topics from inputs, lists, toml save")
    parser.add_argument("--show-input", type=int, nargs='?', const=-1,
            help="Show all or first N topics from inputs")
    parser.add_argument("--add-list", nargs="+",
            help="Add new sections to first using list (for other use -l)")
    parser.add_argument("--del-list", nargs="+",
            help="Delete sections from first using list (for other use -l)")
    parser.add_argument("--force", action="store_true",
            help="Force operation without confirmation (use with --del-list")
    parser.add_argument("--show-lists", type=int, nargs='?', const=-1,
            help="Show all or first N using list section names")
    parser.add_argument("--pure", action="store_true",
    help="Disable section name headers in output (use with --show, --show-lists, --show-saved, --compare, --search, --search-saved")
    parser.add_argument("--search", help="Search topic across input and lists")
    parser.add_argument("--search-saved", help="Search topics in TOML by title, list, or link")
    parser.add_argument("--rename-topic", nargs=2, metavar=("OLD", "NEW"),
            help="Rename topic in using input, list and TOML")
    parser.add_argument("--rename-list", nargs=2, metavar=("OLD", "NEW"),
            help="Rename list section in using list files")
    parser.add_argument("--add-link",
            help="Topic name to set a link in lists for (requires --list-name, --link-look, --link)")
    parser.add_argument("--del-link",
            help="Topic name to remove link in lists from (requires --list-name)")
    parser.add_argument("--link", help="URL for the topic link (used with --add-link)")
    parser.add_argument("--link-look", help="Display text for the link (used with --add-link)")
    parser.add_argument("--save", nargs="*", metavar="TOPIC", help="Save topics to TOML (no args = all)")
    parser.add_argument("--unsave", nargs="+", help="Remove topics from TOML (and delete their files)")
    parser.add_argument("--wipe-save", action="store_true",
            help="Remove all topics from TOML (requires --force)")
    parser.add_argument("--show-save", action="store_true",
            help="Show topics that would be saved on --save")
    parser.add_argument("--show-saved", type=int, nargs="?", const=-1,
            help="Show saved topics from TOML (default: all)")
    parser.add_argument("--auto-ab", choices=["true", "false"],
            help="Enable/disable auto alphabetic sort on every run")
    parser.add_argument("--auto-save", choices=["true", "false"],
            help="Enable/disable auto save to TOML on every run")
    parser.add_argument("--source-table", "--src-table", dest="source_table", action="store_true",
            help="Generate markdown source table in default path (see --settings)")
    parser.add_argument("--show-source-table", "--show-src-table", dest="show_source_table",
            action="store_true", help="Open source table in md viewer")
    args = parser.parse_args()

    defaults = load_defaults(TOPICS_TOML_PATH)

    if args.edit:
        changed = False
        if args.default_input:
            defaults["input"] = paths_to_str([os.path.expanduser(p) for p in args.default_input])
            print(f"Default input set to: {defaults['input']}")
            changed = True
        if args.default_list:
            defaults["list"] = paths_to_str([os.path.expanduser(p) for p in args.default_list])
            print(f"Default list set to: {defaults['list']}")
            changed = True
        if args.default_topic_save:
            defaults["topic_save"] = os.path.expanduser(args.default_topic_save)
            print(f"Default topic save dir set to: {defaults['topic_save']}")
            changed = True
        if args.source_table_file:
            defaults["source_table_file"] = os.path.expanduser(args.source_table_file)
            print(f"Default source table file set to: {defaults['source_table_file']}")
            changed = True
        if args.default_editor:
            defaults["editor"] = args.default_editor
            print(f"Default editor set to: {defaults['editor']}")
            changed = True
        if args.auto_ab:
            defaults["auto_alphabetic_sort"] = args.auto_ab
            print(f"Auto alphabetic sort set to: {args.auto_ab}")
            changed = True
        if args.auto_save:
            defaults["auto_save"] = args.auto_save
            print(f"Auto save set to: {args.auto_save}")
            changed = True
        if args.auto_cast:
            defaults["auto_cast"] = args.auto_cast
            print(f"Auto cast set to: {args.auto_cast}")
            changed = True
        if args.auto_cast_format:
            defaults["auto_cast_format"] = args.auto_cast_format
            print(f"Auto cast format set to: {defaults['auto_cast_format']}")
            changed = True
        if args.default_viewer:
            if not args.format:
                print("Error: --default-viewer requires -f <format>")
            else:
                key = f"viewer_{args.format}"
                defaults[key] = args.default_viewer
                print(f"Default viewer for {args.format} set to: {args.default_viewer}")
                changed = True
        if changed:
            save_defaults(TOPICS_TOML_PATH, defaults)
        else:
            print("Nothing to edit. Use --default-input, --default-list, --default-topic-save, --default-editor, --default-viewer")
        return

    default_inputs = paths_to_list(defaults.get("input", ""))
    default_lists = paths_to_list(defaults.get("list", ""))
    current_input_paths = args.input or default_inputs
    current_list_paths = args.list or default_lists
    current_input_path = current_input_paths[0] if current_input_paths else None
    current_list_path = current_list_paths[0] if current_list_paths else None
    current_topic_save_path = defaults.get("topic_save")

    if args.settings:
        print(f"Input files:          {', '.join(current_input_paths)}")
        print(f"List files:           {', '.join(current_list_paths)}")
        print(f"Source table file:    {defaults.get('source_table_file', "")}")
        print(f"Topic save dir:       {current_topic_save_path}")
        print(f"Auto alphabetic sort: {defaults.get('auto_alphabetic_sort')}")
        print(f"Auto save:            {defaults.get('auto_save', 'false')}")
        print(f"Auto cast:            {defaults.get('auto_cast', 'false')}")
        print(f"Auto cast format:     {defaults.get('auto_cast_format', '')}")
        print(f"Editor:               {defaults.get('editor', '')}")
        for k, v in defaults.items():
                    if k.startswith("viewer_"):
                        fmt = k[len("viewer_"):]
                        print(f"Viewer ({fmt}):          {v}")
        print(f"Last saved:           {defaults.get('last_saved', "")}")

    topics_i = uniq_keep_order([t for p in current_input_paths for t in read_non_empty(p)])
    topics_l = uniq_keep_order([t for p in current_list_paths for t in read_list_file(p)])

    for p in current_input_paths:
        if not os.path.isfile(p):
            print(f"Warning: input file missing: {p}")
    for p in current_list_paths:
        if not os.path.isfile(p):
            print(f"Warning: list file missing: {p}")
    if not topics_i and not topics_l:
        print("Warning: both source files are empty or missing — nothing to save")

    if args.rename_topic:
        rename_topic(
            args.rename_topic[0], args.rename_topic[1],
            TOPICS_TOML_PATH, current_input_paths, current_list_paths,
            args.list_name,
        )

    if args.rename_list:
        rename_list(args.rename_list[0], args.rename_list[1], current_list_paths)

    if args.add_link:
        missing = []
        if not args.list_name:
            missing.append("--list-name")
        if not args.link_look:
            missing.append("--link-look")
        if not args.link:
            missing.append("--link")
        if missing:
            print(f"Error: --add-link requires: {', '.join(missing)}")
        else:
            set_add_link(args.add_link, current_list_paths, args.list_name, args.link, args.link_look)

    if args.del_link:
        if not args.list_name:
            print("Error: --del-link requires: --list-name")
        else:
            del_add_link(args.del_link, current_list_paths, args.list_name)

    if args.compare:
        all_files = (
            [(p, "input", read_non_empty(p)) for p in current_input_paths] +
            [(p, "list", read_list_file(p)) for p in current_list_paths]
        )
        for i, (p1, t1_type, t1) in enumerate(all_files):
            for p2, t2_type, t2 in all_files[i + 1:]:
                diff_1 = diff_lists(t1, t2)
                diff_2 = diff_lists(t2, t1)
                if not args.pure:
                    print(f"\n[{p1} ({t1_type})] vs [{p2} ({t2_type})]")
                if diff_1:
                    if not args.pure:
                        print(f"  Only in {p1} ({len(diff_1)}):")
                    for t in diff_1:
                        print(f"    {t}" if not args.pure else t)
                if diff_2:
                    if not args.pure:
                        print(f"  Only in {p2} ({len(diff_2)}):")
                    for t in diff_2:
                        print(f"    {t}" if not args.pure else t)
                if not diff_1 and not diff_2:
                    if not args.pure:
                        print("  No differences found")

    topics = uniq_keep_order(topics_i + topics_l)
    auto_ab = defaults.get("auto_alphabetic_sort", "false") == "true"

    if args.ab or auto_ab:
        sorted_topics = sorted(topics, key=str.casefold)
        for p in current_input_paths:
            file_topics = read_non_empty(p)
            write_files(p, sorted(file_topics, key=str.casefold))
        for p in current_list_paths:
            sort_list_file(p)
        topics = sorted_topics

    if args.count:
        all_input_topics = [t for p in current_input_paths for t in read_non_empty(p)]
        count_input = len(all_input_topics)
        count_list = len(topics_l)
        norm_i = {normalize_for_compare(t) for t in topics_i}
        norm_l = {normalize_for_compare(t) for t in topics_l}
        count_common = len(norm_i & norm_l)
        count_input_uniq = len(norm_i)
        count_list_uniq = len(norm_l)

        list_link_topics = set()
        for lp in current_list_paths:
            for line in read_list_lines(lp):
                stripped = line.strip()
                if stripped and extract_link(stripped)[1] is not None:
                    list_link_topics.add(strip_link(stripped))

        union_clean = set(strip_link(t) for t in topics)

        print(f"Union uniq topics: {len(union_clean)}")
        print(f"Common topics:     {count_common}")
        print()
        print(f"All input topics:  {count_input}")
        print(f"Input uniq topics: {count_input_uniq}")
        print()
        print(f"All list topics:   {count_list}")
        print(f"List uniq topics:  {count_list_uniq}")
        print(f"List link topics:  {len(list_link_topics)}")

    if args.show is not None:
        dist = build_topic_distribution(topics_i, current_list_paths)
        if args.list_name:
            show_topics = []
            for lp in current_list_paths:
                show_topics += read_list_sections(lp, args.list_name)
            show_topics = uniq_keep_order(show_topics)
        else:
            show_topics = topics_i
        if args.show !=0:
            show_topics = slice_with_negative(show_topics, args.show)
        seen = set()
        for t in show_topics:
            norm = normalize_for_compare(t)
            if norm in seen:
                continue
            seen.add(norm)
            data = dist.get(norm)
            title = strip_link(t) if not data else data["title"]
            if args.pure:
                print(title)
            else:
                if args.list_name:
                    shown_sections = [s for s in (data["sections"] if data else []) if s in args.list_name]
                    src = ", ".join(shown_sections) if shown_sections else ", ".join(args.list_name)
                elif data:
                    parts = []
                    if data["in_input"]:
                        parts.append("input")
                    if data["sections"]:
                        parts.extend(data["sections"])
                    src = ", ".join(parts) if parts else "—"
                else:
                    src = "—"
                print(f"{title}  [{src}]")

    if args.show_saved is not None:
        saved = load_toml_topics(TOPICS_TOML_PATH)
        display = slice_with_negative(saved, args.show_saved)
        for t in display:
            if args.pure:
                print(t["title"])
            else:
                parts = []
                for sl in t.get("lists", []):
                    sec = sl["list"]
                    url = sl.get("link")
                    link_look = sl.get("link_look")
                    if url:
                        display_text = link_look if link_look else t["title"]
                        parts.append(f"{sec} [{display_text}]({url})")
                    else:
                        parts.append(sec)
                lists_str = ", ".join(parts) if parts else "—"
                print(f"\n{t['title']} [path: {t['path']}] \n[lists: {lists_str}]")

    if args.search:
        for lp in current_list_paths:
            search_topic(args.search, topics_i, lp, args.pure)

    if args.search_saved:
        search_saved(args.search_saved, TOPICS_TOML_PATH, pure=args.pure)

    if args.add_topic:
        if args.list_name:
            if current_list_path:
                for section in args.list_name:
                    add_topics_to_list(args.add_topic, current_list_path, section)
        else:
            if current_input_path:
                add_topics_to_input(args.add_topic, current_input_path)

    if args.del_topic:
        if args.list_name:
            keys_to_del = {normalize_topic(t.strip('"')) for t in args.del_topic}
            titles_to_del = {t.strip('"') for t in args.del_topic}
            for section in args.list_name:
                for lp in current_list_paths:
                    remove_from_list_section(lp, section, keys_to_del, titles_to_del)
        else:
            del_topics(
                args.del_topic,
                TOPICS_TOML_PATH,
                input_paths=current_input_paths,
                list_paths=current_list_paths,
            )

    if args.show_input is not None:
        if not topics_i:
            print("Input file is empty or missing")
        else:
            display = slice_with_negative(topics_i, args.show_input)
            print(f"Input topics ({len(display)}/{len(topics_i)}):")
            for t in display:
                print(f"  {t}")

    if args.add_list:
        for section in args.add_list:
            add_list(section, current_list_path)

    if args.del_list:
        for section in args.del_list:
            del_list(section, current_list_path, force=args.force)

    if args.show_lists is not None:
        headers = read_list_headers(current_list_path)
        if not headers:
            print("No lists found")
        else:
            display = slice_with_negative(headers, args.show_lists)
            if args.pure:
                for h in display:
                    print(h)
            else:
                print(f"Lists ({len(display)}/{len(headers)}):")
                for h in display:
                    print(f"  {h}")

    auto_save = defaults.get("auto_save", "false") == "true"

    if args.save is not None or auto_save:
        if current_topic_save_path:
            if args.save:
                topics_to_save = [
                    t for t in topics
                    if strip_link(t) in args.save
                    or normalize_topic(strip_link(t)) in {normalize_topic(s) for s in args.save}
                ]
            else:
                topics_to_save = topics
            save_topics_to_toml(
                TOPICS_TOML_PATH, topics_to_save, current_topic_save_path,
                input_topics=topics_i, list_paths=current_list_paths,
            )
        else:
            print("Error: topic_save path is not set")

    if args.unsave:
        del_topics(args.unsave, TOPICS_TOML_PATH, input_path=None, list_path=None)

    if args.wipe_save:
        if not args.force:
            print("Error: --wipe-save requires --force")
        else:
            wipe_topics(TOPICS_TOML_PATH)

    if args.show_save:
        existing = load_existing_topic_keys(TOPICS_TOML_PATH)
        input_set = set(topics_i)

        topic_lists: dict = {}
        for lp in current_list_paths:
            lines = read_list_lines(lp)
            current_section = None
            seen_in_section: set = set()
            for line in lines:
                section_name = parse_section_name(line)
                if section_name is not None:
                    current_section = section_name
                elif line.strip() and current_section:
                    plain = strip_link(line.strip())
                    key = (plain, current_section)
                    if key not in seen_in_section:
                        seen_in_section.add(key)
                        topic_lists.setdefault(plain, [])
                        if current_section not in topic_lists[plain]:
                            topic_lists[plain].append(current_section)

        seen_keys: dict = {}
        for t in topics:
            key = normalize_topic(strip_link(t))
            if key in existing:
                continue
            if key not in seen_keys or extract_link(t)[1] is not None:
                seen_keys[key] = t
        new_topics = list(seen_keys.values())

        if not new_topics:
            print("Nothing to save — all topics already in TOML")
        else:
            print(f"Would be saved ({len(new_topics)}):")
            for t in new_topics:
                clean = strip_link(t)
                parts = []
                if clean in input_set:
                    parts.append("input")
                if clean in topic_lists:
                    parts.extend(topic_lists[clean])
                src = ", ".join(parts) if parts else "unknown"
                print(f"  {clean}  [{src}]")

    if args.source_table:
        out_path = defaults.get("source_table_file")
        if not out_path:
            print("Error: source_table_file is not set. Use --edit --source-table-file <path>")
        else:
            generate_source_table(TOPICS_TOML_PATH, out_path, topic_save=current_topic_save_path or "")

    if args.show_source_table:
            src_table_path = defaults.get("source_table_file")
            viewer = defaults.get("viewer_md")
            if not src_table_path:
                print("Error: source_table_file is not set. Use --edit --source-table-file <path>")
            elif not viewer:
                print("Error: no viewer set for md. Use --edit --default-viewer <cmd> -f md")
            elif not os.path.exists(src_table_path):
                print(f"Error: source table file not found: {src_table_path}. Run --source-table first")
            else:
                import subprocess
                subprocess.Popen([viewer, src_table_path])

    if args.write:
            import subprocess
            import sys
            import threading
            import time
            topic_save = defaults.get("topic_save")
            if not topic_save:
                print("Error: topic_save path is not set. Use --edit --default-topic-save <path>")
            else:
                os.makedirs(topic_save, exist_ok=True)
                key = normalize_topic(args.write)
                unikey_path = os.path.join(topic_save, f"{key}.unikey")
                if not os.path.exists(unikey_path):
                    open(unikey_path, "w", encoding="utf-8").close()
                    print(f"Created: {unikey_path}")
                else:
                    print(f"Opening: {unikey_path}")
                editor = args.editor or defaults.get("editor") or os.environ.get("EDITOR") or os.environ.get("VISUAL")
                if not editor:
                    print(f"Error: no editor set. Use --editor <cmd> or --edit --default-editor <cmd>")
                else:
                    messages = []

                    def do_cast():
                        out_path = os.path.join(topic_save, f"{key}.{fmt}")
                        unikey_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "unikey.py")
                        with open(unikey_path, "r", encoding="utf-8") as fh:
                            unikey_input = fh.read()
                        result = subprocess.run(
                            [sys.executable, unikey_script, "-f", fmt],
                            input=unikey_input, capture_output=True, text=True,
                        )
                        if result.returncode != 0:
                            messages.append(f"Error: unikey.py failed:\n{result.stderr.strip()}")
                        else:
                            action = "Updated" if os.path.exists(out_path) else "Created"
                            with open(out_path, "w", encoding="utf-8") as fh:
                                fh.write(result.stdout)
                            messages.append(f"{action}: {out_path}")

                    fmt = args.format or defaults.get("auto_cast_format")
                    auto_cast = defaults.get("auto_cast") == "true" and fmt
                    stop_event = threading.Event()

                    def watch():
                        last = os.path.getmtime(unikey_path) if os.path.exists(unikey_path) else 0
                        while not stop_event.is_set():
                            time.sleep(1)
                            cur = os.path.getmtime(unikey_path) if os.path.exists(unikey_path) else 0
                            if cur != last:
                                last = cur
                                do_cast()

                    if auto_cast:
                        t = threading.Thread(target=watch, daemon=True)
                        t.start()

                    subprocess.call([editor, unikey_path])

                    if auto_cast:
                        stop_event.set()
                        for msg in messages:
                            print(msg)

    if args.cast:
        import subprocess
        import sys
        topic_save = defaults.get("topic_save")
        fmt = args.format or defaults.get("auto_cast_format")
        if not fmt:
            print("Error: --cast requires --format <ext> or --auto-cast-format to be set")

        elif not topic_save:
            print("Error: topic_save path is not set. Use --edit --default-topic-save <path>")
        else:
            key = normalize_topic(args.cast)
            unikey_path = os.path.join(topic_save, f"{key}.unikey")
            if not os.path.exists(unikey_path):
                print(f"Error: file not found: {unikey_path}")
            else:
                out_path = os.path.join(topic_save, f"{key}.{fmt}")
                unikey_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "unikey.py")
                with open(unikey_path, "r", encoding="utf-8") as f:
                    unikey_input = f.read()
                result = subprocess.run(
                    [sys.executable, unikey_script, "-f", fmt],
                    input=unikey_input, capture_output=True, text=True,
                )
                if result.returncode != 0:
                    print(f"Error: unikey.py failed:\n{result.stderr.strip()}")
                else:
                    action = "Updated" if os.path.exists(out_path) else "Created"
                    with open(out_path, "w", encoding="utf-8") as f:
                        f.write(result.stdout)
                    print(f"{action}: {out_path}")

    if args.view:
            import subprocess
            topic_save = defaults.get("topic_save")
            fmt = args.format or defaults.get("auto_cast_format")
            if not fmt:
                print("Error: --view requires -f <format> or --auto-cast-format to be set")
            elif not topic_save:
                print("Error: topic_save path is not set.")
            else:
                key = normalize_topic(args.view)
                file_path = os.path.join(topic_save, f"{key}.{fmt}")
                if not os.path.exists(file_path):
                    print(f"Error: file not found: {file_path}")
                else:
                    viewer = defaults.get(f"viewer_{fmt}")
                    if not viewer:
                        print(f"Error: no viewer set for format '{fmt}'. Use --edit --default-viewer <cmd> -f {args.format}")
                    else:
                        subprocess.Popen([viewer, file_path])

    any_action = any([
        args.show is not None,
        args.count,
        args.ab,
        args.rename_topic,
        args.rename_list,
        args.add_link,
        args.del_link,
        args.compare,
        args.settings,
        args.search,
        args.search_saved,
        args.add_topic,
        args.del_topic,
        args.show_input is not None,
        args.add_list,
        args.del_list,
        args.show_lists is not None,
        args.save is not None,
        args.unsave,
        args.wipe_save,
        args.show_save,
        args.show_saved is not None,
        args.source_table,
        args.show_source_table,
        args.editor,
        args.write,
        args.cast,
        args.view,
    ])
    if not any_action:
        parser.print_help()


if __name__ == "__main__":
    main()
