poetry run isort .
poetry run black .
poetry run pytest --asyncio-mode=strict