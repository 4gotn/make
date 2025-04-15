silence=

SHELL=/bin/bash
#find my way home
Here=$(shell git rev-parse --show-toplevel)
There=$(Here)/../4gotn.github.io

H="\033[0;1;31m\n------\n$(Here)\n\n\033[0m"
T="\n------\n$(THere)\n\n"

push:
	cd $(Here);  git commit -am saving; git push; git status
	cd $(There); git commit -am saving; git push; git status

install:
	cargo install mdbook-alerts

status:
	$(shell printf "$H");   cd $(Here); git status
	$(shell printf "$T"); cd $(There); git status

build:
	cd $(Here)/docs; mdbook build
	cd $(There)/docs; touch .nojeklyll; git add .nojekyll .gitignore
