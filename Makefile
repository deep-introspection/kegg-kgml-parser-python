debug_ngly:
	ipython -pylab -i parse_KGML.py data/hsa00510.xml

debug_ko:
	ipython	-pylab -i parse_KGML.py data/ko00020.xml

test_:
	nosetests --with-doctest
