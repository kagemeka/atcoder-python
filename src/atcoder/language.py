import dataclasses
import logging
import typing

_LOGGER = logging.getLogger(__name__)


@dataclasses.dataclass
class Language:
    id: int
    text: str
    name: typing.Optional[str] = None
    compiler_or_runtime: typing.Optional[str] = None
    version: typing.Optional[str] = None
    compile_to: typing.Optional[str] = None
    category: typing.Optional[str] = None
    file_extensions: typing.Optional[typing.List[str]] = None


def _download_languages() -> typing.Optional[typing.List[Language]]:
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


_LANGUAGES = _download_languages()
