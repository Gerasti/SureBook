"""Settings command for simple CLI."""

from typing import List, Dict, Any
from datetime import datetime
from .base import Command
from repositories import ConfigRepository
from file_manager import FileManager


class SettingsCommand(Command):
    """Show and edit settings."""

    def __init__(self, config_repo: ConfigRepository):
        self.config_repo = config_repo

    def help(self) -> str:
        """Return help text for config command."""
        return """Config command - manage settings

Usage:
  config                    Show all settings
  config <key> <value>      Set a setting
  config viewer <fmt> <cmd> Set viewer for format
  config time               Update last_saved to current time
  config default            Reset to default settings
  config help               Show this help

Keys (with aliases):
  input, i                  Input file path
  list, l                   Lists file path
  topic_save, save          Topic save path
  source_table_file, table  Source table file path
  editor, ed                Editor command
  auto_alphabetic_sort, sort  Auto sort (yes/no)
  auto_save, autosave       Auto save (yes/no)
  auto_cast, cast           Auto cast (yes/no)
  auto_cast_format, format  Auto cast format

Boolean values: yes/no, true/false, on/off, 1/0

Examples:
  config                    # Show all settings
  config i ~/input.md       # Set input path
  config sort yes           # Enable auto sort
  config ed nvim            # Set editor
  config viewer md glow     # Set markdown viewer
  config time               # Update last_saved time
  config default            # Reset to defaults
"""

    def execute(self, args: List[str], flags: Dict[str, Any]) -> int:
        """Execute settings command.

        Usage:
            config                  - Show all settings
            config <key> <value>    - Set a setting
            config viewer <fmt> <cmd> - Set viewer for format
            config time             - Update last_saved to current time
            config default          - Reset to default settings
        """
        if args and args[0] == "help" and not flags.get('force'):
            print(self.help())
            return 0

        if args and args[0] == "default":
            return self._reset_defaults()

        if args and args[0] == "time":
            return self._update_time()

        if not args:
            return self._show()

        # Special case for viewer
        if args[0] == "viewer":
            if len(args) < 3:
                return self.error("config viewer requires: <format> <command>")
            result = self._set_viewer(args[1], args[2])
            # Show settings after change
            print()
            self._show()
            return result

        # General setting
        if len(args) < 2:
            return self.error("config requires: <key> <value>")

        key = args[0]
        value = args[1]

        result = self._set_setting(key, value)
        # Show settings after change
        print()
        self._show()
        return result

    def _show(self) -> int:
        """Show all settings."""
        settings = self.config_repo.get_settings()

        print(f"Input:            {settings.input}")
        print(f"List:             {settings.list}")
        print(f"Topic save:       {settings.topic_save}")
        print(f"Source table:     {settings.source_table_file}")
        print(f"Editor:           {settings.editor}")
        print(f"Auto sort:        {settings.auto_alphabetic_sort}")
        print(f"Auto save:        {settings.auto_save}")
        print(f"Auto cast:        {settings.auto_cast}")
        print(f"Auto cast format: {settings.auto_cast_format}")

        if settings.viewers:
            print("\nViewers:")
            for fmt, viewer in settings.viewers.items():
                print(f"  {fmt}: {viewer}")

        if settings.last_saved:
            print(f"\nLast saved: {settings.last_saved}")

        return 0

    def _set_setting(self, key: str, value: str) -> int:
        """Set a setting."""
        settings = self.config_repo.get_settings()

        # Aliases for short names
        aliases = {
            "i": "input",
            "l": "list",
            "save": "topic_save",
            "table": "source_table_file",
            "ed": "editor",
            "sort": "auto_alphabetic_sort",
            "autosave": "auto_save",
            "cast": "auto_cast",
            "format": "auto_cast_format",
        }

        key = aliases.get(key, key)

        # Expand paths
        if key in ["input", "list", "topic_save", "source_table_file"]:
            value = FileManager.expanduser(value)

        # Boolean settings - accept more values
        if key in ["auto_alphabetic_sort", "auto_save", "auto_cast"]:
            bool_value = self._parse_bool(value)
            if bool_value is None:
                return self.error(f"{key} must be true/false, yes/no, on/off, 1/0")
            value = bool_value

        # Check if auto_save is being enabled
        auto_save_enabled = (key == "auto_save" and value is True and not settings.auto_save)

        # Update setting
        if key == "input":
            settings.input = value
        elif key == "list":
            settings.list = value
        elif key == "topic_save":
            settings.topic_save = value
        elif key == "source_table_file":
            settings.source_table_file = value
        elif key == "editor":
            settings.editor = value
        elif key == "auto_alphabetic_sort":
            settings.auto_alphabetic_sort = value
        elif key == "auto_save":
            settings.auto_save = value
        elif key == "auto_cast":
            settings.auto_cast = value
        elif key == "auto_cast_format":
            settings.auto_cast_format = value
        else:
            return self.error(f"Unknown setting: {key}")

        self.config_repo.save_settings(settings)

        # If auto_save was just enabled, trigger save
        if auto_save_enabled:
            print("\nAuto save enabled. Saving all topics...")
            from repositories import InputRepository, ListRepository, TopicRepository
            from fileutils import paths_to_list

            input_paths = paths_to_list(settings.input)
            list_paths = paths_to_list(settings.list)

            if input_paths and list_paths:
                from commands.save import SaveCommand
                input_repo = InputRepository(input_paths[0])
                list_repo = ListRepository(list_paths[0])
                topic_repo = TopicRepository(self.config_repo.toml_path)
                save_cmd = SaveCommand(input_repo, list_repo, topic_repo, self.config_repo)
                save_cmd.execute([], {})

        return 0

    def _parse_bool(self, value: str) -> bool | None:
        """Parse boolean value from string."""
        value = value.lower()
        if value in ["true", "yes", "on", "1"]:
            return True
        if value in ["false", "no", "off", "0"]:
            return False
        return None

    def _set_viewer(self, fmt: str, cmd: str) -> int:
        """Set viewer for format."""
        settings = self.config_repo.get_settings()
        settings.viewers[fmt] = cmd
        self.config_repo.save_settings(settings)
        return 0

    def _reset_defaults(self) -> int:
        """Reset settings to defaults."""
        # Create new settings object with defaults
        from models import Settings

        settings = Settings(
            input="~/SureBook/info/def_input.md",
            list="~/SureBook/info/def_lists.md",
            topic_save="~/SureBook/topics",
            source_table_file="~/SureBook/info/src_table.md",
            auto_alphabetic_sort=True,
            auto_save=True,
            auto_cast=True,
            auto_cast_format="md",
            editor="nvim",
            last_saved="1970-01-01 00:00:00",
            viewers={}
        )

        self.config_repo.save_settings(settings)
        print("Settings reset to defaults")
        print()
        self._show()
        return 0

    def _update_time(self) -> int:
        """Update last_saved to current time."""
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.config_repo.update_setting("last_saved", now_str)
        print(f"Updated last_saved to: {now_str}")
        return 0
