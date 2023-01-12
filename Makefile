INTERPRETER=python
BASE_INTERPRETER=python3
UPGADE_PIP=$(pip install --upgrade $1)

req_install:
	@VENVNAME=$(shell bash -c 'read -p "Input virtual environment name: " venvname; echo $$venvname')
	@BASE_REQ=$(shell bash -c 'read -p "Input base requirements.txt name: " req_name; echo $$req_name')

ifeq ("$(wildcard '/venvs/$(VENVNAME)')", "")
	$(BASE_INTERPRETER) -m venv 'venvs/$(VENVNAME)'
	source venvs/$(VENVNAME)/bin/activate
else
	@source venvs/$(VENVNAME)/bin/activate
endif

	@pip install -r ${req_name}_requirements.txt

upkg:
	$(UPGADE_PIP)