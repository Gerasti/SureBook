import os
from typing import Dict

TOPICS_TOML_PATH = os.path.expanduser("~/surebook/info/topics.toml")

_DEFAULTS_TEMPLATE = {
    "input": os.path.expanduser("~/surebook/info/topics.md"),
    "list": os.path.expanduser("~/surebook/info/topic-lists.md"),
    "topic_save": os.path.expanduser("~/surebook/topics"),
    "source_table_file": os.path.expanduser("~/surebook/info/source-table.md"),
    "auto_alphabetic_sort": "false",
    "auto_save": "false",
}


def load_defaults(toml_path: str) -> Dict:
    defaults = {}
    updated = False
    section = None

    if os.path.exists(toml_path):
        try:
            with open(toml_path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if line.startswith("[") and line.endswith("]"):
                        section = line[1:-1].strip()
                        continue
                    if "=" in line and section == "paths":
                        key, val = line.split("=", 1)
                        defaults[key.strip()] = os.path.expanduser(val.strip().strip('"'))
        except Exception:
            pass
    else:
        updated = True

    for k, v in _DEFAULTS_TEMPLATE.items():
        if k not in defaults:
            defaults[k] = v
            updated = True

    if updated:
        save_defaults(toml_path, defaults)

    return defaults


def save_defaults(toml_path: str, defaults: Dict) -> None:
    os.makedirs(os.path.dirname(toml_path), exist_ok=True)
    other_lines = []
    if os.path.exists(toml_path):
        with open(toml_path, encoding="utf-8") as f:
            in_paths = False
            for line in f:
                stripped = line.strip()
                if stripped == "[paths]":
                    in_paths = True
                    continue
                if in_paths and stripped.startswith("["):
                    in_paths = False
                if not in_paths:
                    other_lines.append(line)

    with open(toml_path, "w", encoding="utf-8") as f:
        f.write("[paths]\n")
        for k, v in defaults.items():
            f.write(f'{k} = "{v}"\n')
        if other_lines:
            f.write("\n")
            f.writelines(other_lines)


def update_toml_paths_key(toml_path: str, key: str, value: str) -> None:
    """Insert or update a key in the [paths] section of the TOML file."""
    if not os.path.exists(toml_path):
        return
    with open(toml_path, encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    in_paths = False
    key_written = False

    for line in lines:
        stripped = line.strip()
        if stripped == "[paths]":
            in_paths = True
            new_lines.append(line)
            continue
        if in_paths and stripped.startswith("[") and stripped != "[paths]":
            if not key_written:
                new_lines.append(f'{key} = "{value}"\n')
                key_written = True
            in_paths = False
        if in_paths and stripped.startswith(f"{key} ="):
            new_lines.append(f'{key} = "{value}"\n')
            key_written = True
            continue
        new_lines.append(line)

    if not key_written:
        new_lines.append(f'{key} = "{value}"\n')

    with open(toml_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
