
docs: api *.rst
	@mkdir -p _static
	@rm -rf html
	@sphinx-build -q -c . -b html . ./html
.PHONY: docs

api:
	@rm -rf api
	@mkdir api
	@sphinx-apidoc --doc-header=API\ Reference ../gloopy -o api
.PHONY: api

clean:
	@rm -rf api html _build _sources _templates .doctrees
.PHONY: clean

