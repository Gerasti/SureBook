#!/usr/bin/env python3
"""Tests for topic_editor.py functions."""

import os
import sys
import tempfile
import shutil

sys.path.insert(0, os.path.dirname(__file__))
from topic_editor import (
    strip_link, extract_link,
    normalize_topic, parse_section_name, find_section_header,
    read_list_lines, read_non_empty, write_files,
    uniq_keep_order, diff_lists, paths_to_list, paths_to_str,
    add_topics_to_input, add_topics_to_list, add_list, del_list,
    read_list_sections, read_list_headers,
    rename_topic, rename_list,
    set_add_link, del_add_link,
    load_list_topics_with_sections, load_list_links_by_section,
    load_toml_topics,
)

def is_topic_duplicate(line: str, existing_lines: list) -> bool:
    plain = strip_link(line.strip())
    for l in existing_lines:
        if strip_link(l.strip()) == plain:
            return True
    return False

PASS = "\033[92m✓\033[0m"
FAIL = "\033[91m✗\033[0m"

results = {"pass": 0, "fail": 0}

def check(name: str, actual, expected):
    if actual == expected:
        print(f"  {PASS} {name}")
        results["pass"] += 1
    else:
        print(f"  {FAIL} {name}")
        print(f"      expected: {expected!r}")
        print(f"      actual:   {actual!r}")
        results["fail"] += 1

def section(title: str):
    print(f"\n── {title}")


# =======================
# Helpers
# =======================
section("strip_link")
check("plain topic unchanged",        strip_link("nginx"), "nginx")
check("removes link",                 strip_link("nginx [nginx](https://x.com)"), "nginx")
check("removes link with long look",  strip_link("bind DNS [bind DNS && more](https://x.com)"), "bind DNS")
check("multiple spaces before link",  strip_link("nginx  [nginx](https://x.com)"), "nginx")

section("extract_link")
check("no link → (None, None)",        extract_link("nginx"), (None, None))
check("extracts look and url",         extract_link("nginx [doc](https://x.com)"), ("doc", "https://x.com"))
check("look differs from topic name",  extract_link("bind DNS [DNS guide](https://x.com)"), ("DNS guide", "https://x.com"))

section("is_topic_duplicate")
check("exact match",           is_topic_duplicate("nginx", ["nginx", "chrony"]), True)
check("linked vs plain",       is_topic_duplicate("nginx [doc](https://x.com)", ["nginx"]), True)
check("plain vs linked",       is_topic_duplicate("nginx", ["nginx [doc](https://x.com)"]), True)
check("no match",              is_topic_duplicate("nginx", ["chrony", "bind DNS"]), False)

section("normalize_topic")
check("spaces to underscores", normalize_topic("bind DNS"), "bind_DNS")
check("multiple spaces",       normalize_topic("bind  DNS"), "bind_DNS")
check("strips whitespace",     normalize_topic("  nginx  "), "nginx")

section("parse_section_name")
check("valid header",          parse_section_name("## sysahelper list:"), "sysahelper")
check("with spaces",           parse_section_name("## my list list:"), "my list")
check("not a header",          parse_section_name("nginx"), None)
check("missing ##",            parse_section_name("# sysahelper list:"), None)
check("missing list:",         parse_section_name("## sysahelper"), None)

section("uniq_keep_order")
check("removes dupes keeps order", uniq_keep_order(["a", "b", "a", "c"]), ["a", "b", "c"])
check("empty list",                uniq_keep_order([]), [])

section("diff_lists")
check("returns difference",    diff_lists(["a", "b", "c"], ["b"]), ["a", "c"])
check("empty when equal",      diff_lists(["a"], ["a"]), [])
check("all different",         diff_lists(["a"], ["b"]), ["a"])

section("paths_to_list / paths_to_str")
check("single path",           paths_to_list("/a/b"), ["/a/b"])
check("two paths",             paths_to_list("/a/b:/c/d"), ["/a/b", "/c/d"])
check("strips spaces",         paths_to_list("/a/b : /c/d"), ["/a/b", "/c/d"])
check("str round-trip",        paths_to_str(paths_to_list("/a:/b:/c")), "/a:/b:/c")


# =======================
# File operations (use temp dir)
# =======================
tmpdir = tempfile.mkdtemp()

def tmp(name): return os.path.join(tmpdir, name)

