"""Data models for the workflow application."""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ListEntry:
    """Represents a topic's presence in a list section with optional link."""
    list_name: str
    link: Optional[str] = None
    link_look: Optional[str] = None

    def to_dict(self):
        """Convert to dictionary for TOML serialization."""
        result = {"list": self.list_name}
        if self.link:
            result["link"] = self.link
        if self.link_look:
            result["link_look"] = self.link_look
        return result

    @classmethod
    def from_dict(cls, data: dict):
        """Create from dictionary."""
        return cls(
            list_name=data["list"],
            link=data.get("link"),
            link_look=data.get("link_look")
        )


@dataclass
class Topic:
    """Represents a topic with its metadata."""
    key: str
    title: str
    path: str
    lists: List[ListEntry] = field(default_factory=list)

    def to_dict(self):
        """Convert to dictionary for TOML serialization."""
        return {
            "title": self.title,
            "path": self.path,
            "lists": [entry.to_dict() for entry in self.lists]
        }

    @classmethod
    def from_dict(cls, key: str, data: dict):
        """Create from dictionary."""
        return cls(
            key=key,
            title=data.get("title", ""),
            path=data.get("path", ""),
            lists=[ListEntry.from_dict(entry) for entry in data.get("lists", [])]
        )


@dataclass
class Settings:
    """Application settings."""
    input: str
    list: str
    topic_save: str
    source_table_file: str
    auto_alphabetic_sort: bool = False
    auto_save: bool = False
    auto_cast: bool = False
    auto_cast_format: str = ""
    editor: str = "nvim"
    last_saved: str = ""
    viewers: dict = field(default_factory=dict)

    def to_dict(self):
        """Convert to dictionary for TOML serialization."""
        result = {
            "input": self.input,
            "list": self.list,
            "topic_save": self.topic_save,
            "source_table_file": self.source_table_file,
            "auto_alphabetic_sort": "true" if self.auto_alphabetic_sort else "false",
            "auto_save": "true" if self.auto_save else "false",
            "auto_cast": "true" if self.auto_cast else "false",
            "auto_cast_format": self.auto_cast_format,
            "editor": self.editor,
        }
        if self.last_saved:
            result["last_saved"] = self.last_saved

        # Add viewers
        for fmt, viewer in self.viewers.items():
            result[f"viewer_{fmt}"] = viewer

        return result

    @classmethod
    def from_dict(cls, data: dict):
        """Create from dictionary."""
        viewers = {}
        for key, value in data.items():
            if key.startswith("viewer_"):
                fmt = key[len("viewer_"):]
                viewers[fmt] = value

        return cls(
            input=data.get("input", ""),
            list=data.get("list", ""),
            topic_save=data.get("topic_save", ""),
            source_table_file=data.get("source_table_file", ""),
            auto_alphabetic_sort=data.get("auto_alphabetic_sort", "false") == "true",
            auto_save=data.get("auto_save", "false") == "true",
            auto_cast=data.get("auto_cast", "false") == "true",
            auto_cast_format=data.get("auto_cast_format", ""),
            editor=data.get("editor", "nvim"),
            last_saved=data.get("last_saved", ""),
            viewers=viewers
        )


@dataclass
class ListSection:
    """Represents a section in a list file."""
    name: str
    topics: List[str] = field(default_factory=list)
