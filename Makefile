
define cutter
s = open('build/README_1.md').read();\
open('build/README_1.md', 'w').write('\n\`\`\`\n' + s[s.find('optional arguments:') + 19:] + '\n\`\`\`\n')
endef

all: README.md

README.md: build/README_0.md build/README_1.md build/README_2.md
	pandoc build/README_0.md build/README_1.md build/README_2.md -o README.md

build/README_1.md: dispenser.py
	python dispenser.py -h > build/README_1.md
	python -c "$(cutter)"
