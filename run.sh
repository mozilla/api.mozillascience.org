#!/bin/bash
set -e # exit with nonzero exit code if anything fails

args=("$@")
CONTAINER_CMD="docker-compose run web"
SHELL_CMD="$CONTAINER_CMD sh -c"
PYTHON_CMD="$CONTAINER_CMD python manage.py"

if [ ${#args[@]} == 0 ]
then
  eval $BUILD
  eval "docker-compose up -d && docker attach apimozillascienceorg_web_1"
else
  cmd=${args[0]}

  if [ $cmd == "test" ]
  then
    eval $BUILD
    eval "$SHELL_CMD \"flake8 . && python manage.py test\""

  elif [ $cmd == "env" ]
  then
    eval "cp env.sample .env"

  elif [ $cmd == "migrate" ]
  then
    eval "$PYTHON_CMD migrate"

  elif [ $cmd == "makemigrations" ]
  then
    eval "$PYTHON_CMD makemigrations"

  elif [ $cmd == "shell" ]
  then
    eval "$CONTAINER_CMD sh"

  elif [ $cmd == "pyshell" ]
  then
    eval "$PYTHON_CMD shell"

  elif [ $cmd == "createsuperuser" ]
  then
    eval "$PYTHON_CMD createsuperuser"

  else
    echo "ERROR: Unknown command"
  fi

fi
