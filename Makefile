.PHONY: dist install
dist:
	python setup.py sdist bdist_wheel && twine upload --skip-existing dist/*
	rm -rf build dist *.egg-info
install:
	pip install -e . && rm -rf *.egg-info
	mkdir -p ~/.llmint && touch ~/.llmint/config.yaml

.PHONY: benchmark_match, benchmark_mapper, test
benchmark_match:
	python -m benchmark.benchmark_record_match
benchmark_mapper:
	python -m benchmark.benchmark_record_mapper
test: | benchmark_match
