#!/usr/bin/env python3
"""Read-only checks for this method package; Python standard library and Git only."""

import argparse
import collections
import posixpath
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
ROOT_FILES = {".gitignore", "LICENSE", "README.md", "README.en.md", "AGENTS.md", "CONTRIBUTING.md"}
REQUIRED = ROOT_FILES | {
    "docs/PRD.md", "docs/DESIGN.md", "docs/TASKS.md", "docs/ADOPTION.md",
    "docs/EXAMPLE.md", "docs/reviews/README.md", "scripts/check_docs.py", "tests/test_check_docs.py",
}
HISTORY = "docs/reviews/initialization-review.md"
STATES = ("TODO", "IN_PROGRESS", "BLOCKED", "REVIEW", "DONE")
FACTS = {"CONFIRMED", "INFERRED", "TODO_CONFIRM"}


def release_path(name):
    """The explicit release surface; add new asset types deliberately."""
    parts = Path(name).parts
    if name.startswith("/") or ".." in parts:
        return False
    return name in ROOT_FILES or (
        len(parts) > 1 and (
            (parts[0] == "docs" and name.endswith(".md"))
            or (parts[0] in {"scripts", "tests"} and name.endswith(".py"))
        ) and not any(part.startswith(".") or part == "__pycache__" for part in parts)
    )


def workspace_files(root):
    files = {}
    candidates = [root / name for name in ROOT_FILES]
    for directory, suffix in (("docs", "*.md"), ("scripts", "*.py"), ("tests", "*.py")):
        base = root / directory
        if base.is_symlink():
            raise ValueError(f"{directory}: release directory cannot be a symlink")
        if base.is_dir():
            candidates.extend(base.rglob(suffix))
    for path in sorted(candidates):
        name = path.relative_to(root).as_posix()
        if not release_path(name) or not path.exists():
            continue
        if path.is_symlink():
            raise ValueError(f"{name}: release asset cannot be a symlink")
        if path.is_file():
            try:
                files[name] = path.read_text(encoding="utf-8")
            except UnicodeError as error:
                raise ValueError(f"{name}: release asset is not UTF-8") from error
    return files


def without_fences(text):
    output, fence = [], None
    for line in text.splitlines():
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            output.append("")
        else:
            output.append(line if fence is None else "")
    return "\n".join(output)


def anchors(text):
    result, counts = set(), collections.Counter()
    for heading in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", without_fences(text), re.M):
        heading = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", heading)
        heading = re.sub(r"<[^>]+>", "", heading).lower()
        slug = re.sub(r"[^\w\- ]", "", heading)
        slug = re.sub(r"\s", "-", slug)
        count = counts[slug]
        counts[slug] += 1
        result.add(f"{slug}-{count}" if count else slug)
    return result


def check_links(name, text, files):
    errors = []
    for target in re.findall(r"!?\[[^\]\n]*\]\(([^)\n]+)\)", without_fences(text)):
        target = target.strip().strip("<>")
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc:
            continue  # Network destinations are deliberately not fetched.
        path = unquote(parsed.path)
        normalized = posixpath.normpath(posixpath.join(posixpath.dirname(name), path)) if path else name
        if normalized.startswith("/") or normalized == ".." or normalized.startswith("../"):
            errors.append(f"{name}: link escapes release root: {target}")
        elif normalized not in files:
            errors.append(f"{name}: missing link target: {target}")
        elif parsed.fragment and unquote(parsed.fragment) not in anchors(files[normalized]):
            errors.append(f"{name}: missing anchor: {target}")
    return errors


def sections(text, prefix, level):
    pattern = rf"^{'#' * level} ({prefix}-\d+) [^\n]*\n(.*?)(?=^#{{1,{level}}} |\Z)"
    return re.findall(pattern, without_fences(text), re.M | re.S)


def field(block, name):
    match = re.search(rf"^- {re.escape(name)}：([^\n]*)", block, re.M)
    return match.group(1).strip().rstrip("。") if match else None


