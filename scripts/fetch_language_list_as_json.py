import atcoder.user_agent
import atcoder.auth
import dataclasses
import pprint
import yaml

import logging

_LOGGER = logging.getLogger(__name__)
_LOGGING_FORMAT = "%(asctime)s %(levelname)s %(pathname)s %(message)s"
logging.basicConfig(
    format=_LOGGING_FORMAT,
    datefmt="%Y-%m-%d %H:%M:%S%z",
    handlers=[logging.StreamHandler()],
    level=logging.DEBUG,
)


def main() -> None:
    credentials = atcoder.auth._input_login_credentials()
    with atcoder.user_agent.UserSessionAgent(credentials) as user:
        languages = user.fetch_languages()

    datas = []
    for language in languages:
        language.file_extensions = []
        data = dataclasses.asdict(language)
        datas.append(data)
    pprint.pprint(datas)
    with open(file="languages.yaml", mode="w", encoding="utf-8") as f:
        yaml.dump(datas, f, default_flow_style=False)
        # json.dump(datas, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
