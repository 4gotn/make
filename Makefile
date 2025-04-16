# vim: set tabstop=2 shiftwidth=2 expandtab:

SHELL=/bin/bash

Here  := $(shell git rev-parse --show-toplevel)
There := $(Here)/../4gotn.github.io
Repos := $(Here) $(There)

define each
	$(foreach d, $(Repos), cd $d; figlet -w 100 -W -f mini $(notdir $d); $(1);)
endef
 
pull:;   @$(call each, git pull)
push:;   @$(call each, git commit -am saving && git push && git status)
status:; @$(call each, git status)

install:
	cargo install mdbook-alerts

build:
	cd $(Here)/docs && mdbook build
	open $(There)/docs/index.html
