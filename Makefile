.PHONY: homework-i-run
homework-i-run:
	@flask run

.PHONY: homework-i-purge
homework-i-purge:
	@echo end of work

.PHONY: init-dev
init-dev:
	@pip install --upgrade pip && \
	pip install --requirement requirements.txt && \
	pre-commit install
