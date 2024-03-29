include help.mk

.DEFAULT_GOAL := start-quick

ROOT_DIR := $(dir $(realpath $(lastword $(MAKEFILE_LIST))))

.PHONY: init 
init: venv update-dependencies ## inital setup of project

.PHONY: venv
venv:
	@python -m venv ${ROOT_DIR}.venv

.PHONY: update-dependencies
update-dependencies: ## install all dependencies
	@git pull
	${ROOT_DIR}.venv/Scripts/pip install -r requirements.txt

.PHONY: save-dependencies
save-dependencies: ## save current dependencies
	${ROOT_DIR}.venv/Scripts/pip freeze > requirements.txt

.PHONY: start
start: ## runs the script with default parameters
	@${ROOT_DIR}.venv/Scripts/python ${ROOT_DIR}main.py --input-directory ${ROOT_DIR}input --output-directory ${ROOT_DIR}output

.PHONY: start-quick
start-quick: ## runs the script with less fine granular (recommended for 4k videos)
	@${ROOT_DIR}.venv/Scripts/python ${ROOT_DIR}main.py --input-directory ${ROOT_DIR}input --output-directory ${ROOT_DIR}output --sample-rate 2 --noise-threshold 2

.PHONY: clean
clean: clean-output ## clean output folder
	@docker run --rm -v ${ROOT_DIR}/input:/mnt busybox sh -c "find /mnt/ -mindepth 1 -maxdepth 1 ! -name .git* -exec rm -r {} \;"

.PHONY: clean-output
clean-output: ## clean input and output folder
	@docker run --rm -v ${ROOT_DIR}/output:/mnt busybox sh -c "find /mnt/ -mindepth 1 -maxdepth 1 ! -name .git* -exec rm -r {} \;"

