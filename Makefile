NIKOLA = uv run nikola

run: serve

build:
	$(NIKOLA) build
	rsync -avP plugins/*/files/ output/

serve:
	# https://serialized.net/2013/04/nikola-and-livereload-ftw/
	while inotifywait -r posts; do $(NIKOLA) build; done &
	$(NIKOLA) serve

new:
	$(NIKOLA) new_post
