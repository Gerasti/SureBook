#!/usr/bin/env python3
"""Simple CLI without argparse - git-style commands."""

import sys
import os

from repositories import ConfigRepository, TopicRepository, InputRepository, ListRepository
from commands import (
    ShowCommand, AddCommand, DeleteCommand, SearchCommand, RenameCommand,
    SaveCommand, SettingsCommand, LinkCommand, EditorCommand, TableCommand,
    UnsaveCommand, CleanupCommand
)
from fileutils import paths_to_list, diff_lists


def get_toml_path():
    """Get TOML path from environment or default."""
    return os.environ.get("TOPICS_TOML_PATH", os.path.expanduser("~/SureBook/info/topics.toml"))


def show_help():
    """Show help message."""
    print("""Usage: topics <command> [args]

Commands:
  show [N]              Show all or first N topics
  show input [N]        Show input topics
  show saved [N]        Show saved topics
  show save [N]         Show new topics to be saved
  show lists [N]        Show list sections
  show from <sec> [N]   Show topics from section
  show N from <sec>     Show N topics from section

  input <path> [N]      Show topics from alternative input file
  list <path> [N]       Show sections from alternative list file

  add <topic>           Add topic to input
  add <topic> to <sec>  Add topic to section
  add list <name>       Create new section

  del <topic>           Delete topic everywhere
  del <topic> from <s>  Delete from section
  del list <name>       Delete section (use 'force' flag)

  search <query>        Search in input/lists
  search saved <query>  Search in TOML

  rename <old> <new>    Rename topic
  rename list <o> <n>   Rename section

  save [topics...]      Save to TOML (empty = all new)
  unsave <topics...>    Remove topics from TOML
  unsave all force      Remove all topics (requires force)

  link add <t> <s> <url> [display]  Add link to topic
  link del <topic> <section>        Remove link

  write <topic>         Open/create .unikey file
  cast <topic>          Convert .unikey to format
  view <topic>          View converted file

  table [generate]      Generate source table
  table show            View source table

  cleanup               Remove duplicate topics from TOML
  sort                  Sort alphabetically
  count                 Show statistics
  compare               Compare input vs lists
  config [key value]    Show/edit settings
  config viewer <f> <c> Set viewer for format

Flags:
  pure                  Clean output without headers
  force                 Force operation
  format <ext>          Specify format (for cast/view)

Limit (for show commands):
  N > 0                 Show first N items
  N < 0                 Show last N items

Examples:
  show 10
  show -5
  show save
  show from backend
  show 5 from notesk
  input ~/other_input.md
  list ~/other_lists.md
  add "Python Tutorial"
  add "Django" to backend
  search python
  save
  link add "Python" backend https://python.org
  write "Python"
  cast "Python" format md
  view "Python" format md
  table generate
  config editor nvim
  config viewer md "glow -p"
""")


def parse_args(args):
    """Parse command line arguments.

    Returns:
        (command, positional_args, flags)
    """
    if not args:
        return None, [], {}

    # Extract flags
    flags = {
        'pure': 'pure' in args,
        'force': 'force' in args,
    }

    # Extract format flag (but not for config command)
    if 'format' in args and args[0] != 'config':
        idx = args.index('format')
        if idx + 1 < len(args):
            flags['format'] = args[idx + 1]
            args = args[:idx] + args[idx + 2:]

    # Remove flags from args
    positional = [a for a in args if a not in ['pure', 'force']]

    if not positional:
        return None, [], flags

    command = positional[0]
    rest = positional[1:]

    return command, rest, flags


