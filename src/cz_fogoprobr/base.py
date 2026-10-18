from __future__ import annotations
from typing import List, Dict, Any
import re
from commitizen.cz.base import BaseCommitizen
from commitizen.git import GitCommit

from .spec import (
    TYPES, SCHEMA_PATTERN, BUMP_PATTERN, BUMP_MAP, BUMP_MAP_MAJOR_VERSION_ZERO,
    CHANGELOG_PATTERN, COMMIT_PARSER, CHANGE_TYPE_MAP, CHANGE_TYPE_ORDER,
)

class CzFogoprobr(BaseCommitizen):
    # commitizen reads these as class attributes (not methods) in cz bump / cz changelog
    bump_pattern = BUMP_PATTERN
    bump_map = BUMP_MAP
    bump_map_major_version_zero = BUMP_MAP_MAJOR_VERSION_ZERO
    changelog_pattern = CHANGELOG_PATTERN
    commit_parser = COMMIT_PARSER
    change_type_map = CHANGE_TYPE_MAP
    change_type_order = CHANGE_TYPE_ORDER

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
            {
                "type": "input",
                "name": "body",
                "message": "Long description (optional, use \\n for newlines):",
                "filter": str.strip,
            },
        ]

    def message(self, answers: Dict[str, Any]) -> str:
        t = answers["type"]
        scope = f"({answers['scope']})" if answers.get("scope") else ""
        bang = "!" if answers.get("is_breaking") else ""
        subject = answers["subject"]
        body = answers.get("body")

        msg = f"{t}{scope}{bang}: {subject}"
        if body:
            msg = f"{msg}\n\n{body}"
        return msg

    def changelog_message_builder_hook(
        self, parsed_message: Dict[str, Any], commit: GitCommit
    ) -> Dict[str, Any]:
        # `type!:` commits go to the BREAKING CHANGE section instead of their type's
        if parsed_message.get("breaking"):
            parsed_message["change_type"] = "BREAKING CHANGE"
        return parsed_message

    def subject(self, commit: GitCommit) -> str:
        first = commit.message.splitlines()[0]
        m = re.match(SCHEMA_PATTERN, first)
        if not m:
            return first
        scope = f"({m.group('scope')})" if m.group('scope') else ""
        return f"{m.group('type')}{scope}: {m.group('subject')}"
