
define INSERTER
s = open('build/README_help.md').read();\
s = s[s.find('optional arguments:') + 19:];\
s2 = open('src.md', encoding = 'utf-8').read();\
open('README.md', 'w', encoding = 'utf-8').write(s2.replace('place_where_should_be_help_inserted', s, 1))
endef

all: README.md

README.md: src.md build/README_help.md
	python -c "$(INSERTER)"

build/README_help.md: dispenser.py
	python dispenser.py -h > build/README_help.md
	
clean:
	rm -r build/*