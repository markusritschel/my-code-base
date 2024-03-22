# This is a self-documenting Makefile.
# For details, check out the following resources:
# https://gist.github.com/klmr/575726c7e05d8780505a
# https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html

# ======= Put your targets etc. between here and the line which is starting with ".DEFAULT_GOAL" =======
# Document any rules by adding a single line starting with ## right before the rule (see examples below)
# ======================================================================================================

.PHONY: docs

## Clean-up python artifacts, logs and jupyter-book built
cleanup: clean-pyc clean-logs clean-docs

## Cleanup python file artifacts
clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +


## Cleanup log files
clean-logs:
	find ./logs -iname '*.log' -type f -exec rm {} +


## Cleanup docs
clean-docs:
	jb clean --all docsrc/


## Generate documentation
docs:
	jb build docsrc


## Test github actions locally
test-gh-actions:
	mkdir /tmp/artifacts
	act push --artifact-server-path /tmp/artifacts --container-options "--userns host" --action-offline-mode

## Run pytest
tests:
	pytest --doctest-modules -v .

## Run flake8 linter
lint:
	flake8 my_code_base


## Sync Jupyter notebooks
sync-nb:
	jupytext --sync notebooks/**/*.ipynb


## Update the requirements.txt
save-requirements:
	pip list --format=freeze > requirements.txt


## Create a conda environment.yml file
save-conda-env:
	pip_packages=$$(conda env export | grep -A9999 ".*- pip:" | grep -v "^prefix: ") ;\
	conda env export --from-history | grep -v "^prefix: " > environment.yaml ;\
	echo "$$pip_packages" >> environment.yaml ;\
	sed -ie 's/name: base/name: $(CONDA_DEFAULT_ENV)/g' environment.yaml; \
	echo "$$CONDA_DEFAULT_ENV"


## Install Python Dependencies via pip
install-requirements:
	python -m pip install -U pip setuptools wheel
	mamba install --file requirements.txt
	pip install sphinxcontrib-napoleon2 rinohtype sphinx-rtd-theme sphinx-autodoc-defaultargs nbsphinx myst-parser sphinx-issues sphinxcontrib-bibtex
	# python -m pip install -r requirements.txt


## Make the source code as package available
src-available:
	pip install -e .


## Create a conda environment named after the project slug, install packages, and activate it
setup-conda-env:
	@echo "Install mamba"
	conda install -c conda-forge mamba
	@echo "Create conda environment '{{ cookiecutter.project_slug }}'"
	mamba env create --file environment.yml
	@echo "Activate conda environment '{{ cookiecutter.project_slug }}'"
	conda activate {{ cookiecutter.project_slug }}


## Check if all packages listed in requirements.txt are installed in the current environment
test-requirements:
	@echo "Check if all packages listed in requirements.txt are installed in the current environment:"
	# the "|| true" prevents the command returning an error if grep does not find a match
	python -m pip -vvv freeze -r requirements.txt | grep "not installed" || true



# ==================== Don't put anything below this line ====================
# https://www.digitalocean.com/community/tutorials/how-to-use-makefiles-to-automate-repetitive-tasks-on-an-ubuntu-vps
.DEFAULT_GOAL := show-help
show-help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)";echo;sed -ne"/^## /{h;s/.*//;:d" -e"H;n;s/^## //;td" -e"s/:.*//;G;s/\\n## /---/;s/\\n/ /g;p;}" ${MAKEFILE_LIST}|LC_ALL='C' sort -f|awk -F --- -v n=$$(tput cols) -v i=21 -v a="$$(tput setaf 6)" -v z="$$(tput sgr0)" '{printf"%s%*s%s ",a,-i,$$1,z;m=split($$2,w," ");l=n-i;for(j=1;j<=m;j++){l-=length(w[j])+1;if(l<= 0){l=n-i-length(w[j])-1;printf"\n%*s ",-i," ";}printf"%s ",w[j];}printf"\n";}'|more