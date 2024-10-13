SRC=.
OUTPUT_DIR=./out
INSTALL_DIR=/usr/local/bin
TARGETS=nocvy

.PHONY: all out install uninstall
all: $(TARGETS)

nocvy: $(SRC)/nocvy.py out

$(TARGETS):
	cp $< $(OUTPUT_DIR)/$@ && chmod 777 $(OUTPUT_DIR)/$@

out:
	mkdir -p $(OUTPUT_DIR)

install:
	cp $(OUTPUT_DIR)/nocvy $(INSTALL_DIR)

uninstall:
	rm -rf $(OUTPUT_DIR) $(INSTALL_DIR)/nocvy
