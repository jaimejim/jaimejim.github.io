#!/usr/bin/env bash
set -e # halt script on error

gem install jekyll html-proofer

bundle install
bundle exec jekyll build
bundle exec htmlproofer ./_site --file-ignore ./_site/drafts/*.html ./_site/temp/*.html