INPUT = tmp("input.md")
LIST  = tmp("lists.md")
TOML  = tmp("topics.toml")

# Seed input file
write_files(INPUT, ["nginx", "chrony", "bind DNS"])

section("read_non_empty / write_files")
check("reads written content", read_non_empty(INPUT), ["nginx", "chrony", "bind DNS"])
check("missing file → []",     read_non_empty(tmp("nope.md")), [])

section("add_topics_to_input")
add_topics_to_input(["wireguard"], INPUT)
check("appends new topic",     read_non_empty(INPUT), ["nginx", "chrony", "bind DNS", "wireguard"])
add_topics_to_input(["nginx"], INPUT)
check("skips existing topic",  read_non_empty(INPUT), ["nginx", "chrony", "bind DNS", "wireguard"])

# Seed list file
with open(LIST, "w") as f:
    f.write("## sysahelper list:\nnginx\n\nchrony\n\n## notesk list:\nbind DNS\n\n")

section("read_list_headers")
check("reads headers",         read_list_headers(LIST), ["sysahelper", "notesk"])

section("read_list_sections")
check("reads section content", read_list_sections(LIST, ["sysahelper"]), ["nginx", "chrony"])
check("reads multiple secs",   read_list_sections(LIST, ["sysahelper", "notesk"]), ["nginx", "chrony", "bind DNS"])
check("missing section → []",  read_list_sections(LIST, ["nope"]), [])

section("find_section_header")
lines = read_list_lines(LIST)
check("finds existing",        find_section_header(lines, "sysahelper"), True)
check("missing → False",       find_section_header(lines, "nope"), False)

section("add_list")
add_list("newlist", LIST)
check("header added",          "newlist" in read_list_headers(LIST), True)
add_list("newlist", LIST)  # duplicate — should skip
check("duplicate skipped",     read_list_headers(LIST).count("newlist"), 1)

section("add_topics_to_list — new section")
LIST2 = tmp("lists2.md")
with open(LIST2, "w") as f:
    f.write("## sysahelper list:\nnginx\n\n")
add_topics_to_list(["wireguard"], LIST2, "sysahelper")
check("appends to existing",   "wireguard" in read_list_sections(LIST2, ["sysahelper"]), True)
add_topics_to_list(["nginx"], LIST2, "sysahelper")
check("skips plain duplicate", read_list_sections(LIST2, ["sysahelper"]).count("nginx"), 1)
add_topics_to_list(["nginx [doc](https://x.com)"], LIST2, "sysahelper")
check("skips linked duplicate of plain", read_list_sections(LIST2, ["sysahelper"]).count("nginx"), 1)

section("del_list — empty section")
LIST3 = tmp("lists3.md")
with open(LIST3, "w") as f:
    f.write("## empty list:\n## sysahelper list:\nnginx\n\n")
del_list("empty", LIST3)
check("empty section deleted", "empty" not in read_list_headers(LIST3), True)
check("other section intact",  "sysahelper" in read_list_headers(LIST3), True)

section("set_add_link")
LIST4 = tmp("lists4.md")
with open(LIST4, "w") as f:
    f.write("## sysahelper list:\nnginx\n\nchrony\n\n")
set_add_link("nginx", [LIST4], ["sysahelper"], "https://nginx.org", "nginx docs")
content = read_list_sections(LIST4, ["sysahelper"])
check("link set on topic",     any("https://nginx.org" in t for t in content), True)
# overwrite existing link
set_add_link("nginx", [LIST4], ["sysahelper"], "https://nginx.org/new", "new docs")
content = read_list_sections(LIST4, ["sysahelper"])
check("link overwritten",      any("https://nginx.org/new" in t for t in content), True)
check("only one nginx entry",  sum(1 for t in content if "nginx" in t), 1)

section("del_add_link")
del_add_link("nginx", [LIST4], ["sysahelper"])
content = read_list_sections(LIST4, ["sysahelper"])
check("link removed",          any("[" in t and "nginx" in t for t in content), False)
check("plain topic remains",   "nginx" in content, True)

section("rename_topic in list")
LIST5 = tmp("lists5.md")
with open(LIST5, "w") as f:
    f.write("## sysahelper list:\nnginx\n\nchrony\n\n")
