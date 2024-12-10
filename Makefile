VENV = venv
FLASK_APP = app.py
PYTHON_VERSION = python3.11

# Install dependencies
install:
	$(PYTHON_VERSION) -m venv $(VENV)
	./$(VENV)/bin/pip install --upgrade pip
	./$(VENV)/bin/pip install -r requirements.txt

# Run the Flask application
run:
	FLASK_APP=$(FLASK_APP) FLASK_DEBUG=1 ./$(VENV)/bin/flask run --port 3000

# Train the model route
train_model:
	./$(VENV)/bin/python $(FLASK_APP) train_model

# Clean up virtual environment
clean:
	rm -rf $(VENV)

# Reinstall all dependencies
reinstall: clean install
