.PHONY: task-i-run
task-i-run:
	@flask run

.PHONY: task-i-purge
task-i-purge:
	@echo chao chao

.PHONY: init-dev
init-dev:
	@pip install --upgrade pip && \
	@pip install --requirement requirements.txt && \
	@pre-commit install