poetry update
poetry run isort .
poetry run black .
poetry run mypy .
poetry run pflake8 .
poetry run pytest --asyncio-mode=strict --verbose
