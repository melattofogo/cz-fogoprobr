from __future__ import annotations
from typing import List, Dict, Any
import re
from commitizen.cz.base import BaseCommitizen
from commitizen.git import GitCommit

from .spec import (
    TYPES, SCHEMA_PATTERN, BUMP_PATTERN, BUMP_MAP, CHANGELOG_PATTERN
)

class CzFogoprobr(BaseCommitizen):
    def info(self) -> str:
        return "fogoprobr Commitizen convention (strict header, optional scope, optional breaking '!')."

    def example(self) -> str:
        return "feat(auth)!: add OAuth2 login"

    def schema(self) -> str:
        return "<type>(<scope>)!: <subject>"

    def schema_pattern(self) -> str:
        return SCHEMA_PATTERN

    def questions(self) -> List[Dict[str, Any]]:
        return [
            {"type": "list", "name": "type", "message": "Select the type:", "choices": TYPES},
            {"type": "input", "name": "scope", "message": "Scope (optional):"},
            {"type": "confirm", "name": "is_breaking", "message": "Breaking change?", "default": False},
            {
                "type": "input",
                "name": "subject",
                "message": "Short, imperative subject:",
                "filter": str.strip,
                "validate": lambda s: 5 <= len(s) <= 72,
            },
        ]

    def message(self, answers: Dict[str, Any]) -> str:
        t = answers["type"]
        scope = f"({answers['scope']})" if answers.get("scope") else ""
        bang = "!" if answers.get("is_breaking") else ""
        subject = answers["subject"]
        return f"{t}{scope}{bang}: {subject}"

    def bump_pattern(self) -> str:
        return BUMP_PATTERN

    def bump_map(self) -> Dict[str, str]:
        return BUMP_MAP

    def changelog_pattern(self) -> str:
        return CHANGELOG_PATTERN

    def subject(self, commit: GitCommit) -> str:
        first = commit.message.splitlines()[0]
        m = re.match(SCHEMA_PATTERN, first)
        if not m:
            return first
        scope = f"({m.group('scope')})" if m.group('scope') else ""
        return f"{m.group('type')}{scope}: {m.group('subject')}"
