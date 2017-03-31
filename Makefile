.PHONY: test upload

test:
	cd tests/ && ./test_pluck.py && ./test_merge.py && ./test_pluckable.py

upload: test
	python setup.py sdist bdist_wheel upload
