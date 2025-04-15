silence=

SHELL=/bin/bash
#find my way home
Here=$(shell git rev-parse --show-toplevel)
There=$(Here)/../4gotn.github.io

push:
	cd $(Here);  git commit -am saving; git push; git status
	cd $(There); git commit -am saving; git push; git status

install:
	cargo install mdbook-alerts

status:
	printf "\n--------\n$(Here)\n\n";  cd $(Here); git status
	printf "\n--------\n$(There)\n\n"; cd $(There); git status

build:
	cd $(Here)/docs; mdbook build
	cd $(There)/docs; touch .nojeklyll; git add .nojekyll .gitignore
