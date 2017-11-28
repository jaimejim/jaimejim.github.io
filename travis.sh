#!/usr/bin/env bash
set -e # halt script on error

#gem install jekyll html-proofer

bundle install --full-index
bundle exec jekyll build
bundle exec htmlproofer ./_site --file-ignore /_site/drafts/ --disable-external