def check_traceability(files):
    errors = []
    requirements = sections(files.get("docs/PRD.md", ""), "REQ", 3)
    designs = sections(files.get("docs/DESIGN.md", ""), "DESIGN", 2)
    tasks = sections(files.get("docs/TASKS.md", ""), "TASK", 2)
    for name, values in (("PRD", requirements), ("DESIGN", designs), ("TASKS", tasks)):
        if not values or len(dict(values)) != len(values):
            errors.append(f"{name}: missing or duplicate tracking IDs")
    req_ids, design_ids, task_map = set(dict(requirements)), set(dict(designs)), dict(tasks)
    fact_counts = collections.Counter()
    for ident, block in requirements:
        match = re.search(r"^- 事实等级：\*\*(\w+)\*\*", block, re.M)
        if not match or match.group(1) not in FACTS:
            errors.append(f"docs/PRD.md: {ident}: invalid fact grade")
        else:
            fact_counts[match.group(1)] += 1
        if "验收" not in block:
            errors.append(f"docs/PRD.md: {ident}: missing acceptance criteria")
    req_summary = re.search(r"需求共 (\d+) 项：CONFIRMED (\d+)、INFERRED (\d+)、TODO_CONFIRM (\d+)", files.get("docs/PRD.md", ""))
    req_expected = [len(requirements), fact_counts["CONFIRMED"], fact_counts["INFERRED"], fact_counts["TODO_CONFIRM"]]
    if not req_summary or list(map(int, req_summary.groups())) != req_expected:
        errors.append(f"docs/PRD.md: requirement statistics must equal {req_expected}")
    design_rows = [line.split("|")[1:-1] for line in files.get("docs/DESIGN.md", "").splitlines()
                   if re.match(r"^\| DESIGN-\d+ \|", line)]
    if {row[0].strip() for row in design_rows} != design_ids:
        errors.append("docs/DESIGN.md: design index differs from design sections")
    for row in design_rows:
        if row[-1].strip() not in {"DRAFT", "REVIEW", "APPROVED", "BLOCKED"}:
            errors.append(f"docs/DESIGN.md: {row[0].strip()}: invalid design state")
        if not any(fact in "|".join(row) for fact in FACTS):
            errors.append(f"docs/DESIGN.md: {row[0].strip()}: missing fact grade")
        for ref in re.findall(r"REQ-\d+", "|".join(row)):
            if ref not in req_ids:
                errors.append(f"docs/DESIGN.md: unknown requirement {ref}")
    design_counts = collections.Counter(row[-1].strip() for row in design_rows)
    design_summary = re.search(r"共 (\d+) 项：APPROVED (\d+)、REVIEW (\d+)、DRAFT (\d+)、BLOCKED (\d+)", files.get("docs/DESIGN.md", ""))
    design_expected = [len(designs)] + [design_counts[state] for state in ("APPROVED", "REVIEW", "DRAFT", "BLOCKED")]
    if not design_summary or list(map(int, design_summary.groups())) != design_expected:
        errors.append(f"docs/DESIGN.md: design statistics must equal {design_expected}")
    dependencies, statuses = {}, {}
    required_fields = ("PRD", "DESIGN", "Priority", "Status", "Depends On", "Owner",
                       "Target Module", "Target Files", "Target API / Method", "Implementation", "Acceptance Criteria")
    for ident, block in tasks:
        for key in required_fields:
            if field(block, key) is None:
                errors.append(f"docs/TASKS.md: {ident}: missing {key}")
        statuses[ident] = field(block, "Status")
        if statuses[ident] not in STATES:
            errors.append(f"docs/TASKS.md: {ident}: invalid task status")
        if statuses[ident] in {"IN_PROGRESS", "REVIEW", "DONE"}:
            if not field(block, "Owner") or field(block, "Owner") == "未分配":
                errors.append(f"docs/TASKS.md: {ident}: assigned owner required")
            if not field(block, "Claimed At"):
                errors.append(f"docs/TASKS.md: {ident}: Claimed At required")
        if field(block, "Priority") not in {"P0", "P1", "P2", "P3"}:
            errors.append(f"docs/TASKS.md: {ident}: invalid priority")
        for key, pattern, known in (("PRD", r"REQ-\d+", req_ids), ("DESIGN", r"DESIGN-\d+", design_ids)):
            refs = re.findall(pattern, field(block, key) or "")
            if not refs:
                errors.append(f"docs/TASKS.md: {ident}: no {key} binding")
            for ref in refs:
                if ref not in known:
                    errors.append(f"docs/TASKS.md: {ident}: unknown {ref}")
        dependencies[ident] = re.findall(r"TASK-\d+", field(block, "Depends On") or "")
        for dep in dependencies[ident]:
            if dep not in task_map:
                errors.append(f"docs/TASKS.md: {ident}: unknown dependency {dep}")
        if statuses[ident] == "DONE":
            for key in ("Completed By", "Completed At", "Review"):
                if not field(block, key):
                    errors.append(f"docs/TASKS.md: {ident}: DONE missing {key}")
            report = (field(block, "Review") or "").strip("`。 ")
            if report not in files:
                errors.append(f"docs/TASKS.md: {ident}: missing DONE review {report}")
            else:
                review = files[report]
                for key in ("Reviewer", "Date"):
                    if not field(review, key):
                        errors.append(f"{report}: DONE review missing {key}")
                conclusion = re.search(r"^- (?:Conclusion|当前结论)：(PASS_WITH_CONDITIONS|PASS|FAIL)\s*$", review, re.M)
                if not conclusion or conclusion.group(1) == "FAIL":
                    errors.append(f"{report}: DONE requires passing review conclusion")
                elif conclusion.group(1) == "PASS_WITH_CONDITIONS" and field(review, "Conditions Resolved") != "yes":
                    errors.append(f"{report}: DONE requires resolved review conditions")
                for line in review.splitlines():
                    cells = [cell.strip() for cell in line.split("|")[1:-1]]
                    if any(cell in {"P0", "P1"} for cell in cells):
                        if any(cell in {"OPEN", "FIXED"} for cell in cells):
                            errors.append(f"{report}: unresolved P0/P1 blocks DONE")
                        if "REJECTED" in cells and not (field(review, "Rejection Approved By") and field(review, "Rejection Evidence")):
                            errors.append(f"{report}: rejected P0/P1 requires approval and evidence")
    for ident, deps in dependencies.items():
        if statuses[ident] in {"IN_PROGRESS", "REVIEW", "DONE"}:
            for dep in deps:
                if dep in statuses and statuses[dep] != "DONE":
                    errors.append(f"docs/TASKS.md: {ident}: dependency {dep} is not DONE")
    visiting, visited = set(), set()

    def visit(ident):
        if ident in visiting:
            errors.append(f"docs/TASKS.md: dependency cycle at {ident}")
            return
        if ident in visited or ident not in dependencies:
            return
        visiting.add(ident)
        for dep in dependencies[ident]:
            visit(dep)
        visiting.remove(ident)
        visited.add(ident)

    for ident in dependencies:
        visit(ident)
    counts = collections.Counter(statuses.values())
    expected = [len(tasks)] + [counts[state] for state in STATES]
    board = re.search(r"^\| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \|$", files.get("docs/TASKS.md", ""), re.M)
    if not board or list(map(int, board.groups())) != expected:
        errors.append(f"docs/TASKS.md: dashboard must equal {expected}")
    return errors


