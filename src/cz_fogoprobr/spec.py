# everything here is pure data/helpers – no commitizen import
TYPES = [
    {"value": "feat", "name": "feat:     new feature"},
    {"value": "fix", "name": "fix:      bug fix"},
    {"value": "docs", "name": "docs:     documentation"},
    {"value": "refactor", "name": "refactor: refactor"},
    {"value": "perf", "name": "perf:     performance"},
    {"value": "test", "name": "test:     tests"},
    {"value": "chore", "name": "chore:    tooling/chores"},
]

SCHEMA_PATTERN = (
    r"^(?P<type>feat|fix|docs|refactor|perf|test|chore)"
    r"(?:\((?P<scope>[^\)]+)\))?"
    r"(?P<breaking>!)?: (?P<subject>.+)$"
)

# `!` after the type (with or without scope) is a breaking change, like a BREAKING CHANGE footer.
# commitizen matches BUMP_MAP keys as regexes against the captured keyword, in order.
BUMP_PATTERN = r"^((BREAKING[\- ]CHANGE|\w+(\([^\)]*\))?!)|feat|fix)"
BUMP_MAP = {
    r"^.+!$": "MAJOR",
    r"^BREAKING[\- ]CHANGE": "MAJOR",
    r"^feat": "MINOR",
    r"^fix": "PATCH",
}
# while in 0.x, breaking changes bump MINOR (major_version_zero = true)
BUMP_MAP_MAJOR_VERSION_ZERO = {
    r"^.+!$": "MINOR",
    r"^BREAKING[\- ]CHANGE": "MINOR",
    r"^feat": "MINOR",
    r"^fix": "PATCH",
}
CHANGELOG_PATTERN = r"^(feat|fix|docs|refactor|perf|test|chore)"
# also parses `BREAKING CHANGE: ...` footer blocks in the body (commitizen scans each body block)
COMMIT_PARSER = (
    r"^(?P<change_type>feat|fix|docs|refactor|perf|test|chore|BREAKING CHANGE)"
    r"(?:\((?P<scope>[^\)]+)\))?"
    r"(?P<breaking>!)?: (?P<message>.+)$"
)
CHANGE_TYPE_MAP = {
    "feat": "Feat",
    "fix": "Fix",
    "refactor": "Refactor",
    "perf": "Perf",
    "docs": "Docs",
    "test": "Test",
    "chore": "Chore",
}
CHANGE_TYPE_ORDER = ["BREAKING CHANGE", "Feat", "Fix", "Refactor", "Perf", "Docs", "Test", "Chore"]
