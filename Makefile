clean:
	rm -rf dist
	rm -rf cbot.egg-info
build:
	python3 -m build
test:
	python3 -m twine upload --repository testpypi dist/*
deploy:
	python3 -m twine upload dist/*
