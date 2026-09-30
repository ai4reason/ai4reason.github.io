#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
import json
from urllib.request import Request, urlopen
from urllib.parse import urlencode
import yaml

SPARQL_ENDPOINT = "https://sparql.dblp.org/sparql"
DBLP_PREFIX = "https://dblp.org/"
DBLP = "https://dblp.org/rdf/schema#"
BIBTEX = "http://purl.org/net/nknouf/ns/bibtex#"
BATCH_SIZE = 50
TIMEOUT = 300

# One row per (publication, field value); multi-valued fields repeat rows.
QUERY_PUBS = """
PREFIX dblp: <https://dblp.org/rdf/schema#>
SELECT DISTINCT ?pub ?type ?bibtex ?title ?version ?year ?event ?month ?venue
       ?journal ?volume ?book ?parent ?series ?seriesvol ?publisher ?pagination
       ?doi ?primary ?page
WHERE {
  VALUES ?author { %s }
  ?pub dblp:createdBy ?author ;
       dblp:title ?title ;
       a ?type .
  FILTER(?type != dblp:Publication)
  OPTIONAL { ?pub dblp:bibtexType ?bibtex }
  OPTIONAL { ?pub dblp:isVersion/dblp:versionLabel ?version }
  OPTIONAL { ?pub dblp:yearOfPublication ?year }
  OPTIONAL { ?pub dblp:yearOfEvent ?event }
  OPTIONAL { ?pub dblp:monthOfPublication ?month }
  OPTIONAL { ?pub dblp:publishedIn ?venue }
  OPTIONAL { ?pub dblp:publishedInJournal ?journal }
  OPTIONAL { ?pub dblp:publishedInJournalVolume ?volume }
  OPTIONAL { ?pub dblp:publishedInBook ?book }
  OPTIONAL { ?pub dblp:publishedAsPartOf/dblp:title ?parent }
  OPTIONAL { ?pub dblp:publishedInSeries ?series }
  OPTIONAL { ?pub dblp:publishedInSeriesVolume ?seriesvol }
  OPTIONAL { ?pub dblp:publishedBy ?publisher }
  OPTIONAL { ?pub dblp:pagination ?pagination }
  OPTIONAL { ?pub dblp:doi ?doi }
  OPTIONAL { ?pub dblp:primaryDocumentPage ?primary }
  OPTIONAL { ?pub dblp:documentPage ?page }
}
"""

# Authors (or editors) of each publication, in order, with their dblp pids.
QUERY_SIGS = """
PREFIX dblp: <https://dblp.org/rdf/schema#>
SELECT DISTINCT ?pub ?ord ?name ?creator WHERE {
  VALUES ?author { %s }
  ?pub dblp:createdBy ?author ;
       dblp:hasSignature ?sig .
  ?sig dblp:signatureOrdinal ?ord ;
       dblp:signatureDblpName ?name ;
       dblp:signatureCreator ?creator .
}
"""

def sparql(query):
   data = urlencode({"query": query}).encode("utf-8")
   req = Request(SPARQL_ENDPOINT, data=data, headers={
      "Accept": "application/sparql-results+json",
      "User-Agent": "ai4reason.github.io publication updater"})
   with urlopen(req, timeout=TIMEOUT) as resp:
      res = json.load(resp)
   return [{k: v["value"] for (k, v) in row.items()} for row in res["results"]["bindings"]]

def clean_name(name):
   "Drop dblp's homonym suffix, e.g. 'Wei Wang 0001' -> 'Wei Wang'."
   return re.sub(r"\s\d{4}$", "", name)

def download_pubs(pids):
   pubs = {}
   for i in range(0, len(pids), BATCH_SIZE):
      values = " ".join(f"<{DBLP_PREFIX}{pid.strip('/')}>" for pid in pids[i:i+BATCH_SIZE])
      rows = sparql(QUERY_PUBS % values)
      sys.stderr.write("Downloaded %d publication rows\n" % len(rows))
      for row in rows:
         pub = pubs.setdefault(row["pub"], dict(types=set(), pages=[], sigs={}))
         pub["types"].add(row.pop("type").removeprefix(DBLP))
         if "page" in row:
            page = row.pop("page")
            if page not in pub["pages"]:
               pub["pages"].append(page)
         for (key, val) in row.items():
            pub.setdefault(key, val)
      rows = sparql(QUERY_SIGS % values)
      sys.stderr.write("Downloaded %d author rows\n" % len(rows))
      for row in rows:
         creator = row["creator"].removeprefix(DBLP_PREFIX)
         pubs[row["pub"]]["sigs"][int(row["ord"])] = (clean_name(row["name"]), creator)
   return pubs

def page_range(pub):
   "Only page ranges are shown (single article numbers are not)."
   pages = pub.get("pagination", "")
   return pages + " " if "-" in pages else ""

