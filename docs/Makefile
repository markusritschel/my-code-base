# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = my-code-base
SOURCEDIR     = source
BUILDDIR      = _build

AUTODOCBUILD  = sphinx-apidoc
MODULEDIR     = ../src/my_code_base
AUTODOCDIR    = api


# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help clean, doc-requirements Makefile

clean:
	rm -rf $(BUILDDIR)/* $(AUTODOCDIR)

$(AUTODOCDIR): $(MODULEDIR)
	mkdir -p $@
	$(AUTODOCBUILD) -f -o $@ $^

doc-requirements: $(AUTODOCDIR)

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
