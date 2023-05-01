.PHONY: clean
clean:
	find . -name '*.pyo' -delete
	find . -name '*.pyc' -delete
	find . -name '*~' -delete
	find . -name '.coverage.*' -delete
	find . -name __pycache__ -delete
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	rm -rf ./build
	rm -rf ./dist
	rm -rf ./premium_primitives.egg-info
	rm -rf ./unpacked_sdist

.PHONY: lint
lint:
	black . --config=./pyproject.toml --check
	ruff . --config=./pyproject.toml

.PHONY: lint-fix
lint-fix:
	black . --config=./pyproject.toml
	ruff . --fix --config=./pyproject.toml

PYTEST = python -m pytest -n auto -s -vv

.PHONY: test
test:
	$(PYTEST)

.PHONY: testcoverage
testcoverage:
	$(PYTEST) --cov=premium_primitives

.PHONY: installdeps
installdeps: upgradepip
	pip install -e .

.PHONY: installdeps-dev
installdeps-dev: upgradepip
	pip install -e ".[dev]"
	pre-commit install

.PHONY: installdeps-test
installdeps-test: upgradepip
	pip install -e ".[test]"

.PHONY: checkdeps
checkdeps:
	$(eval allow_list='featuretools|numpy|pandas|phone-iso3166|phonenumbers|reverse_geocoder|zipcodes')
	pip freeze | grep -v "alteryx/premium_primitives.git" | grep -E $(allow_list) > $(OUTPUT_PATH)

.PHONY: upgradepip
upgradepip:
	python -m pip install --upgrade pip

.PHONY: upgradebuild
upgradebuild:
	python -m pip install --upgrade build

.PHONY: upgradesetuptools
upgradesetuptools:
	python -m pip install --upgrade setuptools

.PHONY: package
package: upgradepip upgradebuild upgradesetuptools
	python -m build
	$(eval PACKAGE=$(shell python -c 'import setuptools; setuptools.setup()' --version))
	tar -zxvf "dist/premium_primitives-${PACKAGE}.tar.gz"
	mv "premium_primitives-${PACKAGE}" unpacked_sdist