def format_source(pub, year, date):
   types = pub["types"]
   bibtex = pub.get("bibtex", "").removeprefix(BIBTEX)
   journal = pub.get("journal", "")
   volume = pub.get("volume", "")
   book = pub.get("parent", pub.get("book", pub.get("venue", "")))
   series = pub.get("series", "")
   seriesvol = pub.get("seriesvol", "")
   publisher = pub.get("publisher", "")
   pages = page_range(pub)

   if "Informal" in types:
      if journal == "CoRR":
         return "arXiv CoRR %s (%s)." % (volume, date)
      return "informal %s (%s)." % (journal or book or "UNKNOWN", date)
   if "Article" in types:
      return "%s: %s(%s)." % (" ".join(filter(None, [journal, volume])), pages, date)
   if "Inproceedings" in types or "Incollection" in types:
      return "%s: %s(%s)." % (book, pages, date)
   if "Reference" in types:
      return "%s (%s)" % (book, date)
   if "Editorship" in types and bibtex == "Proceedings":
      if series:
         return "%s %s (%s)." % (series, seriesvol, date)
      return "%s (%s)." % (pub["title"], date)
   if bibtex in ("Phdthesis", "Mastersthesis"):
      return "Thesis (%s)." % year
   if "Book" in types or "Editorship" in types:
      return "%s (%s)." % (", ".join(filter(None, [series, publisher])), year)
   if "Data" in types:
      return "%s (%s)" % (journal or pub.get("venue") or publisher, date)
   return "%s (%s)." % (pub.get("venue") or book or publisher, date)

def primary_link(pub):
   if "primary" in pub:
      return pub["primary"]
   if "doi" in pub:
      return pub["doi"]
   return pub["pages"][0] if pub["pages"] else ""

def link_type(url):
   if "arxiv" in url:
      return "arXiv"
   elif "doi" in url:
      return "doi"
   elif "easychair" in url:
      return "easychair"
   else:
      return "url"

def is_active(authorinfo, year):
   active = authorinfo.get("active") or {}
   if ("from" in active) and (year < active["from"]):
      return False
   if ("to" in active) and (year > active["to"]):
      return False
   return True

def build_db(pubs, members, year):
   db = {}
   for (iri, pub) in pubs.items():
      # event year for conference papers (as in dblp listings), otherwise publication year
      if "event" not in pub and "year" not in pub:
         continue
      pubyear = int(pub.get("event", pub.get("year")))
      # publication month is shown only with the publication year
      month = pub.get("month", "").removeprefix("--") if "event" not in pub else ""
      date = "%d/%s" % (pubyear, month) if month else str(pubyear)
      if year and pubyear != year:
         continue
      sigs = [pub["sigs"][k] for k in sorted(pub["sigs"])]
      # union of groups of all department members active in the publication year
      groups = set()
      for (_, pid) in sigs:
         if pid in members and is_active(members[pid], pubyear):
            groups.update(members[pid].get("groups") or [])
            groups.add("main")
      if not groups:
         continue
      record = iri.removeprefix(DBLP_PREFIX + "rec/")
      link = primary_link(pub)
      entry = dict(
         authors=", ".join(name for (name, _) in sigs),
         title=pub["title"] + (" (%s)" % pub["version"] if "version" in pub else ""),
         source=format_source(pub, pubyear, date),
         year=pubyear,
         dblp=record,
         groups=sorted(groups),
         link=link)
      if link:
         entry[link_type(link)] = link
      db["DBLP:" + record] = entry
   sys.stderr.write("Relevant entries found: %d\n" % len(db))
   return db

def read_members(ids_file):
   items = yaml.safe_load(open(ids_file))
   return {it["dblp"].strip("/"): it for it in items if it.get("name") and it.get("dblp")}

def csv_dump(db, out):
   entries = sorted(db.values(), key=lambda e: (-e["year"], e["dblp"]))
   for entry in entries:
      groups = ", ".join(g for g in entry["groups"] if g != "main")
      out.write("%s \t %s \t %s \t %s \t %s \t %s\n" % (entry["authors"],
         entry["title"], entry["year"], groups, entry["link"], entry["source"]))

def bibliography(ids_file, year, out_yaml, out_csv):
   members = read_members(ids_file)
   pubs = download_pubs(sorted(members))
   db = build_db(pubs, members, year)
   if not db:
      sys.exit("ERROR: No publications found; refusing to write empty output.")
   if out_yaml:
      with open(out_yaml, "w") as out: yaml.dump(db, out)
   if out_csv:
      with open(out_csv, "w") as out: csv_dump(db, out)

if __name__ == "__main__":
   import argparse

   parser = argparse.ArgumentParser(
      description='Automatically update publication list from DBLP (SPARQL).')
   parser.add_argument('ids_file', type=str,
      help="YAML file with DBLP ids for each author")
   parser.add_argument("-y", "--year", metavar="YEAR", type=int,
      help="Consider only a specific year.")
   parser.add_argument("--csv",
      help="output CSV file")
   parser.add_argument("--yaml",
      help="output YAML file")
   args = parser.parse_args()

   bibliography(args.ids_file, args.year, args.yaml, args.csv)
