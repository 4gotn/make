# vim: set tabstop=2 shiftwidth=2 expandtab:

SHELL=/bin/bash

Here  := $(shell git rev-parse --show-toplevel)
There := $(Here)/../4gotn.github.io
Repos := $(Here) $(There)
		
define both
   $(foreach d, $(Repos), \
      cd $d; echo; figlet -w 100 -W -f mini $(notdir $d); echo; $(1); )
endef

help:  ## Show this help menu
	@gawk 'BEGIN {FS = ":.*?## "}    \
         /^[a-zA-Z0-9_-]+:.*?## / { \
            printf "  \033[1m%-15s\033[0m %s\n", $$1, $$2} \
        ' $(MAKEFILE_LIST)

pull: ## refresh from online repo
	@$(call both, git pull)

push: ## save to online repo
	@$(call both, git commit -am saving && git push && git status)

status: ## find uncommited files
	@$(call both, git status)

install: ## esnure rust is ready
	cargo install mdbook-alerts

build: ## update book
	cd $(Here)/docs && mdbook build
	open $(There)/docs/index.html

publish: ## update book and push online
	build push
