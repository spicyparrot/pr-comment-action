TEST_SOURCE_DIR = ./src
TEST_REPORTS_DIR = ./tests/reports

env.local: deps.code
	python3.9 -m venv env/
	env/bin/pip install --upgrade pip
	env/bin/pip install -U pip wheel setuptools
	env/bin/pip install -r $(TEST_SOURCE_DIR)/requirements.txt

deps.local: test.hooks
	mkdir -p $(TEST_REPORTS_DIR)
	pip install -r $(TEST_SOURCE_DIR)/requirements.txt
	bash test_data.sh --env local

deps.ci: 
	mkdir -p $(TEST_REPORTS_DIR)
	pip install -r $(TEST_SOURCE_DIR)/requirements.txt
	bash -c "set -a && source .env && set +a"
	bash test_data.sh --env local
	
deps.test:
	pip install \
		pytest==7.4.0 \
		pylint==3.0.2 \
		pylint-json2html==0.5.0 \
		pytest-html==3.2.0 \
		pytest-cov \
		pytest-sugar \
		pytest-md \
		pytest-emoji

test.hooks:
	cp .github/hooks/pre-commit .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit

test.lint: deps.test
	pylint $(TEST_SOURCE_DIR) \
		--fail-under=3.0 \
		--output-format=json:$(TEST_REPORTS_DIR)/pylint.json

	pylint-json2html $(TEST_REPORTS_DIR)/pylint.json -o $(TEST_REPORTS_DIR)/pylint.html

test.unit: deps.test
	pytest ./tests/test_*.py \
		--log-cli-level=INFO \
		--emoji -v \
		--html=$(TEST_REPORTS_DIR)/pytest.html \
		--md $(TEST_REPORTS_DIR)/pytest.md \
		--cov=$(TEST_SOURCE_DIR) \
		--cov-report=term-missing:skip-covered \
		--cov-report=html:$(TEST_REPORTS_DIR)/coverage.html \
		--cov-report=xml:$(TEST_REPORTS_DIR)/coverage.xml \
		--junitxml=$(TEST_REPORTS_DIR)/pytest.xml

test.cov: deps.test
	coverage run \
		--source=$(TEST_SOURCE_DIR) \
		--omit="__init__.py" \
		-m  \
		pytest ./tests/test_*.py \
			--log-cli-level=INFO \
			--emoji -v \
			--html=$(TEST_REPORTS_DIR)/pytest.html \
			--md $(TEST_REPORTS_DIR)/pytest.md \
			--junitxml=$(TEST_REPORTS_DIR)/pytest.xml

	coverage xml --include "$(TEST_SOURCE_DIR)/*" -o $(TEST_REPORTS_DIR)/coverage.xml
	coverage html --include "$(TEST_SOURCE_DIR)/*" --directory $(TEST_REPORTS_DIR)/coverage_html