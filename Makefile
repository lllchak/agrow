INTERPRETER=python
BASE_INTERPRETER=python3
SRC_DIR = .
CACHE := $(shell find $(SRC_DIR) -name __pycache__ | sed -e 's/\.\///')

# virtual environment name
ename ?= ""
# *_requirements.txt file name 
rname ?= ""
# package to be installed name
pname ?= ""
# test to be executed
tname ?= ""

# Rule to run creating virtual environment commands. It checks
# if environment already installed and if it's not, 'cenv' rule
# installs one.
cenv:
ifeq ("$(wildcard venvs/$(ename))", "")
	@echo "$(MAKE): Installing new virtual environment..."
	@($(BASE_INTERPRETER) -m venv venvs/$(ename))
	@echo "$(MAKE): Virtual environment successfully installed"
else
	@echo "$(MAKE): Virtual environment already satisfied [./venvs/$(ename)]"
endif

# Rule to run requirements installation command. It takes requirements
# from provided requirements file (all stored in ./requirements directory).
# Also you can install exact package (without using requirements) by providing 
# its name with pname Makefile flag.
idep:
ifeq ($(rname), "")
	@pip install $(pname)
else
	@pip install -r requirements/$(rname)_requirements.txt
endif

# Rule to run requirements uninstallation command. It removes requirements
# from provided requirements file (all stored in ./requirements directory).
# Also you can uninstall exact package (without using requirements) by providing 
# its name with pname Makefile flag.
udep:
ifeq ($(rname), "")
	@pip uninstall $(pname) -y
else
	@pip uninstall -r requirements/$(rname)_requirements.txt -y
endif

# Rule for upgrading given package
upkg:
	@pip install --upgrade $(pname)

# Rule for cleaning trash files adn directories
clean:
	@rm -rf $(CACHE)

