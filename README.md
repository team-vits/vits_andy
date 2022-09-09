# ViTS project

It is a web app project dedicated to the improvement and reconstruction of human well-being through 4 fundamental pillars: nutrition, physical training, rest, emotional management.

This web app has a strong scientific basis where we combine the best of classic literature with the latest scientific discoveries to always provide the best quality to our clients, all this under the premise that each person has special circumstances and require compassion and empathy throughout the process. For this reason our process consists of a continuous accompaniment during which we help to break down fears, myths and false expectations through education, generating a new belief system where they feel capable of achieving the proposed goals by having a clear path, a guiding hand and results on which to rely.

## INTRODUCTION

This repository contains the django project files. This files are needed to create the web app for ViTS startup.

## REQUIREMENTS

We are working with these technologies and programming languages:

* **Docker**. [Installation instruction](https://docs.docker.com/engine/install/)
* **Docker compose**. [Installation instruction](https://docs.docker.com/compose/install/)
* **Python 3.8.10**. [Documentation](https://www.python.org/downloads/release/python-3810/)
* **mysqlclient**. Follow these commands to install it on linux:
    ```
    sudo apt update
    sudo apt upgrade
    sudo apt install mysql-client
    ```

## USAGE

This project works with docker container. So, you have to build the services for the django project and MySQL database. Follow these steps:

### Set up containers

1. From the project folder run ```docker compose up -d```
2. Verify that the two containers are running, use ```docker ps```
3. The django container is already running the sever at http://localhost:8000/. You can check it on your browser.

### Start development

1. Go to project folder and create a python environment. Use ```python3 -m venv venv```
2. Activate environment. Use ```source venv/bin/activate```
3. Run the package installer for Python. Use ```pip install -r requirements.txt```
4. You can start to CODE!!!

## MAINTAINERS

Developers:

 * Andres Lopez
 * Daniel Cortes
 * Diego Lopez

Product Manager:

 * Jhonattan Oviedo
