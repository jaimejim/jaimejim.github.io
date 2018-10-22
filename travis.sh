#!/usr/bin/env bash
set -e # halt script on error

#gem install jekyll html-proofer

bundle install
bundle update pygments.rb
bundle exec jekyll build
#bundle exec htmlproofer ./_site --file-ignore /_site/drafts/ /_site/slides/ /_site/projects/appiot/ --disable-external
