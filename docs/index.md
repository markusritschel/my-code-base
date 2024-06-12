![](_static/logo.png)

## Introduction

Welcome to the documentation of *My Code Base*!

This is a collection of routines that I've developed over time and that I use in my daily work.

```{tip}
- Give a short introduction on what the project is about.
- Limit yourself to just a few sentences.
- Mention any preknowledge the user must have for the project.
- You may also give some instructions on how to navigate through the documentation.
```

## Getting Started

### Installation

#### Install via pip

The easiest way to install the package is via pip directly from this repository:

```bash
$ pip install git+https://github.com/markusritschel/my_code_base.git
```

#### Clone repo and install locally

Alternatively, clone the repo and use the *Make* targets provided.
First, run

```bash
make conda-env
# or alternatively
make install-requirements
```

to install the required packages either via `conda` or `pip`, followed by

```bash
make src-available
```

to make the project's routines (located in `src`) available for import.

### Test code

You can run

```bash
make tests
```

to run the tests via `pytest`.

### Usage

The package can be imported and used as follows:

```python
import my_code_base as mcb
```


## Contact

For any questions or issues, please contact me via git@markusritschel.de or open an [issue](https://github.com/markusritschel/my-code-base/issues).
