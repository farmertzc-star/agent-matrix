"""Regression tests for release failures, using disposable Git repositories."""

import importlib.util
import re
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("check_docs", ROOT / "scripts/check_docs.py")
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)


class DocumentChecks(unittest.TestCase):
    def setUp(self):
        self.files = checker.workspace_files(ROOT)
        # A valid fixture independent of README work in progress, not a release check.
        for name in ("README.md", "README.en.md"):
            self.files[name] = (
                "# agent-matrix\n\n[Adoption](docs/ADOPTION.md)\n"
                "[Example](docs/EXAMPLE.md)\n[Contributing](CONTRIBUTING.md)\n"
                "[License](LICENSE)\n"
            )

    def assert_rejected(self, fragment):
        errors = checker.check_snapshot(self.files)
        self.assertTrue(any(fragment in error for error in errors), errors)

    def test_valid_snapshot(self):
        self.assertEqual([], checker.check_snapshot(self.files))

    def test_missing_local_link(self):
        self.files["AGENTS.md"] += "\n[Missing](docs/not-present.md)\n"
        self.assert_rejected("link target")

    def test_missing_anchor(self):
        self.files["AGENTS.md"] += "\n[Missing](docs/DESIGN.md#not-a-heading)\n"
        self.assert_rejected("anchor")

    def test_unicode_and_encoded_space_link(self):
        self.files["docs/space guide.md"] = "# 中文标题\n"
        self.files["AGENTS.md"] += "\n[Guide](docs/space%20guide.md#中文标题)\n"
        self.assertEqual([], checker.check_snapshot(self.files))

    def test_link_cannot_escape_release_root(self):
        self.files["AGENTS.md"] += "\n[Escape](../outside.md)\n"
        self.assert_rejected("escapes")

    def test_unknown_requirement(self):
        self.files["docs/TASKS.md"] = self.files["docs/TASKS.md"].replace(
            "- PRD：REQ-004", "- PRD：REQ-999", 1
        )
        self.assert_rejected("REQ-999")

    def test_invalid_fact_grade(self):
        self.files["docs/PRD.md"] = self.files["docs/PRD.md"].replace(
            "- 事实等级：**CONFIRMED**", "- 事实等级：**GUESSED**", 1
        )
        self.assert_rejected("fact grade")

    def test_requirement_statistics_mismatch(self):
        self.files["docs/PRD.md"] = self.files["docs/PRD.md"].replace("需求共 9 项", "需求共 99 项", 1)
        self.assert_rejected("requirement statistics")

    def test_design_statistics_mismatch(self):
        self.files["docs/DESIGN.md"] = self.files["docs/DESIGN.md"].replace("共 6 项：", "共 99 项：", 1)
        self.assert_rejected("design statistics")

    def test_missing_task_field(self):
        self.files["docs/TASKS.md"] = re.sub(
            r"^- Target Module：[^\n]*\n", "", self.files["docs/TASKS.md"], count=1, flags=re.M
        )
        self.assert_rejected("Target Module")

    def test_dashboard_mismatch(self):
        self.files["docs/TASKS.md"] = re.sub(
            r"^\| \d+ \| \d+ \| \d+ \| \d+ \| \d+ \| \d+ \|$",
            "| 999 | 0 | 0 | 0 | 0 | 0 |",
            self.files["docs/TASKS.md"], count=1, flags=re.M,
        )
        self.assert_rejected("dashboard")

    def test_unknown_dependency(self):
        self.files["docs/TASKS.md"] = self.files["docs/TASKS.md"].replace(
            "- Depends On：无", "- Depends On：TASK-999", 1
        )
        self.assert_rejected("TASK-999")

    def test_dependency_cycle(self):
        self.files["docs/TASKS.md"] = self.files["docs/TASKS.md"].replace(
            "- Depends On：无", "- Depends On：TASK-002", 1
        )
        self.assert_rejected("cycle")

    def test_done_requires_registration(self):
        self.files["docs/TASKS.md"] = re.sub(
            r"^- Completed By：[^\n]*\n", "", self.files["docs/TASKS.md"], count=1, flags=re.M
        )
        self.assert_rejected("Completed By")

    def test_done_requires_passing_review(self):
        self.files["docs/reviews/TASK-001-review.md"] = self.files[
            "docs/reviews/TASK-001-review.md"
        ].replace("- Conclusion：PASS", "- Conclusion：FAIL", 1)
        self.assert_rejected("review conclusion")

    def test_done_review_requires_reviewer_identity(self):
        self.files["docs/reviews/TASK-001-review.md"] = re.sub(
            r"^- Reviewer：[^\n]*\n", "", self.files["docs/reviews/TASK-001-review.md"], flags=re.M
        )
        self.assert_rejected("missing Reviewer")

    def test_conditional_review_cannot_silently_complete(self):
        self.files["docs/reviews/TASK-001-review.md"] = self.files[
            "docs/reviews/TASK-001-review.md"
        ].replace("- Conclusion：PASS", "- Conclusion：PASS_WITH_CONDITIONS", 1)
        self.assert_rejected("resolved review conditions")

    def test_rejected_high_issue_requires_approval(self):
        self.files["docs/reviews/TASK-001-review.md"] += (
            "\n| R-I001 | P1 | Reviewer | Dispute | Evidence | Impact | Reject | REJECTED | Pending |\n"
        )
        self.assert_rejected("approval and evidence")

    def test_claimed_task_requires_real_owner(self):
        self.files["docs/TASKS.md"] = self.files["docs/TASKS.md"].replace("- Owner：Codex", "- Owner：未分配", 1)
        self.assert_rejected("assigned owner")

    def test_unresolved_high_issue_blocks_done(self):
        self.files["docs/reviews/TASK-001-review.md"] += (
            "\n| R-I001 | P1 | Reviewer | Defect | Evidence | Impact | Fix | OPEN | Pending |\n"
        )
        self.assert_rejected("unresolved P0/P1")

    def test_personal_path_rejected(self):
        self.files["AGENTS.md"] += "\nUse /Users/example/project to run checks.\n"
        self.assert_rejected("machine path")

    def test_new_temp_dependency_rejected(self):
        self.files["AGENTS.md"] += "\npython3 /private/tmp/unshipped-check.py\n"
        self.assert_rejected("machine path")

    def test_missing_license(self):
        del self.files["LICENSE"]
        self.assert_rejected("LICENSE")

    def test_example_green(self):
        success, message = checker.run_example(self.files["docs/EXAMPLE.md"])
        self.assertTrue(success, message)
        self.assertIn("14", message)

    def test_example_red_is_detected(self):
        success, message = checker.run_example(self.files["docs/EXAMPLE.md"], red=True)
        self.assertTrue(success, message)
        self.assertIn("detected", message)

    def test_red_must_not_pass(self):
        text = self.files["docs/EXAMPLE.md"].replace(
            "return min(value, 100)", "return max(0, min(value, 100))"
        )
        success, _ = checker.run_example(text, red=True)
        self.assertFalse(success)


