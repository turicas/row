test:
	@clear
	nosetests -dsv --with-yanc --with-coverage --cover-package row

clean:
	rm .coverage *.pyc

.PHONY:	test clean
