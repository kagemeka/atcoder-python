import yaml


def main() -> None:
    with open(file="src/languages.yaml", mode="r", encoding="utf-8") as f:
        datas = yaml.load(f, yaml.Loader)
    print(datas)


if __name__ == "__main__":
    main()
