# Relish_backend

## Docker settings
### Build docker compose
`docker-compose build`
in the root directory

### run the container
`docker-compose up`

# Code Quality Checks
## Flake8

### Check your code quality
```bash
flake8 .
```
at the root directory

## Isort

### sorting and organizing import statements
```bash
isort .
```
at the root directory

## mypy
```bash
mypt src
```
at the root directory

## Radon
Check code complexity in the files
```bash
radon cc src
```

## Xenon
```
xenon --max-absolute A --max-modules A --max-average A src
```
The command xenon --max-absolute A --max-modules A --max-average A src instructs Xenon to analyze the Python files in the src directory and its subdirectories, and then report on the code complexity based on certain thresholds.

--max-absolute A: Specifies the maximum acceptable absolute cyclomatic complexity grade. In this case, it's set to "A", which likely means Xenon will not report any functions with a cyclomatic complexity grade higher than "A".

--max-modules A: Sets the maximum number of modules to report. Similarly, it's set to "A", indicating that Xenon will limit the number of modules it reports on, likely to those with the highest complexity.

--max-average A: Specifies the maximum acceptable average cyclomatic complexity grade across all modules. Again, it's set to "A", indicating that Xenon will not report any modules with an average complexity grade higher than "A".

With these settings, Xenon is configured to be quite strict, potentially filtering out many functions or modules from its report if they exceed the specified complexity thresholds. Adjusting these thresholds to higher grades (e.g., "B", "C", etc.) would allow for reporting on more complex code.

## Test
```bash
python src/manage.py test tests
```
at the root directory

## Run all checks in one go
```
make check_all
```
at the root.