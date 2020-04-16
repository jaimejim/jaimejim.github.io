#!/usr/bin/env bash
set -e # halt script on error

# gem install
gem install mercenary -v 0.3.6


echo 'Testing travis...'
bundle exec jekyll build
bundle exec htmlproofer ./_site --only-4xx --file-ignore /_site/drafts/ /_site/slides/ /_site/projects/appiot/ --empty-alt_ignore --external_only


#gem update --system

# gem install mercenary -v 0.3.6
# gem install jekyll html-proofer
# gem install jekyll -v 2.5

# bundle install
# bundle update pygments.rb
# bundle exec jekyll build
