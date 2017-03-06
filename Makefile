.PHONY: test upload

test:
	cd tests/ && ./test_pluck.py && ./test_merge.py

upload: test
	python setup.py sdist bdist_wheel upload
