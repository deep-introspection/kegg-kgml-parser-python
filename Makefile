debug_glycol:
	ipython -pylab -i parse_KGML.py -- -p data/hsa00010.xml -t o

debug_ngly:
	ipython -pylab -i parse_KGML.py -- -p data/hsa00510.xml -t o

debug_ko:
	ipython	-pylab -i parse_KGML.py data/ko00020.xml

debug_originalplot: 
	ipython -pylab -i parse_KGML.py -- -p data/hsa00510.xml -t o -d

#"plots/N-Glycan biosynthesis_original_layout.png"
##"plots/N-Glycan biosynthesis_original_layout.png": parse_KGML.py data/hsa00510.xml

debug_plot:
	ipython -pylab -i parse_KGML.py -- -p data/hsa00510.xml -t o -c

debug_gml:
	ipython -pylab -i parse_KGML.py -- -p data/hsa00510.xml -t o -g

test_doctests:
	nosetests --with-doctest -v

test_units:
	nosetests --with-doctest test/ -v

clean:
	-rm *.png *.gml
