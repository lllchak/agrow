# NLP Playground
# Table of content
- [Environment](#environment)
- [For developers](#for-developers)
    * [Running tests](#running-tests)
- [Subprojects structure](#subprojects-structure)
## Environment
All of projects were built using:
- Python 3.10.6 (pip 22.3.1)
- WSL Ubuntu 20.04
- Colab (mostly like a terminal with GPU)

So there is no need in special hardware to reproduce any results.

## For developers
### Setting up and removing virtual environment
It is available to create new environment and install dependencies to it using `./Makefile`. To create new virtual environment run
```bash
make cenv ename=<NEW_ENV_NAME>
```

**Note**: make sure you activated created environment right after you installed it (`source venvs/<NEW_ENV_NAME>/bin/activate`). It would help you to avoid global dependency installing problem.

After environment is installed (installs in `./venvs` folder by default. Intalling to provided directory is yet to come) you can add dependecies from provided requirements file to it running
```bash
make idep rname=<REQUIREMENTS_NAME> (from ./requirements)
```

Or install exact dependency(-ies) running
```bash
make idep pname=<PACKAGE_NAME>
```

To remove existing virtual environment run
```bash
make renv ename=<ENV_NAME>
```

### Running tests
```
```

### Subprojects structure
That repository contains some educational NLP small projects. Here is
the list of projects have been implemented at the moment:
- [Tokenizers](./tokenizers)

Here you can find different tokenizers implementations (mostly based on regular expressions extraction).

- [Vectorizers](./vectorizers/)

Here there are some implementations of sentences vectorizers (count-based only). You can find more advanced approaches in `./embedders` (yet to come).
