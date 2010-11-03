
# These make targets aren't really critical, they are more of a cheatsheet to
# remind me of a few commonly-used commands.

# I run these under Ubuntu bash, or on Windows with Cygwin binaries foremost on
# the PATH


NAME := $(shell python -c "from setup import NAME; print NAME")
SCRIPT := $(shell python -c "from setup import SCRIPT; print SCRIPT")
VERSION := $(shell python -c "from ${NAME} import __version__; print __version__")


clean:
	rm -rf build dist tags pip-log.txt
	-find . \( -name "*.py[oc]" -o -name "*.orig" \) -exec rm {} \;
.PHONY: clean


tags:
	ctags -R ${NAME}
.PHONY: tags


# runsnake is a GUI profile visualiser, very useful.
# http://www.vrplumber.com/programming/runsnakerun/
profile:
	python -O -m cProfile -o profile.out ${SCRIPT}
	runsnake profile.out
.PHONY: profile


tests:
	nosetests ${NAME}
.PHONY: tests


sdist:
	rm -rf dist/${NAME}-${VERSION}.* build
	python setup.py --quiet sdist
	rm -rf ${NAME}.egg-info
.PHONY: sdist


py2exe:
	rm -rf dist/${NAME}-${VERSION}-windows build
	python setup.py --quiet py2exe
.PHONY: py2exe


stats:
	@echo "non-blank lines of code:"
	@echo -n 'product: '
	@find ${NAME} -name '*.py' | grep -v "/tests/" | xargs cat | grep -cve "^\W*$$"
	@echo -n 'tests: '
	@find ${NAME} -name '*.py' | grep "/tests/" | xargs cat | grep -cve "^\W*$$"
.PHONY: stats

