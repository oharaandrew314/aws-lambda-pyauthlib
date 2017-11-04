init:
	pipenv install --dev

clean:
	rm -rf dist build
	pipenv run setup.py clean --all

test:
	pipenv run pytest tests examples --cov-report term-missing --cov
	pipenv run flake8

package: clean
	pip install -q setuptools wheel
	python setup.py bdist_wheel --universal

publish-test: package
	pip install -q twine
	twine upload -r pypitest dist/*

publish: package
	pip install -q twine
	twine upload -r pypi dist/*

dev-mode:
	pip install -e . --upgrade