# NLP Playground
### Environment
All of projects were built using:
- Python 3.10.6 (pip 22.3.1)
- make
- WSL Ubuntu 20.04
- Colab (mostly like a terminal with GPU)

So there is no need in special hardware to reproduce any results.

**Note**: You can find pre-built virtual environments in `./venvs` folder 
if needed.

### Setting up new virtual environment
Despite you can use pre-installed virtual environments, it is also available to create new environment and install dependencies to it using `./Makefile`. To create new virtual environment run
```bash
make cenv ename=<NEW_ENV_NAME>
```
**Note**: make sure you activated created environment right after you installed it (`source venvs/<NEW_ENV_NAME>/bin/activate). It would help you to avoid global dependency installing problem.

After environment is installed (installs in `./venvs` folder by default. Intalling to provided directory is yet to come) you can add dependecies from provided requirements file to it running
```bash
make idep rname=<REQUIREMENTS_NAME> (from ./requirements)
```

Or install exact dependency(-ies) running
```bash
make idep pname=<PACKAGE_NAME>
```

That repository contains some educational NLP small projects. Here is 
the list of projects have been implemented at the moment:
- [Tokenizer](./tokenizer)
- [Word2Vec](./word2vec/)
