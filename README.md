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


Once you have both dependencies installed, you can start by fork and clone the project to your local machine.

```
git clone https://github.com/mozilla/api.mozillascience.org.git
```

Once you have cloned the project, make sure you run the following command first:

```
make cpenv
```

This will create a simple environment for local development then you can start working on the project by running this command:

```
make up
```
