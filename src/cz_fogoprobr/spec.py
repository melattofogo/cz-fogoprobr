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

BUMP_PATTERN = r"^(BREAKING CHANGE|feat|fix)"
BUMP_MAP = {"BREAKING CHANGE": "MAJOR", "feat": "MINOR", "fix": "PATCH"}
CHANGELOG_PATTERN = r"^(feat|fix|docs|refactor|perf|test|chore)"
