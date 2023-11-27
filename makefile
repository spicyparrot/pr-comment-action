env:
	python3.9 -m venv env/
	env/bin/pip install --upgrade pip
	env/bin/pip install -U pip wheel setuptools
	env/bin/pip install -r ./src/requirements.txt

deps:
	pip install -r ./src/requirements.txt
	pip install \
		pytest==7.4.0 \
		pytest-html==3.2.0 \
		pytest-cov \
		pytest-sugar \
		pytest-md \
		pytest-emoji

test:
	pytest ./tests/test_app.py \
		--log-cli-level=INFO \
		--emoji -v \
		--html=./tests/reports/pytest.html \
		--md ./tests/reports/pytest.md \
		--cov=./src \
		--cov-report=term-missing:skip-covered \
		--cov-report=html:./tests/reports/coverage.html \
		--cov-report=xml:./tests/reports/coverage.xml \
		--junitxml=./tests/reports/pytest.xml

cov:
	coverage run -m  \
		pytest ./tests/test_app.py \
			--log-cli-level=INFO \
			--emoji -v \
			--html=./tests/reports/pytest.html \
			--md ./tests/reports/pytest.md \
			--junitxml=./tests/reports/pytest.xml

	coverage xml --include "src/*" -o ./tests/reports/coverage.xml
	coverage html --include "src/*" --directory ./tests/reports/coverage_html