def check_snapshot(files):
    errors = [f"missing required release asset: {name}" for name in sorted(REQUIRED - files.keys())]
    for name, text in sorted(files.items()):
        if not text.endswith("\n"):
            errors.append(f"{name}: missing final newline")
        for number, line in enumerate(text.splitlines(), 1):
            if line.rstrip() != line:
                errors.append(f"{name}:{number}: trailing whitespace")
        if name.endswith(".md"):
            errors.extend(check_links(name, text, files))
            if re.search(r"/(?:Users|home)/[^\s/]+/|[A-Za-z]:\\(?:Users|Documents)\\", text):
                errors.append(f"{name}: personal machine path")
            if name != HISTORY and re.search(r"/(?:private/)?tmp/[^\s`]+", text):
                errors.append(f"{name}: unshipped machine path dependency")
    license_text = files.get("LICENSE", "")
    if not (license_text.startswith("MIT License\n") and
            "Copyright (c) 2026 agent-matrix contributors" in license_text and
            'THE SOFTWARE IS PROVIDED "AS IS"' in license_text):
        errors.append("LICENSE: expected MIT license and confirmed attribution")
    for name in ("README.md", "README.en.md"):
        if re.search(r"\bxxxx\b|软件架构说明|Software architecture description", files.get(name, "")):
            errors.append(f"{name}: initialization placeholder remains")
    guide = files.get("docs/ADOPTION.md", "")
    for title in ("初始化 Prompt", "AGENTS 最小模板", "PRD 最小契约模板", "DESIGN 最小契约模板", "TASKS 最小契约模板"):
        if title not in guide:
            errors.append(f"docs/ADOPTION.md: missing {title}")
    errors.extend(check_traceability(files))
    return errors


