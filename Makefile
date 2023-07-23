PATH := $(HOME)/.local/bin:$(PATH)

install:
	pip3 install --upgrade -r test/requirements.txt

install-user:
	pip3 install --user --upgrade -r test/requirements.txt

lint:
	flake8 --version
	flake8 rplugin
	mypy --version
	mypy --ignore-missing-imports --follow-imports=skip --strict rplugin/python3/deoppet

test:
	pytest --version
	pytest -vv

.PHONY: install lint test
