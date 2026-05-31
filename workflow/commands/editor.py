"""Editor command for simple CLI."""

import os
import sys
import subprocess
import threading
import time
from typing import List, Dict, Any
from .base import Command
from repositories import ConfigRepository
from fileutils import normalize_topic
from file_manager import FileManager


class EditorCommand(Command):
    """Edit and manage topic files."""

    def __init__(self, config_repo: ConfigRepository):
        self.config_repo = config_repo

    def help(self) -> str:
        """Return help text for editor command."""
        return """Editor command - manage topic files

Usage:
  write <topic>         Open/create .unikey file
  cast <topic>          Convert .unikey to format
  cast force            Convert all .unikey files to format
  view <topic>          View converted file
  cat <topic>           Show file content
  work <topic>          Write and view (write + view)
  help                  Show this help

Flags:
  format <ext>          Specify format (for cast/view)
  force                 Convert all .unikey files (for cast)

Examples:
  write "Python"                # Open .unikey file
  cast "Python" format md       # Convert to markdown
  cast force format wikitext    # Convert all files to wikitext
  view "Python" format md       # View markdown file
  cat "Python" format md        # Show file content
  work "Python" format md       # Write and view
"""

    def execute(self, args: List[str], flags: Dict[str, Any]) -> int:
        """Execute editor command.

        Usage:
            write <topic>       - Open/create .unikey file
            cast <topic>        - Convert .unikey to format
            view <topic>        - View converted file
            cat <topic>         - Show file content
            work <topic>        - Write and view
        """
        if args and args[0] == "help" and not flags.get('force'):
            print(self.help())
            return 0

        if not args:
            return self.error("editor requires subcommand: write, cast, view, cat, work")

        subcommand = args[0]

        if subcommand in ["write", "edit", "w"]:
            return self._write(args[1:], flags)
        elif subcommand in ["cast", "convert", "c"]:
            return self._cast(args[1:], flags)
        elif subcommand in ["view", "v"]:
            return self._view(args[1:], flags)
        elif subcommand in ["cat"]:
            return self._cat(args[1:], flags)
        elif subcommand in ["work", "wk"]:
            return self._work(args[1:], flags)
        else:
            return self.error(f"Unknown editor subcommand: {subcommand}")

    def _write(self, args: List[str], flags: Dict[str, Any]) -> int:
        """Open topic file in editor."""
        if args and args[0] == "help" and not flags.get('force'):
            print(self.help())
            return 0

        if not args:
            return self.error("write requires: <topic>")

        topic = args[0]
        settings = self.config_repo.get_settings()

        if not settings.topic_save:
            return self.error("topic_save not set")

        FileManager.ensure_dir(settings.topic_save)
        key = normalize_topic(topic)
        unikey_path = FileManager.join(settings.topic_save, f"{key}.unikey")

        if not FileManager.exists(unikey_path):
            FileManager.write_text(unikey_path, "")
            print(f"Created: {unikey_path}")
        else:
            print(f"Opening: {unikey_path}")

        editor = settings.editor or os.environ.get("EDITOR") or os.environ.get("VISUAL")
        if not editor:
            return self.error("No editor set. Use 'config editor <cmd>' or set EDITOR env var")

        # Auto-cast setup
        fmt = flags.get("format") or settings.auto_cast_format
        auto_cast = settings.auto_cast and fmt

        messages = []
        stop_event = threading.Event()
        cast_done = {"flag": False}

        def do_cast():
            """Perform cast operation."""
            out_path = FileManager.join(settings.topic_save, f"{key}.{fmt}")
            unikey_script = FileManager.join(
                os.path.dirname(os.path.abspath(__file__)), "..", "unikey.py"
            )

            with open(unikey_path, "r", encoding="utf-8") as fh:
                unikey_input = fh.read()

            result = subprocess.run(
                [sys.executable, unikey_script, "-f", fmt],
                input=unikey_input,
                capture_output=True,
                text=True,
            )

            if result.returncode != 0:
                msg = f"Error: unikey.py failed:\n{result.stderr.strip()}"
                messages.append(msg)
            else:
                action = "Updated" if FileManager.exists(out_path) else "Created"
                with open(out_path, "w", encoding="utf-8") as fh:
                    fh.write(result.stdout)
                msg = f"{action}: {out_path}"
                # Store message but don't print yet (editor is still open)
                if not cast_done["flag"]:
                    messages.append(msg)
                    cast_done["flag"] = True

        def watch():
            """Watch file for changes and auto-cast."""
            last = os.path.getmtime(unikey_path) if FileManager.exists(unikey_path) else 0
            while not stop_event.is_set():
                time.sleep(1)
                cur = os.path.getmtime(unikey_path) if FileManager.exists(unikey_path) else 0
                if cur != last:
                    last = cur
                    do_cast()

        if auto_cast:
            t = threading.Thread(target=watch, daemon=True)
            t.start()

        try:
            subprocess.call([editor, unikey_path])
        except FileNotFoundError:
            return self.error(f"Editor not found: {editor}")
        except Exception as e:
            return self.error(f"Failed to launch editor '{editor}': {e}")

        if auto_cast:
            stop_event.set()
            # Perform final cast after editor closes
            if FileManager.exists(unikey_path):
                do_cast()
            # Print messages after editor is closed
            for msg in messages:
                print(msg)

        return 0

    def _cast(self, args: List[str], flags: Dict[str, Any]) -> int:
        """Convert .unikey file to format."""
        if args and args[0] == "help" and not flags.get('force'):
            print(self.help())
            return 0

        settings = self.config_repo.get_settings()
        fmt = flags.get("format") or settings.auto_cast_format
        if not fmt:
            return self.error("Format not specified. Use 'cast <topic> format <ext>'")

        if not settings.topic_save:
            return self.error("topic_save not set")

        # Mass conversion with force flag
        if flags.get('force') and not args:
            unikey_files = FileManager.list_files(settings.topic_save, pattern="*.unikey")
            if not unikey_files:
                print("No .unikey files found")
                return 0

            unikey_script = FileManager.join(
                os.path.dirname(os.path.abspath(__file__)), "..", "unikey.py"
            )

            success_count = 0
            error_count = 0

            for unikey_path in unikey_files:
                key = FileManager.splitext(FileManager.basename(unikey_path))[0]
                out_path = FileManager.join(settings.topic_save, f"{key}.{fmt}")

                try:
                    with open(unikey_path, "r", encoding="utf-8") as f:
                        unikey_input = f.read()

                    result = subprocess.run(
                        [sys.executable, unikey_script, "-f", fmt],
                        input=unikey_input,
                        capture_output=True,
                        text=True,
                    )

                    if result.returncode != 0:
                        print(f"Error converting {key}: {result.stderr.strip()}")
                        error_count += 1
                        continue

                    with open(out_path, "w", encoding="utf-8") as f:
                        f.write(result.stdout)

                    success_count += 1
                except Exception as e:
                    print(f"Error converting {key}: {e}")
                    error_count += 1

            print(f"\nConverted {success_count} files to .{fmt} format")
            if error_count > 0:
                print(f"Failed: {error_count} files")
            return 0

        # Single file conversion
        if not args:
            return self.error("cast requires: <topic>")

        topic = args[0]
        key = normalize_topic(topic)
        unikey_path = FileManager.join(settings.topic_save, f"{key}.unikey")

        if not FileManager.exists(unikey_path):
            return self.error(f"File not found: {unikey_path}")

        out_path = FileManager.join(settings.topic_save, f"{key}.{fmt}")
        unikey_script = FileManager.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "unikey.py"
        )

        with open(unikey_path, "r", encoding="utf-8") as f:
            unikey_input = f.read()

        result = subprocess.run(
            [sys.executable, unikey_script, "-f", fmt],
            input=unikey_input,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            return self.error(f"unikey.py failed:\n{result.stderr.strip()}")

        action = "Updated" if FileManager.exists(out_path) else "Created"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(result.stdout)

        print(f"{action}: {out_path}")
        return 0

    def _view(self, args: List[str], flags: Dict[str, Any]) -> int:
        """View converted file."""
        if args and args[0] == "help" and not flags.get('force'):
            print(self.help())
            return 0

        if not args:
            return self.error("view requires: <topic>")

        topic = args[0]
        settings = self.config_repo.get_settings()

        fmt = flags.get("format") or settings.auto_cast_format
        if not fmt:
            return self.error("Format not specified. Use 'view <topic> format <ext>'")

        if not settings.topic_save:
            return self.error("topic_save not set")

        key = normalize_topic(topic)
        file_path = FileManager.join(settings.topic_save, f"{key}.{fmt}")

        if not FileManager.exists(file_path):
            return self.error(f"File not found: {file_path}")

        viewer = settings.viewers.get(fmt)
        if not viewer:
            return self.error(f"No viewer set for format '{fmt}'. Use 'config viewer {fmt} <cmd>'")

        # Split viewer command if it contains arguments
        import shlex
        viewer_cmd = shlex.split(viewer) + [file_path]
        subprocess.Popen(viewer_cmd)
        print(f"Opened: {file_path}")
        return 0

    def _cat(self, args: List[str], flags: Dict[str, Any]) -> int:
        """Show file content."""
        if args and args[0] == "help" and not flags.get('force'):
            print(self.help())
            return 0

        if not args:
            return self.error("cat requires: <topic>")

        topic = args[0]
        settings = self.config_repo.get_settings()

        fmt = flags.get("format") or settings.auto_cast_format
        if not fmt:
            return self.error("Format not specified. Use 'cat <topic> format <ext>'")

        if not settings.topic_save:
            return self.error("topic_save not set")

        key = normalize_topic(topic)
        file_path = FileManager.join(settings.topic_save, f"{key}.{fmt}")

        if not FileManager.exists(file_path):
            return self.error(f"File not found: {file_path}")

        content = FileManager.read_text(file_path)
        print(content)
        return 0

    def _work(self, args: List[str], flags: Dict[str, Any]) -> int:
        """Write and view topic file."""
        if args and args[0] == "help" and not flags.get('force'):
            print(self.help())
            return 0

        if not args:
            return self.error("work requires: <topic>")

        topic = args[0]
        settings = self.config_repo.get_settings()

        fmt = flags.get("format") or settings.auto_cast_format
        if not fmt:
            return self.error("Format not specified. Use 'work <topic> format <ext>'")

        if not settings.topic_save:
            return self.error("topic_save not set")

        key = normalize_topic(topic)
        file_path = FileManager.join(settings.topic_save, f"{key}.{fmt}")

        # Ensure file exists (cast if needed)
        unikey_path = FileManager.join(settings.topic_save, f"{key}.unikey")
        if FileManager.exists(unikey_path):
            # Cast to ensure target file exists
            result = self._cast(args, flags)
            if result != 0:
                return result

        # Open viewer first (non-blocking)
        if FileManager.exists(file_path):
            viewer = settings.viewers.get(fmt)
            if viewer:
                import shlex
                viewer_cmd = shlex.split(viewer) + [file_path]
                subprocess.Popen(viewer_cmd)
                print(f"Opened viewer: {file_path}")

        # Then open editor (blocking)
        return self._write(args, flags)
