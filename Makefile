PATH := ./vim-themis/bin:$(PATH)
export THEMIS_VIM  := nvim
export THEMIS_ARGS := -e -s --headless
export THEMIS_HOME := ./vim-themis


install: vim-themis
	pip install pynvim --upgrade
	pip install pytest --upgrade
	pip install flake8 --upgrade
	pip install mypy --upgrade
	pip install vim-vint --upgrade

lint:
	vint --version
	vint plugin
	vint autoload
	flake8 --version
	flake8 rplugin/python3/deoppet
	mypy --version
	mypy --ignore-missing-imports rplugin/python3/deoppet

test:
	themis --version
	themis test/autoload/*
	pytest --version
	pytest

vim-themis:
	git clone https://github.com/thinca/vim-themis vim-themis

.PHONY: install lint test
