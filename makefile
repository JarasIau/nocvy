SRC=.
OUTPUT_DIR=./out
INSTALL_DIR=/usr/local/bin
TARGETS=noczwy

.PHONY: all out install uninstall
all: $(TARGETS)

noczwy: $(SRC)/noczwy.py out

$(TARGETS):
	cp $< $(OUTPUT_DIR)/$@ && chmod 777 $(OUTPUT_DIR)/$@

out:
	mkdir -p $(OUTPUT_DIR)

install:
	cp $(OUTPUT_DIR)/noczwy* $(INSTALL_DIR)

uninstall:
	rm -rf $(OUTPUT_DIR) $(INSTALL_DIR)/noczwy*
