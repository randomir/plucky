.PHONY: test upload

test:
	cd tests/ && ./tests.py

upload: test
	python setup.py sdist bdist_wheel upload
