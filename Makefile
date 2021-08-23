
define inserter
s = open('build/README_help.md').read();\
s = s[s.find('optional arguments:') + 19:];\
s2 = open('src.md').read();\
open('README.md', 'w').write(s2.replace('place_where_should_be_help_inserted', s, 1))
endef

all: README.md

README.md: src.md build/README_help.md
	python -c "$(inserter)"
	#pandoc build/README_full.md -o README.md

build/README_help.md: dispenser.py
	python dispenser.py -h > build/README_help.md
	
clean:
	rm -r build/*