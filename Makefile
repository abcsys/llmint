.PHONY: dist install
dist:
	python setup.py sdist bdist_wheel && twine upload --skip-existing dist/*
	rm -rf build dist *.egg-info
install:
	pip install -e . && rm -rf *.egg-info
	mkdir -p ~/.llmint && touch ~/.llmint/config.yaml

.PHONY: test
test:
	python -m benchmark.benchmark_record_match
