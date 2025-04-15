silence=

SHELL=/bin/bash
#find my way home
Here=$(shell git rev-parse --show-toplevel)
There=$(Here)/../4gotn.github.io

H=\033[0;1;31m\n====> $(Here)\n\n\033[0m
T=\033[0;1;33m\n====> $(There)\n\n\033[0m

pull:
	@printf "$H"; cd $(Here);  git pull
	@printf "$T"; cd $(There); git pull

push:
	@printf "$H"; cd $(Here);  git commit -am saving; git push; git status
	@printf "$T"; cd $(There); git commit -am saving; git push; git status

install:
	cargo install mdbook-alerts

status:
	@printf "$H"; cd $(Here); git status
	@printf "$T"; cd $(There); git status

build:
	cd $(Here)/docs; mdbook build

xxx:
	cd $(There)/docs; touch .nojeklyll; \
		git add .nojekyll .gitignore; \
		git commit -am config
