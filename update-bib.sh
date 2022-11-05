#!/bin/sh

cd publications
./dblp-pubs.py --yaml > bib.yml
mv ../docs/_data/bib.yml bib-old.yml
cp bib.yml ../docs/_data/

