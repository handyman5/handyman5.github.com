build: $(NIKOLA)
	$(NIKOLA) build

VENV_BIN = venv/bin
NIKOLA = $(VENV_BIN)/nikola

$(VENV_BIN)/nikola:
	python3 -m venv venv
	$(VENV_BIN)/pip install 'Nikola[extras]'

serve: $(NIKOLA)
	$(NIKOLA) serve

new: $(NIKOLA)
	$(NIKOLA) new_post
