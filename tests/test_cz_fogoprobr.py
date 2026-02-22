import sys
import os
import re
import pytest
from unittest.mock import MagicMock

# Add src to sys.path to ensure we can import the local version
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from cz_fogoprobr.base import CzFogoprobr
from cz_fogoprobr.spec import SCHEMA_PATTERN

@pytest.fixture
def mock_config():
    config = MagicMock()
    config.settings = {"style": []}
    return config

def test_schema_match_basic():
    ok = re.match(SCHEMA_PATTERN, "feat: add thing")
    assert ok and ok.group("type") == "feat"

def test_schema_match_scope_breaking():
    ok = re.match(SCHEMA_PATTERN, "fix(api)!: correct timeout")
    assert ok and ok.group("breaking") == "!"

def test_message_with_body(mock_config):
    cz = CzFogoprobr(mock_config)
    answers = {
        "type": "feat",
        "scope": "api",
        "is_breaking": False,
        "subject": "add OAuth authentication",
        "body": "Added OAuth authentication support to the API service."
    }
    msg = cz.message(answers)
    expected = "feat(api): add OAuth authentication\n\nAdded OAuth authentication support to the API service."
    assert msg == expected

def test_message_without_body(mock_config):
    cz = CzFogoprobr(mock_config)
    answers = {
        "type": "fix",
        "scope": "",
        "is_breaking": True,
        "subject": "fix critical bug",
        "body": ""
    }
    msg = cz.message(answers)
    assert msg == "fix!: fix critical bug"
