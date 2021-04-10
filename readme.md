# Mailbox As A Filesystem

Concept of alternative email client. You don't need to run separate program to check you email. 
Your emails are saved directly on disk, in folders grouped according to different rules. 
It's easy to browse and search. And quite private - after closing docker container, all local traces are removed. 

## Basics

First create account on Fastmail (or other provider), set account and password in `.env` file.
In Fastmail account options, the app_password needs to be enabled first: https://www.fastmail.com/help/clients/apppassword.html

Start app: `make run-docker` 

It will create new folder in /tmp/emails (adjustable as HOST_MAILS_DIR, see below). 

## Features

Inside emails folder, you will see see two "filters":
* Timeline - grouped by date in yyyy/mm/dd format
* Sender - grouped by sender email

Server is optimized to only download new emails.
It doesn't download attachments.


## Options in .env

`CONTAINER_MAILS_DIR`:
Path where mail subdirectories will be created inside docker container.

`HOST_MAILS_DIR`:
Path where mail subdirectories will be created on host OS.

`HOST`:
Which IMAP server to connect to.

`REFRESH_RATE`:
How often to fetch new emails (in seconds)


## Development

Starting:

    make setup
	source mailboxfsvenv/bin/activate
	make lint

## Testing

For basic checks without real account: 

	make test-mock
	make run-mock

When you have real account setup in .env:

	make test
	make run


### TODO

- add source formatting (ie. black)
- add logger
