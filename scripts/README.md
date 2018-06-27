# Scripts

## Purpose

This folder contains seldom used scripts that are not specifically a part of the application itself, but are needed as support tools to make the application useful.

## Language

Since this is primarily a Python project, it is preffered that this folder should Python scripts. However, Bash or Windows scripts can be used when needed.

The language is not crucial here since these scripts will most likely be run by the creator(s) and maintainer(s) of the script rather than by everyone who contributes to the project.

### Using Python scripts

It is recommended that you use Python 3.6 or above and pip 10 or above and setup a virtual environment to install your dependencies into. This can be done by running the following commands in the current folder.

1. `pyvenv env` or on Windows `C:\Python35\python C:\Python35\Tools\Scripts\pyvenv.py env`

2. `source env/bin/activate` or on Windows `env/Scripts/activate.bat`

To install dependencies run:
`pip install -r requirements.txt`

Once you have finished running your scripts, you can deactivate your virtual environment by running:
`deactivate` or on Windows `env/Scripts/deativate.bat`
