develop:
	# this makes it possible to run unit tests
	python3 setup.py develop
build:
	# this builds the packages for pypi
	# might need to run pip install wheel
	python3 setup.py sdist bdist_wheel
upload:
	# this uploads the packages to pypi
	rm -rf dist
	twine upload dist/* 
