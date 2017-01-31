#!/bin/bash

DBNAME="studyriffic"
DBPORT=21205
DBUSER=example
DBPASS=example
DBHOST=localhost
mongo "${DBHOST}:${DBPORT}/${DBNAME}" -u ${DBUSER} -p ${DBPASS} --eval 'db.dropDatabase();'
printf "Remember to remove exported/backed up data as well!\n"

