# vim: set tabstop=2 shiftwidth=2 expandtab:

SHELL=/bin/bash

Here  := $(shell git rev-parse --show-toplevel)
There := $(Here)/../4gotn.github.io
Repos := $(Here) $(There)

H := \033[0;1;31m
T := \033[0;1;33m
Z := \033[0m


#	@for dir in $(Repos); do \
#		name=$$(basename $$dir); figlet -W $$(name); cd $$dir && $(1); \ 
#	done
		
define both
   $(foreach d,$(Repos), cd $d; figlet -W -f small $(notdir $d); $(1); )
endef
 
pull:;   $(call both, git pull)
push:;   $(call both, git commit -am saving && git push && git status)
status:; $(call both, git status)

install:
	cargo install mdbook-alerts

build:
	cd $(Here)/docs && mdbook build
	open $(There)/docs/index.html

