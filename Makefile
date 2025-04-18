# vim: set tabstop=2 shiftwidth=2 expandtab:

SHELL=/bin/bash

Here  := $(shell git rev-parse --show-toplevel)
There := $(Here)/../4gotn.github.io
Repos := $(Here) $(There)

define every
	$(foreach d, $(Repos), cd $d; figlet -w 100 -W -f mini $(notdir $d); $(1);)
endef
 
help:  ## Show this help menu
	@gawk 'BEGIN {FS = ":.*?## "}    \
         /^[a-zA-Z0-9_-]+:.*?## / { \
            printf "  \033[1m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

pull: ## refresh from online repos
	@$(call every, git pull)

push: ## save to online repo
	@$(call every, git diff --quiet || git commit -am saving && git push && git status)

status: ## find uncommited files
	@$(call every, git status)

install: ## esnure rust is ready
	cargo install mdbook-alerts

build: ## update book
	cd $(Here)/docs && mdbook build
	open $(There)/docs/index.html

publish: build push ## update book and push online
