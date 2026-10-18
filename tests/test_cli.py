"""End-to-end: run `cz changelog --dry-run` and `cz bump --dry-run` in a temporary git repo.

Requires the package installed in the environment (e.g. `uv sync`), so commitizen
finds the `cz_fogoprobr` entry point.
"""
import os
import subprocess
import sys

import pytest

PYPROJECT = """\
[tool.commitizen]
name = "cz_fogoprobr"
version = "1.0.0"
tag_format = "v$version"
"""


def _run(args, cwd, check=True):
    env = {**os.environ, "PYTHONIOENCODING": "utf-8", "NO_COLOR": "1"}
    result = subprocess.run(
        args, cwd=cwd, env=env, capture_output=True, text=True, encoding="utf-8"
    )
    if check and result.returncode != 0:
        raise AssertionError(
            f"{args} exited {result.returncode}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def _cz(cwd, *args):
    return _run([sys.executable, "-m", "commitizen", *args], cwd)


def _commit(repo, message):
    _run(["git", "commit", "--allow-empty", "-q", "-m", message], repo)


@pytest.fixture
def repo(tmp_path):
    _run(["git", "init", "-q", "-b", "main"], tmp_path)
    _run(["git", "config", "user.name", "Test"], tmp_path)
    _run(["git", "config", "user.email", "test@example.com"], tmp_path)
    _run(["git", "config", "commit.gpgsign", "false"], tmp_path)
    (tmp_path / "pyproject.toml").write_text(PYPROJECT, encoding="utf-8")
    _run(["git", "add", "pyproject.toml"], tmp_path)
    _commit(tmp_path, "chore: initial commit")
    _run(["git", "tag", "-a", "v1.0.0", "-m", "v1.0.0"], tmp_path)
    return tmp_path


def test_changelog_dry_run_lists_all_types(repo):
    for message in [
        "feat(api): add endpoint",
        "fix: correct timeout",
        "docs(readme): explain usage",
        "refactor: split module",
        "perf: cache lookups",
        "test: cover parser",
        "chore(deps): bump lib",
        "feat(auth)!: replace login flow",
    ]:
        _commit(repo, message)

    out = _cz(repo, "changelog", "--dry-run").stdout

    order = ["BREAKING CHANGE", "Feat", "Fix", "Refactor", "Perf", "Docs", "Test", "Chore"]
    for header in order:
        assert f"### {header}" in out, out
    # sections follow change_type_order
    positions = [out.index(f"### {h}") for h in order]
    assert positions == sorted(positions), out
    assert "**api**: add endpoint" in out
    assert "correct timeout" in out
    breaking = out[out.index("### BREAKING CHANGE") : out.index("### Feat")]
    assert "**auth**: replace login flow" in breaking


def test_changelog_dry_run_lists_breaking_change_footer(repo):
    _commit(repo, "feat(auth): rotate tokens\n\nBREAKING CHANGE: old tokens are rejected")

    out = _cz(repo, "changelog", "--dry-run").stdout

    breaking = out[out.index("### BREAKING CHANGE") : out.index("### Feat")]
    assert "old tokens are rejected" in breaking
    assert "**auth**: rotate tokens" in out[out.index("### Feat") :]


@pytest.mark.parametrize(
    "message, expected",
    [
        ("fix: correct timeout", "1.0.1"),
        ("feat: add endpoint", "1.1.0"),
        ("feat!: drop old api", "2.0.0"),
        ("fix(api)!: change contract", "2.0.0"),
        ("refactor(core)!: rename module", "2.0.0"),
        ("feat: new auth\n\nBREAKING CHANGE: tokens rotated", "2.0.0"),
    ],
)
def test_bump_dry_run_increment(repo, message, expected):
    _commit(repo, "docs: unrelated note")
    _commit(repo, message)

    out = _cz(repo, "bump", "--dry-run", "--yes").stdout

    assert f"1.0.0 → {expected}" in out, out


def test_bump_without_eligible_commits_fails(repo):
    _commit(repo, "docs: only docs")

    result = _run(
        [sys.executable, "-m", "commitizen", "bump", "--dry-run", "--yes"], repo, check=False
    )

    assert result.returncode != 0
    assert "[NO_COMMITS_TO_BUMP]" in result.stderr
