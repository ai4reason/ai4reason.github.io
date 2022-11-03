#!/bin/bash

mkdir -p vendor/bundle
export JEKYLL_VERSION=3.8
docker run --rm --volume="$PWD:/srv/jekyll:Z" --volume="$PWD/vendor/bundle:/usr/local/bundle:Z" --publish 4000:4000 jekyll/builder:$JEKYLL_VERSION jekyll serve

