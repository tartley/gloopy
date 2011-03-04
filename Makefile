
# These make targets aren't really critical, they are more of a cheatsheet to
# remind me of a few commonly-used commands.

# I run these under Ubuntu bash, or on Windows with Cygwin binaries foremost on
# the PATH


NAME := $(shell python -c "from setup import NAME; print NAME")
SCRIPT := $(shell python -c "from setup import SCRIPT; print SCRIPT")
VERSION := $(shell python -c "from ${NAME} import VERSION; print VERSION")
RELEASE := $(shell python -c "from ${NAME} import RELEASE; print RELEASE")


help:
	@echo This Makefile has no default target.


test:
	python -m unittest discover gloopy
.PHONY: tests


# runsnake is a GUI profile visualiser, very useful.
# http://www.vrplumber.com/programming/runsnakerun/
profile:
	python -O -m cProfile -o profile.out ${SCRIPT}
	runsnake profile.out
.PHONY: profile


clean:
	rm -rf build/* dist/* *.egg-info tags pip-log.txt
	-find . \( -name "*.py[oc]" -o -name "*.orig" \) -exec rm {} \;
	$(MAKE) -C ${NAME}/docs clean
.PHONY: clean


tags:
	ctags -R ${NAME}
.PHONY: tags


docs:
	@$(MAKE) -C ${NAME}/docs
.PHONY: docs


sdist: docs
	rm -rf dist/${NAME}-${RELEASE}.* build
	python setup.py sdist
	rm -rf ${NAME}.egg-info
.PHONY: sdist


register: docs
	rm -rf dist/${NAME}-${RELEASE}.* build
	python setup.py --quiet sdist register
	rm -rf ${NAME}.egg-info
.PHONY: register


upload: docs
	rm -rf dist/${NAME}-${VERSION}.* build
	python setup.py --quiet sdist register upload
	rm -rf ${NAME}.egg-info
.PHONY: upload


py2exe:
	rm -rf dist/${NAME}-${RELEASE}-windows build
	python setup.py --quiet py2exe
.PHONY: py2exe


stats:
	@echo "non-blank lines of code:"
	@echo -n 'product: '
	@find ${NAME} -name '*.py' | grep -v "/tests/" | xargs cat | grep -cve "^\W*$$"
	@echo -n 'tests: '
	@find ${NAME} -name '*.py' | grep "/tests/" | xargs cat | grep -cve "^\W*$$"
.PHONY: stats

