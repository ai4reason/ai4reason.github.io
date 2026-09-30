# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Public web pages of the Department of Artificial Intelligence at CIIRC/CTU,
served by GitHub Pages at https://ai4reason.github.io/. The repo is public
and shared with co-workers.

## Layout

- `docs/` — the Jekyll site (the Pages source root). Remote theme
  `pages-themes/leap-day`. Groups (`AR`, `FAI`, `FM`, `ML`) each have a
  layout in `docs/_layouts/` and pages in `docs/groups/<G>/`.
- `docs/_data/members.yml` — member database (hand-edited). Each member's
  `dblp` field (e.g. `pid/56/2424`), `groups`, and optional
  `active: {from: YEAR, to: YEAR}` drive the publication list.
- `docs/_data/bib.yml` — **generated** publication database; never edit by
  hand. `docs/_data/exclude.yml` — hand-maintained list of `DBLP:<key>`
  entries to hide.
- `docs/internal/` — admin docs for department members (`biblio.md`
  describes the publication pipeline for humans).
- `publications/` — Python scripts that build the publication data.

## Publication pipeline

`update-bib.sh` (run from repo root) does:

1. `publications/dblp-pubs.py --yaml docs/_data/bib.yml --csv docs/download/publications.csv docs/_data/members.yml`
2. If the CSV changed, `publications/to-excel.py docs/download/publications`
   regenerates `docs/download/publications.xlsx` (pandas + openpyxl).

`dblp-pubs.py` queries the DBLP SPARQL endpoint
(`https://sparql.dblp.org/sparql`, stdlib `urllib` only) for all
publications created (authored or edited) by the members' pids: one query
for record metadata, one for ordered author signatures. The dblp.org web
pages sit behind Anubis and can't be scraped, which is why the old RIS
download (`publications/dblp-pubs-v1.py`, kept for reference) was
replaced. A record's `groups` is the union of the groups of all its
member-authors who are `active` in its year, plus `main`; records with no
active member are dropped. `year` is the event year when dblp has one
(conference papers), else the publication year. `source` reproduces the
old RIS-based citation strings (full proceedings/book title of the parent
record, page ranges only, `year/month` where RIS had it). The script
exits non-zero rather than write empty output, and `update-bib.sh` then
restores the previous CSV and fails.

Output contracts that the rest of the site depends on:

- **`bib.yml`**: a mapping keyed by `DBLP:<record key>` (e.g.
  `DBLP:journals/ijar/JakubuvJPU26`) — the same key format used in
  `exclude.yml`. Each value has `authors` (comma-joined string), `title`,
  `year` (int), `source`, `dblp` (record key without prefix), `groups`
  (sorted list, including `main`), `link` (the primary URL or `''`), and
  one of `doi` / `arXiv` / `easychair` / `url` holding the same link
  (chosen by substring match on the URL). Consumed by
  `docs/_includes/biblio.html`, which filters by `year` and `groups` and
  builds dblp/bibtex links from `dblp`.
- **`publications.csv`**: tab-separated, no header, 6 columns, each value
  padded as `" \t "`:
  `authors \t title \t year \t groups \t link \t source`, where `groups`
  is comma-joined **without** `main`. Rows are sorted (year desc, then
  dblp key) so the output is deterministic — `update-bib.sh` only
  regenerates the XLSX when the CSV changes. `to-excel.py` adds the header
  `Authors, Title, Year, Group, Link, Venue`. Linked from
  `docs/activities.md`.

## Deployment (GitHub Actions)

- `.github/workflows/bib.yml` (`update-bibliography-database`): on push to
  `main`, daily at 00:00 UTC, and manually. Installs `pyyaml pandas
  openpyxl` on Python 3.13, runs `./update-bib.sh`, commits everything as
  "Auto update pubs" and force-pushes to `main`. A failing
  `update-bib.sh` fails the job, so nothing is committed.
- `.github/workflows/jekyll-gh-pages.yml`: runs after the bib workflow
  completes (or manually); builds `./docs/` with `actions/jekyll-build-pages`
  and deploys to Pages.

Because the bib workflow pushes to `main` after every push, pull before
committing locally.

## Local commands

```sh
./update-bib.sh                       # regenerate bib.yml, CSV, XLSX (from repo root)
cd docs && ./docker-serve.sh          # Jekyll preview at http://localhost:4000 (docker, jekyll/builder:3.8)
cd docs && ./docker-update.sh         # bundle update: refreshes docs/Gemfile.lock + docs/vendor/bundle
```

The Gemfile/Gemfile.lock only matter for local preview: the Pages build
(`actions/jekyll-build-pages`) uses its own pinned `github-pages` gem set.
Python deps for `update-bib.sh` are installed in the bib workflow's `pip3`
line, not managed by any file in the repo.

There are no tests or linters.
