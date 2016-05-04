.PHONY: install
install:
	pip install -r requirements.txt --quiet
	pip install -e .

all: install test-fast style-fast

test: install
	py.test --cov=mousestyles --pyargs mousestyles

style: install
	py.test --pep8 --flakes --pyargs mousestyles

clean:
	find . -name "*.so" -o -name "*.pyc" -o -name "*.pyx.md5" | xargs rm -f
	find . -name "__pycache__" -o -name ".cache" | xargs rm -rf
	rm -rf build dist mousestyles.egg-info

# warning: the following targets don't ensure that the package is up-to-date.
# only use these after running make install.

test-fast:
	py.test --cov=mousestyles --pyargs mousestyles

style-fast:
	py.test --pep8 --flakes --pyargs mousestyles

travis-test:
	py.test --cov=mousestyles --pep8 --flakes --pyargs mousestyles


.PHONY: doc
doc:
	cd doc/source && $(MAKE) html
