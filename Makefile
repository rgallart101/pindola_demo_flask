PYTHON ?= $(shell if [ -x .venv/bin/python ]; then echo .venv/bin/python; else echo python; fi)

.PHONY: compile-language clean serve

compile-language:
	@echo "Compiling translation catalogs..."
	$(PYTHON) -m babel.messages.frontend compile -d app/translations

clean:
	@echo "Removing __pycache__ directories and .pyc files..."
	-find . -type d -name "__pycache__" -prune -exec rm -rf '{}' + ; true
	-find . -type f -name "*.pyc" -delete ; true

serve:
	@echo "Starting Flask application (python run.py)..."
	$(PYTHON) run.py
