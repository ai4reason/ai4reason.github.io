#!/bin/bash

export JEKYLL_VERSION=3.8
docker run --rm --volume="$PWD:/srv/jekyll:Z" --volume="$PWD/vendor/bundle:/usr/local/bundle:Z" -it jekyll/builder:$JEKYLL_VERSION bundle update

