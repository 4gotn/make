# vim: set tabstop=2 shiftwidth=2 expandtab:

SHELL=/bin/bash

Here  := $(shell git rev-parse --show-toplevel)
There := $(Here)/../4gotn.github.io
Repos := $(Here) $(There)

H := \033[0;1;31m
T := \033[0;1;33m
Z := \033[0m

define both
	@for dir in $(Repos); do \
		name=$$(basename $$dir); \
		color=$$( [ "$$name" = "4gotn.github.io" ] && echo "$(T)" || echo "$(H)" ); \
		printf "$$color\n====> $$dir\n\n$(Z)"; \
		cd $$dir && $(1); \
	done
endef
 
pull:;   $(call both, git pull)
push:;   $(call both, git commit -am saving && git push && git status)
status:; $(call both, git status)

install:
	cargo install mdbook-alerts

build:
	cd $(Here)/docs && mdbook build

