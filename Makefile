
# These make targets aren't really critical, they are more of a cheatsheet to
# remind me of a few commonly-used commands.

# I run these under Ubuntu bash, or on Windows with Cygwin binaries foremost on
# the PATH


NAME := gloopy
VERSION := $(shell uv run python -c "from ${NAME} import VERSION; print(VERSION)")

help:  ## Show this help.
	@# Optionally add 'sort' before 'awk'
	@grep -E '^[^_][a-zA-Z_\/\.%-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-10s\033[0m %s\n", $$1, $$2}'
.PHONY: help

run: ## Run Gloopy
	./run
.PHONY: run

get-version:  ## Print version number to stdout
	@echo $(VERSION)

test:  ## Run tests
	uv run python -m unittest discover gloopy
.PHONY: tests

clean:  ## Delete generated files
	rm -rf build dist *.egg-info tags pip-log.txt
	-find . \( -name "*.py[oc]" -o -name "*.orig" -o -name "*.rej" \) -exec rm {} \;
	$(MAKE) -C docs clean
.PHONY: clean

tags:
	ctags -R ${NAME}
.PHONY: tags

# Building docs doesn't currently work
# It was a bit misguided, this project is a wacky personal experiment,
# it doesn't need that kind of documentation anyway

