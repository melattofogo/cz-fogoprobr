import re
from cz_fogoprobr.spec import SCHEMA_PATTERN

def test_schema_match_basic():
    ok = re.match(SCHEMA_PATTERN, "feat: add thing")
    assert ok and ok.group("type") == "feat"

def test_schema_match_scope_breaking():
    ok = re.match(SCHEMA_PATTERN, "fix(api)!: correct timeout")
    assert ok and ok.group("breaking") == "!"
