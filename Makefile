PATH := ./vim-themis/bin:$(PATH)
export THEMIS_VIM  := nvim
export THEMIS_ARGS := -e -s --headless
export THEMIS_HOME := ./vim-themis


install: vim-themis
	pip install --upgrade -r test/requirements.txt

lint:
	vint --version
	vint plugin
	vint autoload
	flake8 --version
	flake8 rplugin/python3/deoppet
	mypy --version
	mypy --ignore-missing-imports --strict rplugin/python3/deoppet

test:
	themis --version
	themis test/autoload/*
	pytest --version
	pytest

vim-themis:
	git clone https://github.com/thinca/vim-themis vim-themis

.PHONY: install lint test
