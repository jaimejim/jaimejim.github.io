[![pages-build-deployment](https://github.com/jaimejim/jaimejim.github.io/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/jaimejim/jaimejim.github.io/actions/workflows/pages/pages-build-deployment)

This is my personal website, you can visit it at [jaime.win](http://jaime.win)

Test locally:

- run `multipass` and mount ubuntu.
  - You must have jekyll and ruby-dev there.
- run `bundle install`
- run `bundle exec jekyll serve`
- open on browser on http://localhost:4000
- Do you want an admin panel to edit your posts? You can install this plugin `jekyll-admin`.

## Quality checks

Link checking (uses `html-proofer`, already in the Gemfile):

- `bundle exec rake proof` builds the site then checks internal links, images and asset paths.
- `bundle exec rake proof:internal` runs the internal check against an existing `_site` (this is the CI gate).
- `bundle exec rake proof:external` checks external links. Run on demand; it is flaky and rate-limited, so it is not run in CI.

Performance and accessibility (Lighthouse CI):

- `npm install` once to get `@lhci/cli`.
- `bundle exec jekyll build`, then `bundle exec jekyll serve --detach --port 4000 --skip-initial-build`, then `npx lhci autorun`.
- Budgets live in `lighthouserc.json`; URLs checked are the home, blog index, a recent post, the about and tags pages.

Both checks also run automatically on push and pull requests via `.github/workflows/ci.yml`.
