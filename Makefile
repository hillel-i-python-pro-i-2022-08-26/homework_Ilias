.PHONY: flask-i-run
flask-i-run:
	@flask run

.PHONY: flask-i-purge
flask-i-purge:
	@echo chao chao

.PHONY: init-dev
init-dev:
	@pip install --upgrade pip && \
	pip install --requirement requirements.txt && \
	pre-commit install