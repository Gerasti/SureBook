#!/usr/bin/env python3
"""
Integration tests for simple CLI commands.
Tests validate that all user-facing commands work correctly.
"""

import os
import sys
import tempfile
import shutil
import subprocess


class TestEnvironment:
    """Manages temporary test environment with files."""

    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(prefix="workflow_test_")
        self.input_file = os.path.join(self.temp_dir, "input.md")
        self.list_file = os.path.join(self.temp_dir, "lists.md")
        self.toml_file = os.path.join(self.temp_dir, "topics.toml")
        self.topic_save_dir = os.path.join(self.temp_dir, "topics")

        os.makedirs(self.topic_save_dir, exist_ok=True)

    def setup_input_file(self, topics):
        """Create input file with topics."""
        with open(self.input_file, "w", encoding="utf-8") as f:
            for topic in topics:
                f.write(f"{topic}\n")

    def setup_list_file(self, sections):
        """Create list file with sections.
        sections: dict like {"section1": ["topic1", "topic2"], ...}
        """
        with open(self.list_file, "w", encoding="utf-8") as f:
            for section, topics in sections.items():
                f.write(f"## {section} list:\n")
                for topic in topics:
                    f.write(f"{topic}\n\n")

    def setup_toml_file(self):
        """Create basic TOML config."""
        with open(self.toml_file, "w", encoding="utf-8") as f:
            f.write("[settings]\n")
            f.write(f'input = "{self.input_file}"\n')
            f.write(f'list = "{self.list_file}"\n')
            f.write(f'topic_save = "{self.topic_save_dir}"\n')
            f.write('auto_alphabetic_sort = "false"\n')
            f.write('auto_save = "false"\n')
            f.write('editor = "nvim"\n')
            f.write("\n[topics]\n")

    def read_input(self):
        """Read input file contents."""
        if not os.path.exists(self.input_file):
            return []
        with open(self.input_file, encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]

    def read_list(self):
        """Read list file contents."""
        if not os.path.exists(self.list_file):
            return {}
        sections = {}
        current_section = None
        with open(self.list_file, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.endswith("list:"):
                    current_section = line[3:-6].strip()
                    sections[current_section] = []
                elif line and current_section:
                    sections[current_section].append(line)
        return sections

    def cleanup(self):
        """Remove temporary directory."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)


def run_cli(*args, env=None):
    """Run CLI command and return (returncode, stdout, stderr)."""
    cli_path = os.path.join(os.path.dirname(__file__), "cli.py")
    cmd = [sys.executable, cli_path] + list(args)

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        env=env or os.environ.copy()
    )
    return result.returncode, result.stdout, result.stderr


class TestRunner:
    """Test runner with reporting."""

    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []

    def test(self, name, func):
        """Run a test function."""
        print(f"Running: {name}...", end=" ")
        try:
            func()
            print("✓ PASS")
            self.passed += 1
            self.tests.append((name, True, None))
        except AssertionError as e:
            error_msg = str(e) if str(e) else "Assertion failed"
            print(f"✗ FAIL: {error_msg}")
            self.failed += 1
            self.tests.append((name, False, error_msg))
        except Exception as e:
            error_msg = f"Exception: {e}"
            print(f"✗ ERROR: {e}")
            self.failed += 1
            self.tests.append((name, False, error_msg))

    def report(self):
        """Print test summary."""
        print("\n" + "="*60)
        print(f"Tests: {self.passed + self.failed}")
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")

        if self.failed > 0:
            print("\nFailed tests:")
            for name, passed, error in self.tests:
                if not passed:
                    print(f"  - {name}: {error}")

        return self.failed == 0


# ============================================================================
# TEST CASES
# ============================================================================

def test_config(runner):
    """Test config command."""
    def run():
        env = TestEnvironment()
        env.setup_toml_file()

        code, out, err = run_cli("config", env={"TOPICS_TOML_PATH": env.toml_file})

        assert code == 0, f"Command failed: {err}"
        assert "Input:" in out
        assert "List:" in out

        env.cleanup()

    runner.test("config", run)


def test_add_topic_to_input(runner):
    """Test add topic to input."""
    def run():
        env = TestEnvironment()
        env.setup_input_file(["Topic1", "Topic2"])
        env.setup_toml_file()

        code, out, err = run_cli("add", "Topic3", env={"TOPICS_TOML_PATH": env.toml_file})

        assert code == 0, f"Command failed: {err}"
        topics = env.read_input()
        assert "Topic3" in topics
        assert len(topics) == 3

        env.cleanup()

    runner.test("add topic to input", run)


def test_add_topic_to_list(runner):
    """Test add topic to list section."""
    def run():
        env = TestEnvironment()
        env.setup_list_file({"Section1": ["Topic1"]})
        env.setup_input_file([])
        env.setup_toml_file()

        code, out, err = run_cli("add", "Topic2", "to", "Section1",
                                  env={"TOPICS_TOML_PATH": env.toml_file})

        assert code == 0, f"Command failed: {err}"
        sections = env.read_list()
        assert "Topic2" in sections["Section1"]

        env.cleanup()

    runner.test("add topic to list", run)


def test_del_topic(runner):
    """Test del topic."""
    def run():
        env = TestEnvironment()
        env.setup_input_file(["Topic1", "Topic2", "Topic3"])
        env.setup_list_file({"Section1": ["Topic1", "Topic2"]})
        env.setup_toml_file()

        code, out, err = run_cli("del", "Topic2", env={"TOPICS_TOML_PATH": env.toml_file})

        assert code == 0, f"Command failed: {err}"
        topics = env.read_input()
        assert "Topic2" not in topics
        assert "Topic1" in topics

        env.cleanup()

    runner.test("del topic", run)


def test_add_list(runner):
    """Test add list."""
    def run():
        env = TestEnvironment()
        env.setup_list_file({"Section1": []})
        env.setup_input_file([])
        env.setup_toml_file()

        code, out, err = run_cli("add", "list", "Section2",
                                  env={"TOPICS_TOML_PATH": env.toml_file})

        assert code == 0, f"Command failed: {err}"
        sections = env.read_list()
        assert "Section2" in sections

        env.cleanup()

    runner.test("add list", run)


def test_del_list(runner):
    """Test del list with force."""
    def run():
        env = TestEnvironment()
        env.setup_list_file({"Section1": ["Topic1"], "Section2": []})
        env.setup_input_file([])
        env.setup_toml_file()

        code, out, err = run_cli("del", "list", "Section1", "force",
                                  env={"TOPICS_TOML_PATH": env.toml_file})

        assert code == 0, f"Command failed: {err}"
        sections = env.read_list()
        assert "Section1" not in sections
        assert "Section2" in sections

        env.cleanup()

    runner.test("del list force", run)


def test_show_input(runner):
    """Test show input."""
    def run():
        env = TestEnvironment()
        env.setup_input_file(["Topic1", "Topic2", "Topic3"])
        env.setup_toml_file()

        code, out, err = run_cli("show", "input", env={"TOPICS_TOML_PATH": env.toml_file})

        assert code == 0, f"Command failed: {err}"
        assert "Topic1" in out
        assert "Topic2" in out
        assert "Topic3" in out

        env.cleanup()

    runner.test("show input", run)


def test_show_lists(runner):
    """Test show lists."""
    def run():
        env = TestEnvironment()
        env.setup_list_file({"Section1": [], "Section2": []})
        env.setup_input_file([])
        env.setup_toml_file()

        code, out, err = run_cli("show", "lists", env={"TOPICS_TOML_PATH": env.toml_file})

        assert code == 0, f"Command failed: {err}"
        assert "Section1" in out
        assert "Section2" in out

        env.cleanup()

    runner.test("show lists", run)


def test_count(runner):
    """Test count."""
    def run():
        env = TestEnvironment()
        env.setup_input_file(["Topic1", "Topic2"])
        env.setup_list_file({"Section1": ["Topic1", "Topic3"]})
        env.setup_toml_file()

        code, out, err = run_cli("count", env={"TOPICS_TOML_PATH": env.toml_file})

        assert code == 0, f"Command failed: {err}"
        assert "Input topics:" in out
        assert "List topics:" in out

        env.cleanup()

    runner.test("count", run)


def test_compare(runner):
    """Test compare."""
    def run():
        env = TestEnvironment()
        env.setup_input_file(["Topic1", "Topic2"])
        env.setup_list_file({"Section1": ["Topic2", "Topic3"]})
        env.setup_toml_file()

        code, out, err = run_cli("compare", env={"TOPICS_TOML_PATH": env.toml_file})

        assert code == 0, f"Command failed: {err}"
        assert "Topic1" in out or "Topic3" in out

        env.cleanup()

    runner.test("compare", run)


def test_search(runner):
    """Test search."""
    def run():
        env = TestEnvironment()
        env.setup_input_file(["Python Tutorial", "Java Guide"])
        env.setup_list_file({"Section1": ["Python Advanced"]})
        env.setup_toml_file()

        code, out, err = run_cli("search", "Python", env={"TOPICS_TOML_PATH": env.toml_file})

        assert code == 0, f"Command failed: {err}"
        assert "Python" in out

        env.cleanup()

    runner.test("search", run)


def test_sort(runner):
    """Test sort."""
    def run():
        env = TestEnvironment()
        env.setup_input_file(["Zebra", "Apple", "Banana"])
        env.setup_toml_file()

        code, out, err = run_cli("sort", env={"TOPICS_TOML_PATH": env.toml_file})

        assert code == 0, f"Command failed: {err}"
        topics = env.read_input()
        assert topics == ["Apple", "Banana", "Zebra"]

        env.cleanup()

    runner.test("sort", run)


def test_rename_topic(runner):
    """Test rename topic."""
    def run():
        env = TestEnvironment()
        env.setup_input_file(["OldName", "Topic2"])
        env.setup_list_file({"Section1": ["OldName"]})
        env.setup_toml_file()

        code, out, err = run_cli("rename", "OldName", "NewName",
                                  env={"TOPICS_TOML_PATH": env.toml_file})

        assert code == 0, f"Command failed: {err}"
        topics = env.read_input()
        assert "NewName" in topics
        assert "OldName" not in topics

        sections = env.read_list()
        assert "NewName" in sections["Section1"]

        env.cleanup()

    runner.test("rename topic", run)


def test_rename_list(runner):
    """Test rename list."""
    def run():
        env = TestEnvironment()
        env.setup_list_file({"OldSection": ["Topic1"]})
        env.setup_input_file([])
        env.setup_toml_file()

        code, out, err = run_cli("rename", "list", "OldSection", "NewSection",
                                  env={"TOPICS_TOML_PATH": env.toml_file})

        assert code == 0, f"Command failed: {err}"
        sections = env.read_list()
        assert "NewSection" in sections
        assert "OldSection" not in sections

        env.cleanup()

    runner.test("rename list", run)


def test_save(runner):
    """Test save."""
    def run():
        env = TestEnvironment()
        env.setup_input_file(["Topic1", "Topic2"])
        env.setup_list_file({"Section1": ["Topic3"]})
        env.setup_toml_file()

        code, out, err = run_cli("save", env={"TOPICS_TOML_PATH": env.toml_file})

        assert code == 0, f"Command failed: {err}"
        assert "Saved:" in out or "saved:" in out.lower()

        env.cleanup()

    runner.test("save", run)


def test_pure_flag(runner):
    """Test pure flag."""
    def run():
        env = TestEnvironment()
        env.setup_input_file(["Topic1", "Topic2"])
        env.setup_toml_file()

        code, out, err = run_cli("show", "input", "pure",
                                  env={"TOPICS_TOML_PATH": env.toml_file})

        assert code == 0, f"Command failed: {err}"
        # Pure output should not have headers
        assert "Input topics" not in out
        assert "Topic1" in out

        env.cleanup()

    runner.test("pure flag", run)


def test_show_with_limit(runner):
    """Test show with limit."""
    def run():
        env = TestEnvironment()
        env.setup_input_file(["Topic1", "Topic2", "Topic3", "Topic4"])
        env.setup_toml_file()

        code, out, err = run_cli("show", "2", env={"TOPICS_TOML_PATH": env.toml_file})

        assert code == 0, f"Command failed: {err}"
        lines = [l for l in out.split("\n") if l.strip()]
        # Should show only 2 topics
        assert len(lines) == 2

        env.cleanup()

    runner.test("show with limit", run)


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Run all tests."""
    print("="*60)
    print("CLI Integration Tests (Simple Format)")
    print("="*60 + "\n")

    runner = TestRunner()

    # Basic commands
    test_config(runner)
    test_add_topic_to_input(runner)
    test_add_topic_to_list(runner)
    test_del_topic(runner)
    test_add_list(runner)
    test_del_list(runner)

    # Display commands
    test_show_input(runner)
    test_show_lists(runner)
    test_count(runner)
    test_compare(runner)
    test_search(runner)

    # Modification commands
    test_sort(runner)
    test_rename_topic(runner)
    test_rename_list(runner)
    test_save(runner)

    # Options
    test_show_with_limit(runner)
    test_pure_flag(runner)

    # Report
    success = runner.report()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
