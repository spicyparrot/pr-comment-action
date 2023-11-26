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
	pytest ./tests/test.py \
		--log-cli-level=INFO \
		--emoji -v \
		--html=./tests/reports/pr_comment.html \
		--md ./tests/reports/pr_comment.md

cov:
	pytest ./tests/test.py \
		--log-cli-level=INFO \
		--cov=./src \
		--cov-report=term-missing:skip-covered \
		--cov-report=xml:./tests/reports/coverage.xml \
		--cov-report=html:./tests/reports/coverage.html

coverage:
	coverage run -m  \
		pytest ./tests/test.py \
			--log-cli-level=INFO

run:
	python3.9 ./src/main.py



#pytest ./tests/test_pykx.py --log-cli-level=INFO --cov=./src/kdb --cov-report=xml:./secrets/coverage.xml --cov-report=html:./secrets/coverage.html

#--junitxml=/pixel/test_results/pytest.xml \

#bash -c 'set -o pipefail && pytest --exitfirst tests/test.py -v --log-cli-level=INFO --junitxml=/pixel/test_results/pytest.xml --cov-report=term-missing:skip-covered --cov-report=xml:./coverage.xml --cov=main --timeout=90 | tee /tmp/test_reports/test.txt /pixel/test_results/pytest-coverage.txt && coverage xml -i && mv coverage.xml /pixel/test_results/'
#--junitxml=/pixel/test_results/pytest.xml
#--cov-report=term-missing:skip-covered 
#--cov-report=xml:./coverage.xml 
#--cov=main 
#--timeout=90 | tee /tmp/test_reports/test.txt /pixel/test_results/pytest-coverage.txt && coverage xml -i && mv coverage.xml /pixel/test_results/'