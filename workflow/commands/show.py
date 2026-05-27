"""Show command for simple CLI."""

from typing import List, Dict, Any
from .base import Command
from repositories import InputRepository, ListRepository, TopicRepository
from fileutils import normalize_for_compare, strip_link


class ShowCommand(Command):
    """Show topics from input/list files."""

    def __init__(self, input_repo: InputRepository, list_repo: ListRepository, topic_repo: TopicRepository):
        self.input_repo = input_repo
        self.list_repo = list_repo
        self.topic_repo = topic_repo

    def help(self) -> str:
        """Return help text for show command."""
        return """Show command - display topics

Usage:
  show [N]           Show all topics with sources (limit to N)
  show input [N]     Show input topics
  show saved [N]     Show saved topics from TOML
  show save [N]      Show topics that would be saved
  show lists [N]     Show list sections
  show from <sec> [N]  Show topics from specific section
  show N from <sec>  Show N topics from section
  show help          Show this help

Limit:
  N > 0              Show first N items
  N < 0              Show last N items (from end)

Flags:
  pure               Clean output without headers

Examples:
  show               # Show all topics with sources
  show 10            # Show first 10 topics
  show -5            # Show last 5 topics
  show input -3      # Show last 3 input topics
  show save          # Show topics that would be saved
  show save 10       # Show first 10 topics to save
  show from backend  # Show all topics from backend
  show 5 from notesk # Show first 5 from notesk
  show -2 from notesk # Show last 2 from notesk
"""

    def execute(self, args: List[str], flags: Dict[str, Any]) -> int:
        """Execute show command.

        Usage:
            show [N]              - Show all or first N topics with sources
            show input [N]        - Show input topics
            show saved [N]        - Show saved topics
            show lists [N]        - Show list sections
        """
        if args and args[0] == "help" and not flags.get('force'):
            print(self.help())
            return 0

        pure = flags.get('pure', False)

        if not args:
            # show all with sources
            return self._show_all_with_sources(0, pure)

        subcommand = args[0]

        # Check for "show N from <section>" pattern
        if len(args) >= 3 and args[1] == "from":
            try:
                limit = int(subcommand)
                section_name = args[2]

                section = self.list_repo.get_section(section_name)
                if not section:
                    print(f"Section not found: {section_name}")
                    return 1

                topics = section.topics
                if limit > 0:
                    topics = topics[:limit]
                elif limit < 0:
                    topics = topics[limit:]  # Show last N items

                header = f"Topics in [{section_name}] ({len(topics)}):" if not pure else None
                self.print_items(topics, header, pure)
                return 0
            except ValueError:
                pass  # Not a number, continue with normal flow

        if subcommand == "from":
            # show from <section> [N]
            if len(args) < 2:
                return self.error("show from requires section name")

            section_name = args[1]
            limit = int(args[2]) if len(args) > 2 else 0

            section = self.list_repo.get_section(section_name)
            if not section:
                print(f"Section not found: {section_name}")
                return 1

            topics = section.topics
            if limit > 0:
                topics = topics[:limit]
            elif limit < 0:
                topics = topics[limit:]  # Show last N items

            header = f"Topics in [{section_name}] ({len(topics)}):" if not pure else None
            self.print_items(topics, header, pure)
            return 0

        elif subcommand == "input":
            limit = int(args[1]) if len(args) > 1 else 0
            topics = self.input_repo.get_all()
            if limit > 0:
                topics = topics[:limit]
            elif limit < 0:
                topics = topics[limit:]

            header = f"Input topics ({len(topics)}):" if not pure else None
            self.print_items(topics, header, pure)
            return 0

        elif subcommand == "saved":
            limit = int(args[1]) if len(args) > 1 else 0
            topics = self.topic_repo.get_all()
            if limit > 0:
                topics = topics[:limit]
            elif limit < 0:
                topics = topics[limit:]

            if pure:
                for t in topics:
                    print(t.title)
            else:
                for t in topics:
                    parts = []
                    for entry in t.lists:
                        if entry.link:
                            display = entry.link_look if entry.link_look else t.title
                            parts.append(f"{entry.list_name} [{display}]({entry.link})")
                        else:
                            parts.append(entry.list_name)
                    lists_str = ", ".join(parts) if parts else "—"
                    print(f"\n{t.title} [path: {t.path}]")
                    print(f"[lists: {lists_str}]")
            return 0

        elif subcommand == "lists":
            limit = int(args[1]) if len(args) > 1 else 0
            sections = self.list_repo.get_section_names()
            if limit > 0:
                sections = sections[:limit]
            elif limit < 0:
                sections = sections[limit:]

            header = f"Lists ({len(sections)}):" if not pure else None
            self.print_items(sections, header, pure)
            return 0

        elif subcommand == "save":
            # show save [N] - show topics that would be saved
            limit = int(args[1]) if len(args) > 1 else 0
            return self._show_save(limit, pure)

        else:
            # show N with sources
            try:
                limit = int(subcommand)
                return self._show_all_with_sources(limit, pure)
            except ValueError:
                return self.error(f"Unknown subcommand: {subcommand}")

    def _show_all_with_sources(self, limit: int, pure: bool) -> int:
        """Show all topics with their sources."""
        topics_i = self.input_repo.get_all()

        # Build distribution
        dist = self._build_distribution()

        # Get unique topics from input
        show_topics = topics_i
        if limit > 0:
            show_topics = show_topics[:limit]

        seen = set()
        for t in show_topics:
            norm = normalize_for_compare(t)
            if norm in seen:
                continue
            seen.add(norm)

            data = dist.get(norm)
            title = strip_link(t) if not data else data["title"]

            if pure:
                print(title)
            else:
                if data:
                    parts = []
                    if data["in_input"]:
                        parts.append("input")
                    if data["sections"]:
                        parts.extend(data["sections"])
                    src = ", ".join(parts) if parts else "—"
                else:
                    src = "—"
                print(f"{title}  [{src}]")

        return 0

    def _build_distribution(self) -> Dict[str, Dict]:
        """Build topic distribution mapping."""
        dist = {}

        # Add input topics
        for t in self.input_repo.get_all():
            norm = normalize_for_compare(t)
            dist.setdefault(norm, {
                "title": strip_link(t),
                "in_input": False,
                "sections": [],
            })
            dist[norm]["in_input"] = True

        # Add list topics
        for section in self.list_repo.get_all_sections():
            for topic_str in section.topics:
                plain = strip_link(topic_str)
                norm = normalize_for_compare(plain)
                dist.setdefault(norm, {
                    "title": plain,
                    "in_input": False,
                    "sections": [],
                })
                if section.name not in dist[norm]["sections"]:
                    dist[norm]["sections"].append(section.name)

        return dist

    def _show_save(self, limit: int, pure: bool) -> int:
        """Show topics that would be saved."""
        from fileutils import normalize_topic, uniq_keep_order

        topics_i = self.input_repo.get_all()
        topics_l = self.list_repo.get_all_topics()
        topics = uniq_keep_order(topics_i + topics_l)

        existing = self.topic_repo.get_existing_keys()

        # Build topic sections mapping
        topic_sections = {}
        for section in self.list_repo.get_all_sections():
            for topic_str in section.topics:
                from fileutils import strip_link
                plain = strip_link(topic_str)
                if plain not in topic_sections:
                    topic_sections[plain] = []
                if section.name not in topic_sections[plain]:
                    topic_sections[plain].append(section.name)

        # Filter new topics
        new_topics = []
        for topic_str in topics:
            from fileutils import strip_link
            clean_topic = strip_link(topic_str)
            key = normalize_topic(clean_topic)
            if key not in existing:
                new_topics.append(clean_topic)

        if not new_topics:
            print("No new topics to save (all topics already in TOML)")
            return 0

        if limit > 0:
            new_topics = new_topics[:limit]
        elif limit < 0:
            new_topics = new_topics[limit:]

        if pure:
            for topic in new_topics:
                print(topic)
        else:
            print(f"Would be saved ({len(new_topics)}):")
            topics_i_set = set(topics_i)
            for topic in new_topics:
                parts = []
                if topic in topics_i_set:
                    parts.append("input")
                if topic in topic_sections:
                    parts.extend(topic_sections[topic])
                src = ", ".join(parts) if parts else "unknown"
                print(f"  {topic}  [{src}]")

        return 0
