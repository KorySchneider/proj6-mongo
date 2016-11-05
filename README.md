# proj6-mongo

_Kory Schneider_

_CIS 322, Fall 2016_

## What is this?
This is a simple web program that uses [MongoDB](https://www.mongodb.com/) to
store memos (which in this case are strings of text with an associated date).

## Installation
First clone the repository:

    $ cd where/you/want/it
    $ git clone https://github.com/koryschneider/proj6-mongo
    $ cd proj6-mongo

Then you will need to create a couple files containing credentials and some configuration:

    $ mkdir secrets; cd secrets
    $ touch admin_secrets.py
    $ touch client_secrets.py

To see examples of `*_secrets.py`, see the [main project repository](https://github.com/UO-CIS-322/proj6-mongo/tree/master/secrets).
Some of the fields in `client_secrets.py` is not necessary to run the program,
as it was simply used for grading. These fields are `author`, `repo`, and `server_main`.

Finally, set up the environment and run the server:

    $ bash configure && make service

## Usage

`$ make service` will start a Green Unicorn (gunicorn) server, which is more suitable for running over a long period of time.

`$ make run` will launch the server in debugging mode.

`$ make test` will run the test suite.

## Credit

Forked from Michal Young at https://github.com/UO-CIS-322/proj4-brevets for CIS 322: Intro to Software Engineering.
