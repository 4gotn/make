-include ../Makefile

~/tmp/%.pdf: %.py  ## make doco: .py ==> .pdf using a2ps | ps2pdf
	mkdir -p ~/tmp
	echo "Generating $@ ..."
	a2ps $< \
		--pro=color \
		--line-numbers=1 \
		--file-align=fill \
		--borders=no \
		--columns=3 \
		--left-title="" \
		--left-footer="$<" \
		--right-footer="page %s. of %s#" \
		-Br -M letter -o - \
	| ps2pdf - $@
	open $@
# 		--lines-per-page=150 \
# 		--chars-per-line=80 \

html:
	docco -o ~/tmp forgo.py

pythonInstall:
	sudo npm install -g docco

general: ../../moot/optimize/[bchmp]*/*.csv
	@{ $(foreach d, $^,  python3 -B forgo.py --tree $d;) } | sort -n | fmt
