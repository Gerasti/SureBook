"""Delete command for simple CLI."""

import fnmatch
from typing import List, Dict, Any
from .base import Command
from repositories import InputRepository, ListRepository, TopicRepository
from fileutils import normalize_topic, strip_link
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
  del <pattern>         Delete topics matching pattern (wildcards: * ?)
  del <topic> from <s>  Delete from specific section
  del list <name>       Delete section (requires force flag)
  del help              Show this help

Flags:
  force                 Force deletion of non-empty lists

Examples:
  del "Python Tutorial"           # Delete everywhere
  del "ecorouter*"                # Delete all topics starting with ecorouter
  del "Docker *"                  # Delete all Docker topics
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
        if args and args[0] == "help" and not flags.get('force'):
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

        # Check if topic contains wildcards
        has_wildcard = '*' in topic or '?' in topic

        if len(args) >= 3 and args[1] == "from":
            section = args[2]
            if has_wildcard:
                # Get all topics from section and match pattern
                section_obj = self.list_repo.get_section(section)
                if not section_obj:
                    print(f"Section not found: {section}")
                    return 1

                matched_topics = []
                for t in section_obj.topics:
                    t_clean = strip_link(t)
                    # Match against original title
                    if fnmatch.fnmatch(t_clean, topic):
                        matched_topics.append(t)
                    # Also match against normalized key (with underscores)
                    elif fnmatch.fnmatch(normalize_topic(t_clean), topic):
                        matched_topics.append(t)
                if not matched_topics:
                    print(f"No topics matching '{topic}' in [{section}]")
                    return 0

                deleted_count = 0
                for t in matched_topics:
                    if self.list_repo.remove_topic_from_section(section, strip_link(t)):
                        print(f"Deleted: {strip_link(t)} [list:{section}]")
                        deleted_count += 1
                print(f"Total deleted from [{section}]: {deleted_count}")
            else:
                removed = self.list_repo.remove_topic_from_section(section, topic)
                if removed:
                    print(f"Deleted: {topic} [list:{section}]")
                else:
                    print(f"Not found in [{section}]: {topic}")
        else:
            # Delete everywhere
            if has_wildcard:
                # Collect all topics from all sources
                all_topics = set()

                # From input
                for t in self.input_repo.get_all():
                    all_topics.add(strip_link(t))

                # From lists
                for section in self.list_repo.get_all_sections():
                    for t in section.topics:
                        all_topics.add(strip_link(t))

                # From TOML
                for topic_obj in self.topic_repo.get_all():
                    all_topics.add(topic_obj.title)

                # Match pattern - check both original title and normalized key
                matched_topics = []
                for t in all_topics:
                    # Match against original title
                    if fnmatch.fnmatch(t, topic):
                        matched_topics.append(t)
                    # Also match against normalized key (with underscores)
                    elif fnmatch.fnmatch(normalize_topic(t), topic):
                        matched_topics.append(t)

                if not matched_topics:
                    print(f"No topics matching '{topic}'")
                    return 0

                print(f"Found {len(matched_topics)} topics matching '{topic}'")
                deleted_count = 0

                for matched_topic in matched_topics:
                    sources = []
                    if self.input_repo.remove(matched_topic):
                        sources.append("input")

                    for section in self.list_repo.get_all_sections():
                        if self.list_repo.remove_topic_from_section(section.name, matched_topic):
                            sources.append(f"list:{section.name}")

                    key = normalize_topic(matched_topic)
                    topic_obj = self.topic_repo.get_by_key(key)
                    if topic_obj:
                        if FileManager.exists(topic_obj.path):
                            FileManager.remove(topic_obj.path)
                        self.topic_repo.delete(key)
                        sources.append("TOML")

                    if sources:
                        print(f"Deleted: {matched_topic} [{', '.join(sources)}]")
                        deleted_count += 1

                print(f"Total deleted: {deleted_count}")
            else:
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
