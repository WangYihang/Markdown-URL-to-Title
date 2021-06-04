test: build
	twine upload --skip-existing --repository-url https://test.pypi.org/legacy/ dist/*
release: build
	twine upload --skip-existing dist/*
build: dependency
	python3 setup.py sdist bdist_wheel
	twine check dist/*
dependency:
	pip3 install twine
clean:
	rm -rf build dist *.egg-info