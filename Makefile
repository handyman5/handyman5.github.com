run: serve

build: $(NIKOLA)
	$(NIKOLA) build

VENV_BIN = venv/bin
NIKOLA = $(VENV_BIN)/nikola

$(VENV_BIN)/nikola:
	python3 -m venv venv
	$(VENV_BIN)/pip install 'Nikola[extras]'

serve: $(NIKOLA)
	# https://serialized.net/2013/04/nikola-and-livereload-ftw/
	while inotifywait -r posts; do $(NIKOLA) build; done &
	$(NIKOLA) serve

new: $(NIKOLA)
	$(NIKOLA) new_post