def git_output(root, *args):
    result = subprocess.run(["git", *args], cwd=root, capture_output=True)
    if result.returncode:
        raise ValueError("Git read failed: " + result.stderr.decode("utf-8", errors="replace").strip())
    return result.stdout


def check_staged(root):
    errors, files = [], {}
    if git_output(root, "ls-files", "--unmerged"):
        errors.append("index has unresolved conflicts")
    names = git_output(root, "ls-files", "--cached", "-z").decode("utf-8").split("\0")
    for name in sorted(set(names) - {""}):
        if not release_path(name):
            errors.append(f"{name}: not a release asset; keep local files out of the index")
            continue
        mode = git_output(root, "ls-files", "--stage", "--", name).split(b" ", 1)[0]
        if mode == b"120000":
            errors.append(f"{name}: release symlink is not allowed")
            continue
        try:
            files[name] = git_output(root, "show", ":" + name).decode("utf-8").replace("\r\n", "\n")
        except UnicodeError:
            errors.append(f"{name}: staged release asset is not UTF-8")
    errors.extend(check_snapshot(files))
    workspace = workspace_files(root)
    for name, text in workspace.items():
        if name not in files:
            errors.append(f"{name}: release asset not staged")
        elif text.replace("\r\n", "\n") != files[name]:
            errors.append(f"{name}: workspace differs from index; stage the reviewed version")
    for name in files.keys() - workspace.keys():
        errors.append(f"{name}: index asset is missing from workspace")
    return errors


def run_example(text, red=False):
    namespace = {}
    try:
        for marker in ("tests", "red" if red else "green"):
            match = re.search(rf"<!-- example:{marker} -->\s*```python\n(.*?)\n```", text, re.S)
            if not match:
                return False, f"Missing example block: {marker}"
            exec(compile(match.group(1), f"EXAMPLE:{marker}", "exec"), namespace)
        count = namespace["run_example_tests"](namespace["normalize_percent"])
    except AssertionError as error:
        return (True, f"RED detected expected defect: {error}") if red else (False, f"GREEN failed: {error}")
    except Exception as error:
        return False, f"Example execution failed: {type(error).__name__}: {error}"
    if red:
        return False, "RED unexpectedly passed; tests did not detect the seeded defect"
    return count == 14, f"GREEN: {count}/14 boundary and type cases passed"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--staged", action="store_true", help="check the actual Git index and workspace agreement")
    modes.add_argument("--example", action="store_true", help="execute the documented green example in memory")
    modes.add_argument("--example-red", action="store_true", help="require tests to detect the documented seeded defect")
    args = parser.parse_args()
    try:
        if args.example or args.example_red:
            success, message = run_example((ROOT / "docs/EXAMPLE.md").read_text(encoding="utf-8"), red=args.example_red)
            print(message)
            return 0 if success else 1
        errors = check_staged(ROOT) if args.staged else check_snapshot(workspace_files(ROOT))
    except (OSError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if errors:
        print(f"FAIL: {len(errors)} error(s)", file=sys.stderr)
        return 1
    print("PASS: " + ("staged release matches the reviewed workspace" if args.staged else "release documents and traceability"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
