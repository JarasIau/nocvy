SRC=./src
OUTPUT_DIR=./out
INSTALL_DIR=/usr/local/bin
TARGETS=swdet swdet-mt

.PHONY: all out install uninstall
all: $(TARGETS)

swdet: $(SRC)/swdet.py out
swdet-mt: $(SRC)/swdet-mt.py out

$(TARGETS):
	cp $< $(OUTPUT_DIR)/$@ && chmod 777 $(OUTPUT_DIR)/$@

out:
	mkdir -p $(OUTPUT_DIR)

install:
	cp $(OUTPUT_DIR)/swdet* $(INSTALL_DIR)

uninstall:
	rm -rf $(OUTPUT_DIR) $(INSTALL_DIR)/swdet*
