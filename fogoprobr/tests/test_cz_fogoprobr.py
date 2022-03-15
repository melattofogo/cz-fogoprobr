import pytest

from commitizen import defaults
from commitizen.config import BaseConfig

from cz_fogoprobr import (
    FogoprobrCz,
    parse_scope,
    parse_subject,
)
from commitizen.cz.exceptions import AnswerRequiredError

valid_scopes = ["", "simple", "dash-separated", "camelCase" "UPPERCASE"]

scopes_transformations = [["with spaces", "with-spaces"], [None, ""]]

valid_subjects = ["this is a normal text", "aword"]

subjects_transformations = [["with dot.", "with dot"]]

invalid_subjects = ["", "   ", ".", "   .", "", None]

@pytest.fixture()
def config():
    _config = BaseConfig()
    _config.settings.update({"name": defaults.DEFAULT_SETTINGS["name"]})
    return _config

# testa entradas validas em scope
def test_parse_scope_valid_values():
    for valid_scope in valid_scopes:
        assert valid_scope == parse_scope(valid_scope)

# testa transformacao em entradas invalidas de scope
def test_scopes_transformations():
    for scopes_transformation in scopes_transformations:
        invalid_scope, transformed_scope = scopes_transformation
        assert transformed_scope == parse_scope(invalid_scope)


# testa entradas validas em subject
def test_parse_subject_valid_values():
    for valid_subject in valid_subjects:
        assert valid_subject == parse_subject(valid_subject)

# testa AnswerRequiredError no caso de entradas invalidas em subject
def test_parse_subject_invalid_values():
    for valid_subject in invalid_subjects:
        with pytest.raises(AnswerRequiredError):
            parse_subject(valid_subject)

# testa transformacao em entradas invalidas de subject
def test_subject_transformations():
    for subject_transformation in subjects_transformations:
        invalid_subject, transformed_subject = subject_transformation
        assert transformed_subject == parse_subject(invalid_subject)

# testa estrutura de questions
def test_questions(config):
    cz_commits = FogoprobrCz(config)
    questions = cz_commits.questions()
    # deve ser uma lista
    assert isinstance(questions, list)
    # primeiro entrada deve ser um dicionario
    assert isinstance(questions[0], dict)

# testa existencia de keyboard shortcuts para cada tipo de alteracao
def test_choices_all_have_keyboard_shortcuts(config):
    cz_commits = FogoprobrCz(config)
    questions = cz_commits.questions()
    
    list_questions = (q for q in questions if q["type"] == "list")
    for select in list_questions:
        assert all("key" in choice for choice in select["choices"])


def test_small_answer(config):
    cz_commits = FogoprobrCz(config)
    answers = {
        "prefix": "fix",
        "scope": "users",
        "subject": "email pattern corrected",
        "body": "",
    }
    message = cz_commits.message(answers)
    assert message == "fix(users): email pattern corrected"


def test_long_answer(config):
    cz_commits = FogoprobrCz(config)
    answers = {
        "prefix": "fix",
        "scope": "users",
        "subject": "email pattern corrected",
        "body": "complete content",
    }
    message = cz_commits.message(answers)
    assert (
        message
        == "fix(users): email pattern corrected\n\ncomplete content"
    )

# testa que o examplo retorna str
def test_example(config):
    """just testing a string is returned. not the content"""
    cz_commits = FogoprobrCz(config)
    example = cz_commits.example()
    assert isinstance(example, str)

# testa que o schema retorna str
def test_schema(config):
    """just testing a string is returned. not the content"""
    cz_commits = FogoprobrCz(config)
    schema = cz_commits.schema()
    assert isinstance(schema, str)

# testa que o info retorna str
def test_info(config):
    """just testing a string is returned. not the content"""
    cz_commits = FogoprobrCz(config)
    info = cz_commits.info()
    assert isinstance(info, str)
