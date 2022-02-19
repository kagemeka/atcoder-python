from __future__ import annotations

import dataclasses
import logging

import optext.option

_LOGGER = logging.getLogger(__name__)


@dataclasses.dataclass
class Language:
    id: int
    text: str
    name: str
    compiler_or_runtime: str | None = None
    version: str | None = None
    compile_to: str | None = None
    category: str | None = None
    file_extensions: list[str] | None = None


def _parse_language_text(
    language_text: str,
) -> tuple[str, str | None, str | None, str | None]:
    import re

    pattern = re.compile(r"^(.+)\s+\(((.+)\s+)?(.+)\)(;\s+(.+))?.*$")
    match = re.match(pattern, language_text)
    assert match is not None
    _LOGGER.debug(match)
    _LOGGER.debug(match.groups())
    return (
        match[1],
        match[3],
        match[4],
        match[6],
    )


def _download_languages() -> list[Language] | None:
    import pprint

    import requests
    import yaml

    _LANGUAGES_YAML_URL = (
        "https://raw.githubusercontent.com/kagemeka/atcoder-api-python/"
        "main/src/languages.yaml"
    )
    response = requests.get(_LANGUAGES_YAML_URL)
    status = response.status_code
    if response.status_code != 200:
        _LOGGER.error(f"download languages failed: {status}")
        return None
    _LOGGER.info("download lanugages success")
    languages = [
        Language(**language) for language in yaml.safe_load(response.text)
    ]
    _LOGGER.debug(f"downloaded languages: \n{pprint.pformat(languages)}")
    return languages


_LANGUAGES = optext.option.unwrap(_download_languages())


_LANGUAGE_FROM_TEXT: dict[str, Language] | None = None


def _language_from_text(language_text: str) -> Language | None:
    global _LANGUAGE_FROM_TEXT
    if _LANGUAGE_FROM_TEXT is None:
        _LANGUAGE_FROM_TEXT = {
            language.text: language for language in _LANGUAGES
        }
    return _LANGUAGE_FROM_TEXT.get(language_text)


_LANGUAGE_FROM_NAME: dict[str, Language] | None = None


def _language_from_name(language_name: str) -> Language | None:
    global _LANGUAGE_FROM_NAME
    if _LANGUAGE_FROM_NAME is None:
        _LANGUAGE_FROM_NAME = {
            language.name: language for language in _LANGUAGES
        }
    return _LANGUAGE_FROM_NAME.get(language_name)


_LANGUAGE_FROM_COMPILER: dict[str, Language] | None = None


def _language_from_compiler(
    compiler_or_runtime: str,
) -> Language | None:
    global _LANGUAGE_FROM_COMPILER
    if _LANGUAGE_FROM_COMPILER is None:
        _LANGUAGE_FROM_COMPILER = {
            language.compiler_or_runtime: language
            for language in _LANGUAGES
            if language.compiler_or_runtime
        }
    return _LANGUAGE_FROM_COMPILER.get(compiler_or_runtime)
