 
.PHONY: install test lint clean

# Create (or update) your virtualenv and install deps
install:
	python -m venv venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -r requirements.txt

# Run your tests
test:
	venv/bin/pytest --maxfail=1 --disable-warnings -q

# Tear it all down
clean:
	rm -rf venv merged.txt merged_all.txt


