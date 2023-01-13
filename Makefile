INTERPRETER=python
BASE_INTERPRETER=python3

# virtual environment name
ename ?= ename
# *_requirements.txt file name 
rname ?= rname
# package to be installed name
pname ?= pname
# test to be executed
tname ?= tname

# Rule to run creating virtual environment commands. It checks
# if environment already installed and if it's not, 'cenv' rule
# installs one.
cenv:
ifeq ("$(wildcard venvs/$(ename))", "")
	@echo "$(MAKE): Installing new virtual environment..."
	@($(BASE_INTERPRETER) -m venv venvs/$(ename))
else
	@echo "$(MAKE): Virtual environment already satisfied [./venvs/$(ename)]"
endif

# Rule to run requirements installation command. It takes requirements
# from provided requirements file (all stored in ./requirements directory)
idep:
	@pip install -r requirements/$(rname)_requirements.txt

# Rule for upgrading given package
upkg:
	@pip install --upgrade $(pname)

