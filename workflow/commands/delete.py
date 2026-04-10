"""Delete command for simple CLI."""

from typing import List, Dict, Any
from .base import Command
from repositories import InputRepository, ListRepository, TopicRepository
from fileutils import normalize_topic
from file_manager import FileManager


class DeleteCommand(Command):
    """Delete topics or lists."""

    def __init__(self, input_repo: InputRepository, list_repo: ListRepository, topic_repo: TopicRepository):
        self.input_repo = input_repo
        self.list_repo = list_repo
        self.topic_repo = topic_repo

    def help(self) -> str:
        """Return help text for delete command."""
        return """Delete command - remove topics and lists

Usage:
  del <topic>           Delete topic everywhere
  del <topic> from <s>  Delete from specific section
  del list <name>       Delete section (requires force flag)
  del help              Show this help

Flags:
  force                 Force deletion of non-empty lists

Examples:
  del "Python Tutorial"           # Delete everywhere
  del "Django" from backend       # Delete from backend only
  del list old force              # Delete old section with force
"""

    def execute(self, args: List[str], flags: Dict[str, Any]) -> int:
        """Execute delete command.

        Usage:
            del <topic>           - Delete topic everywhere
            del <topic> from <s>  - Delete from section
            del list <name>       - Delete section (use 'force' flag)
        """
        if args and args[0] == "help":
            print(self.help())
            return 0

        if not args:
            return self.error("del requires arguments")

        force = flags.get('force', False)

        if args[0] == "list":
            # del list <name>
            if len(args) < 2:
                return self.error("del list requires name")

            name = args[1]
            section = self.list_repo.get_section(name)

            if not section:
                print(f"List not found: {name}")
                return 1

            if section.topics and not force:
                print(f"List [{name}] contains {len(section.topics)} topics")
                print("Use 'force' flag to delete")
                return 1

            deleted = self.list_repo.delete_section(name)
            if deleted:
                print(f"Deleted list: {name}")
            return 0

        # del <topic> [from <section>]
        topic = args[0]

        if len(args) >= 3 and args[1] == "from":
            section = args[2]
            removed = self.list_repo.remove_topic_from_section(section, topic)
            if removed:
                print(f"Deleted: {topic} [list:{section}]")
            else:
                print(f"Not found in [{section}]: {topic}")
        else:
            # Delete everywhere
            sources = []
            if self.input_repo.remove(topic):
                sources.append("input")

            for section in self.list_repo.get_all_sections():
                if self.list_repo.remove_topic_from_section(section.name, topic):
                    sources.append(f"list:{section.name}")

            key = normalize_topic(topic)
            topic_obj = self.topic_repo.get_by_key(key)
            if topic_obj:
                if FileManager.exists(topic_obj.path):
                    FileManager.remove(topic_obj.path)
                self.topic_repo.delete(key)
                sources.append("TOML")

            if sources:
                print(f"Deleted: {topic} [{', '.join(sources)}]")
            else:
                print(f"Not found: {topic}")

        return 0
