.PHONY: test upload

test: $(patsubst tests/%,%,$(wildcard tests/test_*))

test_%: tests/test_%
	python "$<"

upload: test
	python setup.py sdist bdist_wheel upload
