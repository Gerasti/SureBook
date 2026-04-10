"""File management utilities with centralized file operations."""

import os
from typing import List, Optional


class FileManager:
    """Centralized file operations manager."""

    @staticmethod
    def ensure_dir(path: str) -> None:
        """Ensure directory exists, create if needed."""
        os.makedirs(path, exist_ok=True)

    @staticmethod
    def ensure_parent_dir(file_path: str) -> None:
        """Ensure parent directory of file exists."""
        parent = os.path.dirname(file_path)
        if parent:
            FileManager.ensure_dir(parent)

    @staticmethod
    def exists(path: str) -> bool:
        """Check if path exists."""
        return os.path.exists(path)

    @staticmethod
    def is_file(path: str) -> bool:
        """Check if path is a file."""
        return os.path.isfile(path)

    @staticmethod
    def is_dir(path: str) -> bool:
        """Check if path is a directory."""
        return os.path.isdir(path)

    @staticmethod
    def read_lines(path: str, strip: bool = False) -> List[str]:
        """Read all lines from file.

        Args:
            path: File path
            strip: If True, strip whitespace from each line

        Returns:
            List of lines (empty list if file doesn't exist)
        """
        if not FileManager.is_file(path):
            return []

        with open(path, encoding="utf-8") as f:
            lines = f.readlines()
            if strip:
                return [line.strip() for line in lines]
            return lines

    @staticmethod
    def read_non_empty_lines(path: str) -> List[str]:
        """Read non-empty lines from file (stripped).

        Returns:
            List of non-empty lines (empty list if file doesn't exist)
        """
        if not FileManager.is_file(path):
            return []

        with open(path, encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]

    @staticmethod
    def read_text(path: str) -> str:
        """Read entire file as text.

        Returns:
            File contents (empty string if file doesn't exist)
        """
        if not FileManager.is_file(path):
            return ""

        with open(path, encoding="utf-8") as f:
            return f.read()

    @staticmethod
    def write_lines(path: str, lines: List[str], ensure_newline: bool = True) -> None:
        """Write lines to file.

        Args:
            path: File path
            lines: Lines to write
            ensure_newline: If True, ensure each line ends with newline
        """
        FileManager.ensure_parent_dir(path)

        with open(path, "w", encoding="utf-8") as f:
            for line in lines:
                if ensure_newline and not line.endswith("\n"):
                    f.write(line + "\n")
                else:
                    f.write(line)

    @staticmethod
    def write_text(path: str, content: str) -> None:
        """Write text to file."""
        FileManager.ensure_parent_dir(path)

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    @staticmethod
    def append_lines(path: str, lines: List[str], ensure_newline: bool = True) -> None:
        """Append lines to file."""
        FileManager.ensure_parent_dir(path)

        with open(path, "a", encoding="utf-8") as f:
            for line in lines:
                if ensure_newline and not line.endswith("\n"):
                    f.write(line + "\n")
                else:
                    f.write(line)

    @staticmethod
    def append_text(path: str, content: str) -> None:
        """Append text to file."""
        FileManager.ensure_parent_dir(path)

        with open(path, "a", encoding="utf-8") as f:
            f.write(content)

    @staticmethod
    def remove(path: str) -> bool:
        """Remove file if exists.

        Returns:
            True if file was removed, False if didn't exist
        """
        if FileManager.exists(path):
            os.remove(path)
            return True
        return False

    @staticmethod
    def list_files(directory: str, pattern: Optional[str] = None) -> List[str]:
        """List files in directory.

        Args:
            directory: Directory path
            pattern: Optional filename pattern (e.g., "*.md")

        Returns:
            List of file paths (empty if directory doesn't exist)
        """
        if not FileManager.is_dir(directory):
            return []

        files = []
        for fname in os.listdir(directory):
            fpath = os.path.join(directory, fname)
            if FileManager.is_file(fpath):
                if pattern is None:
                    files.append(fpath)
                else:
                    import fnmatch
                    if fnmatch.fnmatch(fname, pattern):
                        files.append(fpath)
        return files

    @staticmethod
    def get_mtime(path: str) -> float:
        """Get file modification time.

        Returns:
            Modification time as timestamp (0 if file doesn't exist)
        """
        if FileManager.exists(path):
            return os.path.getmtime(path)
        return 0.0

    @staticmethod
    def expanduser(path: str) -> str:
        """Expand ~ in path."""
        return os.path.expanduser(path)

    @staticmethod
    def basename(path: str) -> str:
        """Get basename of path."""
        return os.path.basename(path)

    @staticmethod
    def dirname(path: str) -> str:
        """Get directory name of path."""
        return os.path.dirname(path)

    @staticmethod
    def splitext(path: str) -> tuple:
        """Split path into name and extension."""
        return os.path.splitext(path)

    @staticmethod
    def join(*paths) -> str:
        """Join path components."""
        return os.path.join(*paths)