class StagedChecks(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="agent-matrix-tests-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        files = checker.workspace_files(ROOT)
        for name in ("README.md", "README.en.md"):
            files[name] = "# agent-matrix\n\n[Adoption](docs/ADOPTION.md)\n"
        for name, content in files.items():
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        self.git("init", "--quiet")
        self.git("add", "--", ".")

    def git(self, *args):
        return subprocess.run(
            ["git", *args], cwd=self.root, capture_output=True, text=True, check=True
        ).stdout

    def test_staged_matches_workspace(self):
        self.assertEqual([], checker.check_staged(self.root))

    def test_staged_old_version_rejected(self):
        target = self.root / "README.md"
        target.write_text(target.read_text() + "\nUnstaged change.\n")
        errors = checker.check_staged(self.root)
        self.assertTrue(any("differs from index" in error for error in errors), errors)

    def test_unstaged_public_asset_rejected(self):
        (self.root / "docs/new-guide.md").write_text("# New guide\n")
        errors = checker.check_staged(self.root)
        self.assertTrue(any("not staged" in error for error in errors), errors)

    def test_staged_local_config_rejected(self):
        target = self.root / ".idea/workspace.xml"
        target.parent.mkdir(exist_ok=True)
        target.write_text("<local/>\n")
        self.git("add", "--force", "--", ".idea/workspace.xml")
        errors = checker.check_staged(self.root)
        self.assertTrue(any("not a release asset" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
