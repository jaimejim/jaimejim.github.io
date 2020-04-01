#!/usr/bin/env bash
set -e # halt script on error

gem update --system
gem install 
gem install mercenary -v 0.3.6
gem install jekyll html-proofer
gem install jekyll -v 2.5

bundle install
bundle update pygments.rb
bundle exec jekyll build
#bundle exec htmlproofer ./_site --file-ignore /_site/drafts/ /_site/slides/ /_site/projects/appiot/ --disable-external
