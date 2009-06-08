debug_ngly:
	ipython -pylab -i parse_KGML.py -- -p data/hsa00510.xml -t o

debug_ko:
	ipython	-pylab -i parse_KGML.py data/ko00020.xml

test_:
	nosetests --with-doctest
