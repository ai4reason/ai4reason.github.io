#!/bin/sh

DATA=docs/_data
MEMBERS=$DATA/members.yml
BIB=$DATA/bib.yml
PUBS=docs/download/publications

python publications/dblp-pubs.py --yaml $BIB --csv ${PUBS}.csv $MEMBERS 

python publications/to-excel.py $PUBS

