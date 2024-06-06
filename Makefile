check_all: check_quality organize_imports check_types check_complexity check_xenon run_tests

check_quality:
	flake8 .

organize_imports:
	isort .

check_types:
	mypy src

check_complexity:
	radon cc src

check_xenon:
	xenon --max-absolute A --max-modules A --max-average A src

run_tests:
	python src/manage.py test tests

.PHONY: check_all check_quality organize_imports check_types check_complexity check_xenon run_tests