def main():
    """Main entry point."""
    if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help', 'help']:
        show_help()
        return 0

    command, args, flags = parse_args(sys.argv[1:])

    if not command:
        show_help()
        return 0

    # Initialize repositories
    toml_path = get_toml_path()
    config_repo = ConfigRepository(toml_path)
    topic_repo = TopicRepository(toml_path)
    settings = config_repo.get_settings()

    # Expand paths from settings
    from file_manager import FileManager
    settings.input = FileManager.expanduser(settings.input)
    settings.list = FileManager.expanduser(settings.list)
    settings.topic_save = FileManager.expanduser(settings.topic_save)
    settings.source_table_file = FileManager.expanduser(settings.source_table_file)

    input_paths = paths_to_list(settings.input)
    list_paths = paths_to_list(settings.list)
    input_path = input_paths[0] if input_paths else None
    list_path = list_paths[0] if list_paths else None

    # Allow config command to run even without paths configured
    if command == "config":
        settings_cmd = SettingsCommand(config_repo)
        return settings_cmd.execute(args, flags)

    if not input_path or not list_path:
        print("Error: input/list paths not configured")
        print("Check your TOML configuration")
        return 1

    input_repo = InputRepository(input_path)
    list_repo = ListRepository(list_path)

    # Auto sort if enabled
    if settings.auto_alphabetic_sort:
        input_repo.sort_alphabetically()
        list_repo.sort_alphabetically()

    # Initialize commands
    show_cmd = ShowCommand(input_repo, list_repo, topic_repo)
    add_cmd = AddCommand(input_repo, list_repo)
    delete_cmd = DeleteCommand(input_repo, list_repo, topic_repo)
    search_cmd = SearchCommand(input_repo, list_repo, topic_repo)
    rename_cmd = RenameCommand(input_repo, list_repo, topic_repo)
    save_cmd = SaveCommand(input_repo, list_repo, topic_repo, config_repo)
    settings_cmd = SettingsCommand(config_repo)
    link_cmd = LinkCommand(list_repo)
    editor_cmd = EditorCommand(config_repo)
    table_cmd = TableCommand(topic_repo, config_repo)
    unsave_cmd = UnsaveCommand(topic_repo)
    cleanup_cmd = CleanupCommand(toml_path)

    # Handle input/list path overrides first
    if command == "input":
        # input <path> [command] - use alternative input file
        if args == ["help"] and not flags.get('force'):
            print("""Input command - use alternative input file

Usage:
  input <path>      Show topics from alternative input file
  input help        Show this help

Examples:
  input ~/other_input.md        # Show topics from other file
""")
            return 0

        if not args:
            print("Error: input requires path")
            return 1
        alt_input_path = FileManager.expanduser(args[0])
        if not FileManager.exists(alt_input_path):
            print(f"Error: File not found: {alt_input_path}")
            return 1

        # Replace input_repo with alternative
        input_repo = InputRepository(alt_input_path)

        # Get subcommand or default to show
        if len(args) > 1:
            command = args[1]
            args = args[2:]
        else:
            # Default: show input topics
            show_cmd = ShowCommand(input_repo, list_repo, topic_repo)
            return show_cmd.execute(["input"], flags)

    if command == "list":
        # list <path> [command] - use alternative list file
        if args == ["help"] and not flags.get('force'):
            print("""List command - use alternative list file

Usage:
  list <path>       Show sections from alternative list file
  list help         Show this help

Examples:
  list ~/other_lists.md         # Show sections from other file
""")
            return 0

        if not args:
            print("Error: list requires path")
            return 1
        alt_list_path = FileManager.expanduser(args[0])
        if not FileManager.exists(alt_list_path):
            print(f"Error: File not found: {alt_list_path}")
            return 1

        # Replace list_repo with alternative
        list_repo = ListRepository(alt_list_path)

        # Get subcommand or default to show
        if len(args) > 1:
            command = args[1]
            args = args[2:]
        else:
            # Default: show list sections
            show_cmd = ShowCommand(input_repo, list_repo, topic_repo)
            return show_cmd.execute(["lists"], flags)

    # Re-initialize commands (in case repos were replaced)
    show_cmd = ShowCommand(input_repo, list_repo, topic_repo)
    add_cmd = AddCommand(input_repo, list_repo)
    delete_cmd = DeleteCommand(input_repo, list_repo, topic_repo)
    search_cmd = SearchCommand(input_repo, list_repo, topic_repo)
    rename_cmd = RenameCommand(input_repo, list_repo, topic_repo)
    save_cmd = SaveCommand(input_repo, list_repo, topic_repo, config_repo)
    settings_cmd = SettingsCommand(config_repo)
    link_cmd = LinkCommand(list_repo)
    editor_cmd = EditorCommand(config_repo)
    table_cmd = TableCommand(topic_repo, config_repo)
    unsave_cmd = UnsaveCommand(topic_repo)

    # Execute command
    try:
        if command == "show":
            return show_cmd.execute(args, flags)

        elif command == "add":
            return add_cmd.execute(args, flags)

        elif command in ["del", "delete", "rm"]:
            return delete_cmd.execute(args, flags)

        elif command in ["search", "find"]:
            return search_cmd.execute(args, flags)

        elif command in ["rename", "mv"]:
            return rename_cmd.execute(args, flags)

        elif command == "save":
            return save_cmd.execute(args, flags)

        elif command == "sort":
            if args == ["help"] and not flags.get('force'):
                print("""Sort command - sort topics alphabetically

Usage:
  sort              Sort input and lists alphabetically
  sort help         Show this help

Examples:
  sort              # Sort all topics
""")
                return 0
            input_repo.sort_alphabetically()
            list_repo.sort_alphabetically()
            print("Sorted alphabetically")
            return 0

        elif command == "count":
            if args == ["help"] and not flags.get('force'):
                print("""Count command - show statistics

Usage:
  count             Show topic statistics
  count help        Show this help

Output:
  - Union uniq topics: Total unique topics across input and lists
  - Common topics: Topics present in both input and lists
  - Input statistics: Total and unique topics in input
  - List statistics: Total, unique, and linked topics in lists
  - Topic files: Count of files by extension in topic_save directory

Examples:
  count             # Show all statistics
""")
                return 0
            topics_i = input_repo.get_all()
            topics_l = list_repo.get_all_topics()
            from fileutils import normalize_for_compare, uniq_keep_order, strip_link, extract_link

            # Normalize for comparison
            norm_i = {normalize_for_compare(t) for t in topics_i}
            norm_l = {normalize_for_compare(t) for t in topics_l}

            # Union and common
            union_uniq = len(norm_i | norm_l)
            common = len(norm_i & norm_l)

            # Input stats
            input_uniq = len(norm_i)

            # List stats
            list_uniq = len(norm_l)
            list_with_links = sum(1 for t in topics_l if extract_link(t)[1])

            print(f"Union uniq topics: {union_uniq}")
            print(f"Common topics:     {common}")
            print()
            print(f"All input topics:  {len(topics_i)}")
            print(f"Input uniq topics: {input_uniq}")
            print()
            print(f"All list topics:   {len(topics_l)}")
            print(f"List uniq topics:  {list_uniq}")
            print(f"List link topics:  {list_with_links}")

            # Count topic files by extension
            topic_save_dir = FileManager.expanduser(settings.topic_save)
            if FileManager.exists(topic_save_dir):
                from collections import defaultdict
                ext_count = defaultdict(int)
                total_files = 0

                for filename in os.listdir(topic_save_dir):
                    filepath = os.path.join(topic_save_dir, filename)
                    if os.path.isfile(filepath):
                        total_files += 1
                        ext = os.path.splitext(filename)[1]
                        if ext:
                            ext_count[ext] += 1
                        else:
                            ext_count['(no ext)'] += 1

                if total_files > 0:
                    print()
                    print(f"Topic files total: {total_files}")
                    for ext in sorted(ext_count.keys()):
                        print(f"  {ext:12} {ext_count[ext]}")

            return 0

        elif command == "compare":
            if args == ["help"] and not flags.get('force'):
                print("""Compare command - compare topics between sources

Usage:
  compare           Compare input vs all list sections
  compare help      Show this help

Output:
  For each pair of sources (input and sections):
  - Only in source1: Topics unique to first source
  - Only in source2: Topics unique to second source
  - Common: Topics present in both sources

Examples:
  compare           # Compare all sources
""")
                return 0
            from fileutils import normalize_for_compare

            topics_i = input_repo.get_all()
            sections = list_repo.get_all_sections()

            # Build normalized sets
            sources = {"input": {normalize_for_compare(t) for t in topics_i}}
            for section in sections:
                sources[section.name] = {normalize_for_compare(t) for t in section.topics}

            # Compare all pairs
            source_names = list(sources.keys())
            comparisons = []

            for i, name1 in enumerate(source_names):
                for name2 in source_names[i+1:]:
                    set1 = sources[name1]
                    set2 = sources[name2]

                    only_in_1 = set1 - set2
                    only_in_2 = set2 - set1
                    common = set1 & set2

                    if only_in_1 or only_in_2:
                        comparisons.append({
                            "name1": name1,
                            "name2": name2,
                            "only_1": len(only_in_1),
                            "only_2": len(only_in_2),
                            "common": len(common)
                        })

            if not comparisons:
                print("All sources are identical")
                return 0

            # Print results
            for comp in comparisons:
                print(f"\n{comp['name1']} vs {comp['name2']}:")
                print(f"  Only in {comp['name1']}: {comp['only_1']}")
                print(f"  Only in {comp['name2']}: {comp['only_2']}")
                print(f"  Common: {comp['common']}")

            return 0

        elif command == "config":
            return settings_cmd.execute(args, flags)

        elif command == "link":
            return link_cmd.execute(args, flags)

        elif command in ["write", "cast", "view"]:
            return editor_cmd.execute([command] + args, flags)

        elif command == "table":
            return table_cmd.execute(args, flags)

        elif command == "unsave":
            return unsave_cmd.execute(args, flags)

        elif command == "cleanup":
            return cleanup_cmd.execute(args, flags)

        else:
            print(f"Unknown command: {command}")
            print("Run 'help' for usage")
            return 1

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        # Auto save if enabled and not in read-only commands
        # Exclude show and its subcommands (show, show save, show input, etc.)
        if settings.auto_save and command not in ["config", "show", "search", "count", "compare"]:
            try:
                save_cmd.execute([], {"auto": True})
            except Exception as e:
                print(f"Auto-save failed: {e}")


if __name__ == "__main__":
    sys.exit(main())
