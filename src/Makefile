-include ../Makefile

~/tmp/%.pdf: %.py  ## make doco: .py ==> .pdf using a2ps | ps2pdf
	mkdir -p ~/tmp
	echo "Generating $@ ..."
	a2ps $< \
		--pro=color \
		--line-numbers=1 \
		--file-align=fill \
		--borders=no \
		--columns=4 \
		--lines-per-page=150 \
		--chars-per-line=80 \
		--left-title="" \
		--left-footer="$<" \
		--right-footer="page %s. of %s#" \
		-Br -M letter -o - \
	| ps2pdf - $@
	open $@

html:
	docco -o ~/tmp forgo.py

pythonInstall:
	sudo npm install -g docco
