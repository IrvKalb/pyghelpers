all:

clean:
	rm -fr __pycache__ dist MANIFEST *.egg-info src/__pycache__ src/*.egg-info
	
sdist:
	python3 setup.py sdist
	
upload:
	python3 -m twine upload dist/* --verbose
	
install:
	pip3 install -U --user --force-reinstall --no-index -f dist pyghelpers

uploadtest:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/* 
	
installtest:
	pip install --user -U --index-url https://test.pypi.org/simple/ pyghelpers