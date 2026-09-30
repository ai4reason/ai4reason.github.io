#!/bin/bash
# Local preview at http://localhost:4000 with the GitHub Pages build image.
# Keep IMAGE in sync with the image of actions/jekyll-build-pages@v1.

IMAGE=ghcr.io/actions/jekyll-build-pages:v1.0.13
docker run --rm -it --user "$(id -u):$(id -g)" --env HOME=/tmp \
   --env BUNDLE_GEMFILE=/Gemfile --env PAGES_REPO_NWO=ai4reason/ai4reason.github.io \
   --volume="$PWD:/srv/jekyll:Z" --workdir /srv/jekyll --publish 4000:4000 \
   --entrypoint bundle $IMAGE exec jekyll serve --host 0.0.0.0
