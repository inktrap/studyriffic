#!/bin/bash

OUTPUT_DIR="/var/www/virtual/example/data.example.subdomain.uberspace.de"
DBNAME="studyriffic"
DBPORT=27017
DBUSER=example
DBPASS=example
DBHOST=localhost
COLLECTIONS=$(mongo --quiet "${DBHOST}:${DBPORT}/${DBNAME}" -u ${DBUSER} -p ${DBPASS} --eval 'print(db.getCollectionNames());')
# append local bin to path if it is there
if [[ -d $HOME/bin ]]; then
    export PATH=$PATH:$HOME/bin
fi
FDUPES=$(which fdupes 2>/dev/null || true)

if [[ ! -d "$OUTPUT_DIR" ]];then
    (>&2 printf "Output directory %s does not exist!\n" "${OUTPUT_DIR}")
    exit 1
fi

if [[ ! -d "$OUTPUT_DIR/json" ]];then
    mkdir "${OUTPUT_DIR}/json" || exit 1
fi
#if [[ ! -d "$OUTPUT_DIR/zip" ]];then
#    mkdir "${OUTPUT_DIR}/zip" || exit 1
#fi

if [[ ! -f "${OUTPUT_DIR}/.htaccess" ]]; then
    (>&2 printf "No access restriction via .htaccess file found in OUTPUT_DIR!\n")
    exit 1
fi

IFS=',' read -ra COLLECTION <<< "$COLLECTIONS"
for i in "${COLLECTION[@]}"; do
    if [ "$i" != "system.indexes" ]; then
        THIS_DATE=$(date +%Y-%m-%d_%H%M%S)
        mongoexport --quiet --jsonArray -h ${DBHOST}:${DBPORT} -d ${DBNAME} -u ${DBUSER} -p ${DBPASS} --collection "${i}" -o "${OUTPUT_DIR}/json/${DBNAME}_${i}-${THIS_DATE}.json"
    fi
done

# junk the paths, be quiet, be recursive
OUTPUT=$(zip -j -q -r "${OUTPUT_DIR}/current.zip" "${OUTPUT_DIR}/json" 2>&1)
# do not raise an error if there are no files to zip
# else: print the error to stderr and fail
if [[ "$OUTPUT" != *"zip error: Nothing to do!"* && "${OUTPUT}" ]]; then
    (>&2 echo "$OUTPUT")
    exit 1
fi

# delete duplicate backups
if [[ -x $FDUPES && $FDUPES && -d $OUTPUT_DIR && $OUTPUT_DIR ]]; then
    ## test run:
    # $FDUPES --reverse --order=time --recurse --noempty ${OUTPUT_DIR}
    # deletes without output
    $FDUPES --reverse --order=time --recurse --noempty --noprompt --delete --quiet ${OUTPUT_DIR} > /dev/null
fi

# zipfile by date
# cp "${OUTPUT_DIR}/current.zip" "${OUTPUT_DIR}/zip/${THIS_DATE}.zip" 

