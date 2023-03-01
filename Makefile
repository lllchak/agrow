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
# docker image id
iid ?= ""

# Rule to run creating virtual environment commands. It checks
# if environment is already installed and if it's not, 'cenv' rule
# installs one.
cenv:
ifeq ("$(wildcard venvs/$(ename))", "")
	@echo "$(MAKE): Installing virtual environment '$(ename)'..."
	@($(BASE_INTERPRETER) -m venv venvs/$(ename))
	@echo "$(MAKE): Virtual environment '$(ename)' successfully installed"
else
	@echo "$(MAKE): Virtual environment already installed [./venvs/$(ename)]"
endif

# Rule to run virtual environment removing. If checks if environment
# exists and removes it, otherwise do nothing
renv:
ifeq ("$(wildcard venvs/$(ename))", "")
	@echo "$(MAKE): Virtual environment '$(ename)' does not exist"
else
	@echo "$(MAKE): Removing virtual environment '$(ename)'..."
	@(rm -rf "venvs/$(ename)")
	@echo "$(MAKE): Virtual environment '$(ename)' successfully removed"
endif

# Rule to run requirements installation command. It takes requirements
# from provided requirements file (all stored in ./requirements directory).
# Also you can install exact package (without using requirements) by providing
# its name with pname Makefile flag.
idep:
ifeq ($(rname), "")
	@pip install $(pname)
else
	@pip install -r $(rname)
endif

# Rule to run requirements uninstallation command. It removes requirements
# from provided requirements file (all stored in ./requirements directory).
# Also you can uninstall exact package (without using requirements) by providing
# its name with pname Makefile flag.
udep:
ifeq ($(rname), "")
	@pip uninstall $(pname) -y
else
	@pip uninstall -r $(rname) -y
endif

# Rule for upgrading given package
upkg:
	@pip install --upgrade $(pname)

# Rule for removing docker images by index. If index is not provided, then
# remove all images from docker images
rimg:
ifeq ("$(shell docker images -qa)", "")
	@echo "$(MAKE): No images to remove"
else
ifeq ($(iid), "")
	@docker rmi $(shell docker images -qa)
else
	@docker rmi $(iid)
endif
endif

# Rule for force removing docker images. Behaves exactly as rimg by forces
# removing if it is not possible for any reason
rimg-force:
ifeq ("$(shell docker images -qa)", "")
	@echo "$(MAKE): No images to remove"
else
ifeq ($(iid), "")
	@docker rmi -f $(shell docker images -qa)
else
	@docker rmi -f $(iid)
endif
endif

# Rule for cleaning trash files adn directories
clean:
	@rm -rf $(CACHE)
