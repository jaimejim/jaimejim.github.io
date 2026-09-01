#!/usr/bin/env ruby

require "html-proofer"

SITE_DIR = "./_site".freeze

# Absolute jaime.win links live all over the posts (e.g. {{ site.url }}/tags/...).
# Swap the host away so html-proofer treats them as internal and actually
# resolves them against the built _site instead of skipping them as external.
SWAP_URLS = { %r{^https?://(www\.)?jaime\.win} => "" }.freeze

# External endpoints that 403 / rate-limit / are not meant to be crawled.
IGNORE_URLS = [
  %r{^https?://ietf\.jaime\.win},   # gated PDF host
  %r{^https?://cdn\.midjourney\.com}, # hotlink-protected CDN
].freeze

def build!
  sh "bundle exec jekyll build"
end

namespace :proof do
  desc "Check internal links, images and asset paths (fast, deterministic; CI gate)"
  task :internal do
    HTMLProofer.check_directory(SITE_DIR,
      disable_external: true,
      allow_missing_href: true,
      allow_hash_href: true,
      enforce_https: false, # old external http:// links are not internal-link failures
      swap_urls: SWAP_URLS).run
  end

  desc "Check external links (flaky/rate-limited; run on demand, not in CI)"
  task :external do
    HTMLProofer.check_directory(SITE_DIR,
      ignore_urls: IGNORE_URLS,
      swap_urls: SWAP_URLS,
      only_4xx: true,
      enforce_https: false).run
  end
end

desc "Build the site, then run the internal link check"
task :proof do
  build!
  Rake::Task["proof:internal"].invoke
end

task default: :proof
