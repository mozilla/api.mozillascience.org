# api.mozillascience.org
django API application for mozillascience.org

[![Build Status](https://travis-ci.org/mozilla/api.mozillascience.org.svg?branch=master)](https://travis-ci.org/mozilla/api.mozillascience.org)

## Getting started

To start working with the API server locally, you will need to make sure you have the following prerequisite dependencies installed.

1. [git](https://git-scm.com/)
2. [Docker](https://docs.docker.com/engine/installation/)

Important note: You will have to make sure that you have successfully run the `Docker Quickstart Terminal` to get the `DEFAULT` VirtualBox configured to start working locally.

To verify that you should see this nice little graphic:

```

                        ##         .
                  ## ## ##        ==
               ## ## ## ## ##    ===
           /"""""""""""""""""\___/ ===
      ~~~ {~~ ~~~~ ~~~ ~~~~ ~~~ ~ /  ===- ~~~
           \______ o           __/
             \    \         __/
              \____\_______/
```


Once you have both dependencies installed, you can start by forking and cloning the project to your local machine.

```
git clone https://github.com/mozilla/api.mozillascience.org.git
```

## Running your application

Here are a list of commands you can run that are relevant to working with this project.

If you are on a UNIX-based system, run each command using:
```
sh run.sh <command_name>
```
where `<command_name>` should be replaced by one of the commands in the table below.

If you are on a Windows system, run each command using:
```
run.bat <command_name>
```
where `<command_name>` should be replaced by one of the commands in the table below.

**To just start up the application, refer to command 2 below**

|No.|Command|Description|
|--------|-----|-----|
| 1. | env | Setup your environment with the default configuration. |
| 2. | | Start the application by not passing in a command name. Remember to run the `env` command first before this. |
| 3. | test | Run tests for this project. |
| 4. | makemigrations | Create migration files to reflect model changes. Run this whenever you make changes to a model. |
| 5. | migrate | Apply migrations to the database. |
| 6. | shell | Open up a Bash shell in the docker container to run shell commands. |
| 7. | pyshell | Open up a Python interactive shell in the docker container. |
| 8. | createsuperuser | Create a super user for the Django administrative interface. |
| 9. | schema-image | Generate a database schema visualization and add it to your file tree in the `app` folder as `db_schema.png`. This is automatically done when you run the `makemigrations` command. |

## Environment Variables

|Variable|Value|About|
|--------|-----|-----|
| GH_TOKEN | String | Optional, token only required if you are going to be using it extensively.|
| DATABASE_URL | URL | Required: URL to your postgres database e.g. `postgres://<USER>:<PASSWORD>@<HOSTNAME>:<PORT>/<DBNAME>`|
| DJANGO_SECRET_KEY | String | Required: anything that is something people can't guess!|
| DEBUG | Boolean | Required: `True` or `False` |
|CORS_WHITELIST| String | Optional, comma separated list of domains (without space), e.g. `google.ca,.herokuapp.com`. For allowing all domains, set to `*`|
|CORS_REGEX_WHITELIST| String | Optional, comma separated list of domain regex patterns (without space), e.g. `^(https?://)?(\w+\.)?google\.com$,\.herokuapp\.com$`|

### Running python commands

Sometimes you will need to run a specific python/django command in the container, to accomplish this you will need to run:

```
docker-compose run web <your command here>
```

NOTE: Replace `<your command here>` with an actual command, for example: `docker-compose run web echo 'hello world'`

### Generating a visualization of the database schema

To generate an image representing the schema of the database (which creates a `db_schema.png` file in the `app` directory) run the following command:

```
sh run.sh schema-image
```

or on Windows:
```
run.bat schema-image
```

NOTE: Whenever you make a change to a model and create a migration for it, the schema visualization is automatically updated. Remember to commit these changes.

### Deployment

The API server uses [Heroku](https://www.heroku.com/) for its deployment services, and the current workflow is that
every push to `master` will deploy a new version of this app to the staging server on heroku (assuming travis CI passes before it deploys).
The production server is deployed from the staging server using the Heroku [Pipelines](https://devcenter.heroku.com/articles/pipelines) to promote to production.
