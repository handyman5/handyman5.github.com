# nikola auto is busted in the latest release
# NIKOLA = uv run --with "git+https://github.com/getnikola/nikola.git\#egg=Nikola[extras]" nikola
NIKOLA = uv run --with "git+https://github.com/getnikola/nikola.git@0a3f5e923b35e9884207faee645512d1ef5df4f6\#egg=Nikola[extras]" nikola

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
	-rsync -avP ~/Notes/Blog/*.md posts/
	-rsync -avP ~/Notes/Blog/images/* images/

build:  ## Render all the files
	$(NIKOLA) build
	rsync -avP plugins/*/files/ output/

serve: pull build ## Run the local web server and watch for changes
	$(NIKOLA) auto

new: ## Create a new post
	$(NIKOLA) new_post

publish-dry-run:  ## Dry-run of publishing
	./node_modules/.bin/sequoia publish --dry-run

publish:  ## Publish via standard.site
	./node_modules/.bin/sequoia publish
