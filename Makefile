build:
	python3 setup.py sdist bdist_wheel
upload:
	rm -rf dist
	twine upload dist/* 
install:
	pip install tldrwl
