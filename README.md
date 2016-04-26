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

Once you have cloned the project, make sure you run the following command first:

```
make cpenv
```
This will create a simple environment for local development then you can start working on the project by running this command:

## Environment Variables

|Variable|Value|About|
|--------|-----|-----|
| GH_TOKEN | String | Optional, token only required if you are going to be using it extensively.|
| DATABASE_URL | URL | Required: URL to your postgres database e.g. `postgres://<USER>:<PASSWORD>@<HOSTNAME>:<PORT>/<DBNAME>`|
| DJANGO_SECRET_KEY | String | Required: anything that is something people can't guess!|
| DEBUG | Boolean | Required: `True` or `False` |

### Database migration

You'll also need run the migration script from time to time to keep up to date with the model, and to accomplish that you can simply run:

```
make migrate
```

### Start the server

After you have created the environment file using `make cpenv` and ran the migration script using `make migrate` you can now run the server by simply run:

```
make up
```

### Running python commands

Sometimes you will need to run a specific python/django command in the container, to accomplish this you will need to run:

```
docker-compose run web <your command here>
```

NOTE: Replace `<your command here>` with an actual command, for example: `docker-compose run web echo 'hello world'`

### Deployment

The API server uses [Heroku](https://www.heroku.com/) for its deployment services, and the current workflow is that
every push to `master` will deploy a new version of this app to the staging server on heroku (assuming travis CI passes before it deploys).
The production server is deployed from the staging server using the Heroku [Pipelines](https://devcenter.heroku.com/articles/pipelines) to promote to production.
