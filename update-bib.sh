#!/bin/sh

DATA=docs/_data
MEMBERS=$DATA/members.yml
BIB=$DATA/bib.yml
PUBS=docs/download/publications
CSV=${PUBS}.csv

mv $CSV ${CSV}.tmp
if ! python publications/dblp-pubs.py --yaml $BIB --csv $CSV $MEMBERS; then
   # keep the previous CSV and fail the workflow so nothing gets committed
   mv ${CSV}.tmp $CSV
   exit 1
fi

if ! diff $CSV ${CSV}.tmp > /dev/null; then
   echo "Generating Excel..."
   python publications/to-excel.py $PUBS
else
   # do not genete Excel when the CSV is unchanged
   echo "Skipped generating Excel"
fi

rm -f ${CSV}.tmp

