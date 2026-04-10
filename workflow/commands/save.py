"""Save command for simple CLI."""

from typing import List, Dict, Any
from datetime import datetime
from .base import Command
from repositories import InputRepository, ListRepository, TopicRepository, ConfigRepository
from models import Topic, ListEntry
from fileutils import normalize_topic, strip_link, extract_link, uniq_keep_order
from file_manager import FileManager


class SaveCommand(Command):
    """Save topics to TOML."""

    def __init__(
        self,
        input_repo: InputRepository,
        list_repo: ListRepository,
        topic_repo: TopicRepository,
        config_repo: ConfigRepository
    ):
        self.input_repo = input_repo
        self.list_repo = list_repo
        self.topic_repo = topic_repo
        self.config_repo = config_repo

    def help(self) -> str:
        """Return help text for save command."""
        return """Save command - save topics to TOML

Usage:
  save [topics...]      Save topics to TOML (empty = all new)
  save help             Show this help

Note: Use 'show save' to preview topics that would be saved

Examples:
  save                  # Save all new topics
  save "Python" "Django"  # Save specific topics
  show save             # Preview what would be saved (moved to show command)
  show save 10          # Preview first 10 topics to save
"""

    def execute(self, args: List[str], flags: Dict[str, Any]) -> int:
        """Execute save command.

        Usage:
            save [topics...]      - Save to TOML (empty = all)
        """
        # Check for help
        if args and args[0] == "help":
            print(self.help())
            return 0

        # Check for deprecated 'save show' syntax
        if args and args[0] == "show":
            print("Note: 'save show' is deprecated. Use 'show save' instead.")
            print("Example: show save [N]")
            return 1

        settings = self.config_repo.get_settings()

        if not settings.topic_save:
            return self.error("topic_save not set")

        topics_i = self.input_repo.get_all()
        topics_l = self.list_repo.get_all_topics()
        topics = uniq_keep_order(topics_i + topics_l)

        if args:
            # Save specific topics
            topics = [t for t in topics if strip_link(t) in args]

        existing = self.topic_repo.get_existing_keys()

        # Build topic sections and links mapping
        topic_sections = {}
        topic_links = {}

        for section in self.list_repo.get_all_sections():
            for topic_str in section.topics:
                plain = strip_link(topic_str)
                if plain not in topic_sections:
                    topic_sections[plain] = []
                if section.name not in topic_sections[plain]:
                    topic_sections[plain].append(section.name)

                # Extract link
                link_look, url = extract_link(topic_str)
                if url:
                    topic_links[(plain, section.name)] = (link_look, url)

        # Save topics
        FileManager.ensure_dir(settings.topic_save)
        saved_count = 0

        for topic_str in topics:
            clean_topic = strip_link(topic_str)
            key = normalize_topic(clean_topic)

            if key in existing:
                continue

            # Create topic object
            md_path = FileManager.join(settings.topic_save, f"{key}.md")
            sections = topic_sections.get(clean_topic, [])

            list_entries = []
            for sec in sections:
                link_look, url = topic_links.get((clean_topic, sec), (None, None))
                if url:
                    entry = ListEntry(list_name=sec, link=url, link_look=link_look)
                else:
                    entry = ListEntry(list_name=sec)
                list_entries.append(entry)

            topic = Topic(
                key=key,
                title=clean_topic,
                path=md_path,
                lists=list_entries
            )

            self.topic_repo.save(topic)
            print(f"Saved: {clean_topic}")
            saved_count += 1

        if saved_count == 0:
            print("Nothing to save — all topics already in TOML")
        else:
            print(f"Total saved: {saved_count}")
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.config_repo.update_setting("last_saved", now_str)

        return 0
