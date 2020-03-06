**[This project was sunsetted](https://blog.mozilla.org/foundation-archive/mozilla-science/news-from-mozilla-science-lab/) in September 2018. More information can be found at the [ScienceLab wiki](https://wiki.mozilla.org/ScienceLab).**

# api.mozillascience.org
django API application for mozillascience.org

[![Build Status](https://travis-ci.org/mozilla/api.mozillascience.org.svg?branch=master)](https://travis-ci.org/mozilla/api.mozillascience.org)

## Getting started

To start working with the API server locally, you will need to make sure you have the following prerequisite dependencies installed.

1. [git](https://git-scm.com/)
2. python3
3. pip
4. virtualenv (optional)


Once you have all dependencies installed, you can start by forking and cloning the project to your local machine.

```
git clone https://github.com/mozilla/api.mozillascience.org.git
```

Create a virtual environment using either `virtualenv` or `python3`'s virtual environment invocation. For the purposes of this README.md it is assumed you called this virtual environment `venv`.

Activate the virtual environment.

- Unix/Linux/OSX: `source venv/bin/activate`
- Windows: `venv\Scripts\Activate`

(for both, the virtual environment can be deactivated by running the corresponding "deactivate" command)

Install all dependencies into the virtual environment:

```bash
pip install -r requirements.dev.txt
```

## Setup

```bash
cp env.sample .env
python app/manage.py migrate
python app/manage.py createsuperuser
```

You can now run the server using:

```bash
python app/manage.py runserver
```

As this is a Python/Django project, we also support additional commands that might be of use. Please consult the following table for some common commands you might want to use:

| No. | Command | Description |
| --- | ------- | ----------- |
| 1. | flake8 app --config=./app/tox.ini | Run Flake8 linting on the code.  |
| 2. | python app/manage.py test | Run the tests defined for this project. |
| 3. | python app/manage.py makemigrations | Create migration files for all Django model changes detected. |
| 4. | python app/manage.py migrate | Apply migrations to the database. |
| 5. | python app/manage.py shell | Open up a Python interactive shell. |
| 6. | python app/manage.py createsuperuser | Create a super user for the Django administrative interface. |
| 7. | python app/manage.py collectstatic | Create a folder containing all the static content that needs to be served for use by the API and the admin interface. |

## Environment Variables

|Variable|Value|About|
|--------|-----|-----|
| GH_TOKEN | String | Optional, token only required if you are going to be using it extensively.|
| DATABASE_URL | URL | Required: URL to your postgres database e.g. `postgres://<USER>:<PASSWORD>@<HOSTNAME>:<PORT>/<DBNAME>`|
| DJANGO_SECRET_KEY | String | Required: anything that is something people can't guess!|
| DEBUG | Boolean | Required: `True` or `False` |
| CORS_WHITELIST | String | Optional, comma separated list of domains (without space), e.g. `google.ca,.herokuapp.com`. For allowing all domains, set to `*`|
| CORS_REGEX_WHITELIST | String | Optional, comma separated list of domain regex patterns (without space), e.g. `^(https?://)?(\w+\.)?google\.com$,\.herokuapp\.com$`|
| USE_S3| Boolean | default is True. Do we want to use s3 for media uploads? |
| SECURE_SSL_REDIRECT | Boolean | Redirect insecure requests to HTTPS. Defaults to `False` |
| SECURE_SSL_HOST | String | The host that the secure redirect should use. If not set, the host is not modified |

Also envs `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_STORAGE_BUCKET_NAME`, `AWS_S3_CUSTOM_DOMAIN`, `AWS_LOCATION`, `FILEBROWSER_DIRECTORY` are **required** if `USE_S3` is True. For more info see [filebrowser_s3 documentation](https://github.com/Pomax/filebrowser_s3#variables-documentation)

### Deployment

The API server uses [Heroku](https://www.heroku.com/) for its deployment services, and the current workflow is that
every push to `master` will deploy a new version of this app to the staging server on heroku (assuming travis CI passes before it deploys).
The production server is deployed from the staging server using the Heroku [Pipelines](https://devcenter.heroku.com/articles/pipelines) to promote to production.
