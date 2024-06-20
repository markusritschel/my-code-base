# Introduction

Welcome to the documentation of *My Code Base*!

This is a collection of routines that I've developed over time and that I use in my daily work.
The online documentation serves in first instance myself, providing me a kind of well-documented archive of the functions.
However, if you stumbled upon this accidentally, I hope you find some of the content useful 🙂.


## Getting Started

### Installation

#### Install via pip

The easiest way to install the package is via pip directly from this repository:

```bash
$ pip install git+https://github.com/markusritschel/my-code-base.git
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

### Usage

The package can be imported and used as follows:

```python
import my_code_base
```

### Test code

You can run

```bash
make tests
```

to run the tests via `pytest`.


## Contact

For any questions or issues, please contact me via git@markusritschel.de or open an [issue](https://github.com/markusritschel/my-code-base/issues).
