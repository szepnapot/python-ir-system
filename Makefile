.PHONY: install run clean lint

install:
	python3 -m pip install --user pipenv
	pipenv install

run:
	pipenv run python main.py

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

lint:
	black .
