# Disable command logging by default. This can be overridden by setting the
# verbosity when executing `make`.
ifndef VERBOSE
.SILENT:
endif

help: ## show this message
	@grep -h -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST)  \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-10s\033[0m %s\n", $$1, $$2}'

.PHONY: help
.DEFAULT_GOAL := help


install: ## create environment virtual and install requirements for inicialize the project
	- ( \
		virtualenv -p python3.8 venv; \
		.  venv/bin/activate;  \
		pip install --upgrade pip \
		pip install -r requirements.txt;  \
		pip install -U pytest; \
	)
