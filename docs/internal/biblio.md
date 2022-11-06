---
layout: internal
button: ✏️  Publications
index: 40
---

# Bibliography list

The publication list is automatically downloaded from DBLP for all department members.
The database is periodically updated every day and with every repository update.

The list of all publications of all group members is rendered in the _Activities_ page for each group.
The [Activities](/activities.html) page of the whole department lists the publications by all department members.

⚠️  Publication information are downloaded from [DBLP](https://dblp.uni-trier.de/) using DBLP identificators from the member database.
The `dblp` fields must set correctly.  See [member updates](/internal/members.html) for more info.


## Adjusting the list

A publication not listed in DBLP can not be added manually. 
However, an existing publication can be excluded from the list, as follows.


1️⃣  Locate the publication record in the bibliography database 
[bib.yml](https://github.com/ai4reason/ai4reason.github.io/blob/main/docs/_data/bib.yml){:target="_blank"}
and find its DBLP key (the first line ending with `:`).

⚠️  Do not edit the file manually.  It is generated and any changes will be lost.

2️⃣  Insert a line with this key into the file
[exclude.yml](https://github.com/ai4reason/ai4reason.github.io/blob/main/docs/_data/exclude.yml){:target="_blank"}
as follows.

```
- DBLP:books/daglib/0068045
```

3️⃣  Commit the changes and create a pull request.

## Automation

The list of publications is downloaded from DBLP by the script
[dblp-pubs.py](https://github.com/ai4reason/ai4reason.github.io/blob/main/publications/dblp-pubs.py){:target="_blank"}
which reads the DBLP identificators of members from the 
members database [members.yml](https://github.com/ai4reason/ai4reason.github.io/blob/main/docs/_data/members.yml){:target="_blank"}.

At every push to the repository, but at least daily, the DBLP download is launched by script
[update-bib.sh](https://github.com/ai4reason/ai4reason.github.io/blob/main/update-bib.sh){:target="_blank"}.
This is due to the GitHub action 
[update-bibliography-database](https://github.com/ai4reason/ai4reason.github.io/blob/main/.github/workflows/bib.yml){:target="_blank"}.
This action triggers another GitHub action 
[jekyll-gh-pages](https://github.com/ai4reason/ai4reason.github.io/blob/main/.github/workflows/jekyll-gh-pages.yml){:target="_blank"}
which publishes the web pages.


## Continue ...

+ [Internal administration](/internal/index.html)
+ [Content update](/internal/content.html)
+ [Members update](/internal/members.html)


