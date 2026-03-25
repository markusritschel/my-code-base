# My Code Base <!-- omit in toc -->

[![build](https://github.com/markusritschel/my-code-base/actions/workflows/main.yml/badge.svg)](https://github.com/markusritschel/my-code-base/actions/)

[![License MIT license](https://img.shields.io/github/license/markusritschel/my-code-base)](./LICENSE)


This is a collection of routines that I've developed over time and that I use in my daily work.



## <u>Table of Contents</u> <!-- omit in toc -->
<!-- Automatically created in VSCode with the `Markdown All in One` extension -->

- [Preparation](#preparation)
  - [Cloning the project to your local machine](#cloning-the-project-to-your-local-machine)
  - [Setup](#setup)
- [Testing](#testing)
- [Maintainer](#maintainer)
- [Contact \& Issues](#contact--issues)


## Preparation

### Cloning the project to your local machine

To reproduce the project, clone this repository on your machine

```bash
git clone https://github.com/markusritschel/my-code-base
```


### Setup

Then, in the new directory (`cd my-code-base/`) install the package via:
```
pip install .
```
or via
```
pip install -e .
```
if you plan on making changes to the code.

Alternatively, install directly from GitHub via
```
pip install 'git+https://github.com/markusritschel/my-code-base.git'
```

## Testing
Run `make tests` in the source directory to test the code.
This will execute both the unit tests and docstring examples (using `pytest`).

Run `make lint` to check code style consistency.



## Maintainer

- [markusritschel](https://github.com/markusritschel)

## Contact & Issues

For any questions or issues, please contact me via git@markusritschel.de or open an [issue](https://github.com/markusritschel/my-code-base/issues).

***

&copy; [Markus Ritschel](https://github.com/markusritschel), 2026
