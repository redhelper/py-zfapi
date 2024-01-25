sync-deps:
	poetry install --no-root

fmt:
	poetry run autoflake .
	poetry run black .
	poetry run isort .

lint:
	poetry run autoflake --check-diff .
	poetry run black --check --diff .
	poetry run isort --check --diff .
	poetry check

test:
	poetry run pytest -v -s $(test_path)
