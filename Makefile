# vim: set tabstop=2 shiftwidth=2 expandtab:

SHELL=/bin/bash

Here  := $(shell git rev-parse --show-toplevel)
There := $(Here)/../4gotn.github.io
Repos := $(Here) $(There)
		
define both
   $(foreach d, $(Repos), \
      @cd $d; echo; figlet -w 100 -W -f mini $(notdir $d); echo; $(1); \
      )
endef
 
pull:;   $(call both, git pull)
push:;   $(call both, git commit -am saving && git push && git status)
status:; $(call both, git status)

install:
	cargo install mdbook-alerts

build:
	cd $(Here)/docs && mdbook build
	open $(There)/docs/index.html

