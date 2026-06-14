NIKOLA = uv run nikola

.DEFAULT_GOAL := help

.PHONY: help
help: ## Show this help
	@echo "Makefile targets:"
	@awk 'BEGIN {FS = ":.*##"} \
		/^[a-zA-Z0-9_.-]+:.*##/ { \
			printf "  %-20s %s\n", $$1, $$2 \
		}' $(MAKEFILE_LIST)

run: serve

pull:  ## Pull posts from ~/Notes/Blog, transform metadata for Nikola
	-uv run python3 scripts/pull-from-notes.py

build:  ## Render all the files
	$(NIKOLA) build
	rsync -avP plugins/*/files/ output/

serve: pull build ## Run the local web server and watch for changes
	# https://serialized.net/2013/04/nikola-and-livereload-ftw/
	while inotifywait -r posts; do $(NIKOLA) build; done &
	$(NIKOLA) serve

new: ## Create a new post
	$(NIKOLA) new_post
