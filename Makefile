.PHONY: setup run test clean

# Variables
PYTHON = python3
PIP = pip3
STREAMLIT = streamlit

# Setup commands
setup:
	$(PIP) install -r requirements.txt

# Run the test pipeline
test:
	$(PYTHON) src/test_pipeline.py

# Run the Streamlit app
run:
	$(STREAMLIT) run src/app.py

# Clean up
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".DS_Store" -delete

# Full setup and run
all: setup test run

# Help command
help:
	@echo "Available commands:"
	@echo "  make setup    : Install dependencies"
	@echo "  make test     : Run test pipeline"
	@echo "  make run      : Start Streamlit app"
	@echo "  make clean    : Clean up cache files"
	@echo "  make all      : Full setup and run" 