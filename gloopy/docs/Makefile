
html: api
	mkdir -p _static
	sphinx-build -c . -b html . ./html
.PHONY: html

clean_html:
	rm -rf html
.PHONY: clean_html

api:
	mkdir -p api
	sphinx-apidoc --doc-header=API\ Reference -o api ..\\..\\gloopy
.PHONY: api

clean_api:
	rm -rf api
.PHONY: clean_api

clean: clean_api clean_html
.PHONY: clean