TOML5 = tmp("topics5.toml")
with open(TOML5, "w") as f:
    f.write('[topics]\n\n[topics."nginx"]\ntitle = "nginx"\npath = "/tmp/nginx.md"\n')
rename_topic("nginx", "nginx proxy", TOML5, [], [LIST5])
check("renamed in list",       "nginx proxy" in read_list_sections(LIST5, ["sysahelper"]), True)
check("old name gone from list", "nginx" not in read_list_sections(LIST5, ["sysahelper"]), True)

section("rename_topic in TOML")
with open(TOML5) as f:
    toml_content = f.read()
check("key renamed in TOML",   '[topics."nginx_proxy"]' in toml_content, True)
check("title renamed in TOML", 'title = "nginx proxy"' in toml_content, True)

section("rename_topic — duplicate removal")
LIST6 = tmp("lists6.md")
with open(LIST6, "w") as f:
    f.write("## sysahelper list:\nnginx\n\nnginx proxy\n\n")
rename_topic("nginx", "nginx proxy", TOML5, [], [LIST6])
content = read_list_sections(LIST6, ["sysahelper"])
check("duplicate removed",     content.count("nginx proxy"), 1)
check("old name gone",         "nginx" not in content, True)

section("rename_list — simple")
LIST7 = tmp("lists7.md")
with open(LIST7, "w") as f:
    f.write("## old list:\nnginx\n\nchrony\n\n")
rename_list("old", "new", [LIST7])
check("new header present",    "new" in read_list_headers(LIST7), True)
check("old header gone",       "old" not in read_list_headers(LIST7), True)
check("topics preserved",      read_list_sections(LIST7, ["new"]), ["nginx", "chrony"])

section("rename_list — merge")
LIST8 = tmp("lists8.md")
with open(LIST8, "w") as f:
    f.write("## target list:\nexisting\n\n## source list:\nnew1\n\nexisting\n\nnew2\n\n")
rename_list("source", "target", [LIST8])
check("merged into target",    "new1" in read_list_sections(LIST8, ["target"]), True)
check("new2 merged",           "new2" in read_list_sections(LIST8, ["target"]), True)
check("existing not duped",    read_list_sections(LIST8, ["target"]).count("existing"), 1)
check("source section removed", "source" not in read_list_headers(LIST8), True)

section("load_list_topics_with_sections")
LIST9 = tmp("lists9.md")
with open(LIST9, "w") as f:
    f.write("## a list:\nnginx\n\nchrony\n\n## b list:\nnginx\n\nbind DNS\n\n")
ts = load_list_topics_with_sections([LIST9])
check("nginx in two sections", sorted(ts.get("nginx", [])), ["a", "b"])
check("chrony in one section", ts.get("chrony"), ["a"])
check("no dupes from repeat",  ts.get("nginx", []).count("a"), 1)

section("load_list_links_by_section")
LIST10 = tmp("lists10.md")
with open(LIST10, "w") as f:
    f.write("## sysahelper list:\nnginx [nginx docs](https://nginx.org)\n\nchrony\n\n")
ll = load_list_links_by_section([LIST10])
check("link extracted",        ll.get(("nginx", "sysahelper")), ("nginx docs", "https://nginx.org"))
check("no link for chrony",    ("chrony", "sysahelper") not in ll, True)

section("load_toml_topics")
TOML2 = tmp("topics2.toml")
with open(TOML2, "w") as f:
    f.write('[topics]\n\n[topics."nginx"]\ntitle = "nginx"\npath = "/tmp/nginx.md"\nlink = "https://nginx.org"\nlink-look = "nginx docs"\n\n[topics."chrony"]\ntitle = "chrony"\npath = "/tmp/chrony.md"\n')
tt = load_toml_topics(TOML2)
check("loads two topics",      len(tt), 2)
check("title correct",         tt[0]["title"], "nginx")
check("link loaded",           tt[0]["link"], "https://nginx.org")
check("link-look loaded",      tt[0]["link_look"], "nginx docs")
check("no link for chrony",    tt[1]["link"], None)

# =======================
# Cleanup
# =======================
shutil.rmtree(tmpdir)

# =======================
# Summary
# =======================
total = results["pass"] + results["fail"]
print(f"\n{'='*40}")
print(f"Results: {results['pass']}/{total} passed", end="")
if results["fail"]:
    print(f"  ({results['fail']} failed)")
else:
    print(" ✓")
