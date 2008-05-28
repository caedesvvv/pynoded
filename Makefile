prefix=/usr/local

all:

doc:
	epydoc  --config docs/epydoc/pygraph.conf

install:
	python setup.py install --prefix=$(prefix)

clean:

distclean: clean

distro:
	echo "Not implemented"

