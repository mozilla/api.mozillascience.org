SETLOCAL ENABLEEXTENSIONS

IF "%1"=="" (
    %build%
    docker-compose up -d
    docker attach apimozillascienceorg_web_1
) ELSE (
    CALL :CMD_%1
    IF ERRORLEVEL 1 CALL :ERROR
)

:CMD_test
  %build%
  docker-compose run web sh -c "flake8 . && python manage.py test"
  GOTO :EOF

:CMD_env
  COPY env.sample .env
  GOTO :EOF

:CMD_migrate
  docker-compose run web python manage.py migrate
  GOTO :EOF

:CMD_makemigrations
  docker-compose run web python manage.py makemigrations
  GOTO :EOF

:CMD_shell
  docker-compose run web sh
  GOTO :EOF

:CMD_pyshell
  docker-compose run web python manage.py shell
  GOTO :EOF

:CMD_createsuperuser
  docker-compose run web python manage.py createsuperuser
  GOTO :EOF

:ERROR
  ECHO ERROR: Unknown command
  GOTO :EOF
