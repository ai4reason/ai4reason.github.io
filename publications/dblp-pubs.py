#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
from urllib.request import urlopen
import yaml

RIS = re.compile(r"^([A-Z][A-Z0-9])  - (.*)$")

def parse_ris(ris, year):
   db = {}
   entry = {}
   for line in ris.split("\n"):
      mo = RIS.match(line)
      if not mo:
         if entry:
            if (not year) or int(entry["PY"].rstrip("/")) == year:
               db[entry["ID"]] = entry
               #print("FOUND "+entry["ID"])
            entry = {}
         continue
      if mo.group(1) == "AU" or mo.group(1) == "ED":
         if "AU" not in entry:
            entry["AU"] = []
         entry["AU"].append(mo.group(2))
      else:
         entry[mo.group(1)] = mo.group(2)
   return db
      
def normalize_entry(entry, groups):
   authors = entry["AU"]
   authors = [" ".join(reversed(author.split(", "))) for author in authors]

   title = entry["TI"]
   year = entry["PY"].rstrip("/")

   if ("Informal" in entry["TY"]) and ("Publication" in entry["TY"]):
      if "JO" in entry and entry["JO"] == "CoRR":
         journal = "arXiv %s %s (%s)." % (entry["JO"], entry["VL"], entry["PY"].rstrip("/"))
      else:
         lib = entry["JO"] if "JO" in entry else entry["BT"] if "BT" in entry else "UNKNOWN"
         journal = "informal %s (%s)." % (lib, entry["PY"].rstrip("/"))
   elif entry["TY"] == "CPAPER":
      if "SP" in entry and "EP" in entry:
         journal = "%s: %s-%s (%s)." % (entry["BT"], entry["SP"], entry["EP"], entry["PY"].rstrip("/"))
      else:
         journal = "%s: (%s)." % (entry["BT"], entry["PY"].rstrip("/"))
   elif entry["TY"] == "JOUR":
      if "SP" in entry and "EP" in entry:
         journal = "%s %s: %s-%s (%s)." % (entry["JO"], entry["VL"], entry["SP"], entry["EP"], entry["PY"].rstrip("/"))
      else:
         journal = "%s %s: (%s)." % (entry["JO"], entry["VL"], entry["PY"].rstrip("/"))
   elif entry["TY"] == "CONF":
      journal = "%s %s (%s)." % (entry["T3"], entry["VL"], entry["PY"].rstrip("/"))
   elif entry["TY"] == "CHAP":
      journal = "%s: %s-%s (%s)." % (entry["BT"], entry["SP"], entry["EP"], entry["PY"].rstrip("/"))
   elif entry["TY"] == "THES":
      journal = "Thesis (%s)." % year
   elif entry["TY"] == "BOOK":
      journal = "%s, %s (%s)." % (entry["T3"], entry["PB"], year)
   elif entry["TY"] == "EDBOOK":
      journal = "%s, %s (%s)." % (entry["T3"], entry["PB"], year)
   elif entry["TY"] == "DATA":
      journal = "%s (%s)" % (entry["JO"], year)
   elif entry["TY"] == "ENCYC":
      journal = "%s (%s)" % (entry["BT"], year)
   else:
      journal = "YAN TODO: %s" % entry["TY"]
      journal += str(entry)

   url = entry["UR"] if "UR" in entry else ""
   if "arxiv" in url:
      urltype = "arXiv"
   elif "doi" in url:
      urltype = "doi"
   elif "easychair" in url:
      urltype = "easychair"
   else:
      urltype = "url"

   record = entry["ID"].split(":")[1]
   return dict(authors=authors, title=title, source=journal, year=int(year),
               url=(urltype, url), dblp=record, groups=set(groups), link=url)

def normalize_entries(db, groups):
   for eid in db.keys():
      db[eid] = normalize_entry(db[eid], groups)

def update_db(db, new):
   for eid in new:
      if eid in db:
         db[eid]["groups"].update(new[eid]["groups"])
      else:
         db[eid] = new[eid]

def finalize_db(db):
   for entry in db.values():
      entry["groups"] = sorted(entry["groups"])
      entry["authors"] = ", ".join(entry["authors"])
      (typ, link) = entry["url"]
      del entry["url"]
      if link:
         entry[typ] = link
   #return list(db.values())
   return db

def download_db(authors, year):
   db = {}
   for author in authors:
   #for author in sorted(authors)[:3]:
      sys.stderr.write("Donwloading %s\n" % author)
      url = "https://dblp.uni-trier.de/%s.ris" % authors[author]["dblp"]
      data = urlopen(url)
      ris = data.read().decode("utf-8")
      authordb = parse_ris(ris, year)
      groups = authors[author]["groups"] if "groups" in authors[author] else []
      groups = set(groups)
      groups.add("main")
      normalize_entries(authordb, groups)
      update_db(db, authordb)
   db = finalize_db(db)
   sys.stderr.write("Relevant entries found: %d\n" % len(db))
   return db

def read_authors(ids_file):
   items = yaml.safe_load(open(ids_file))
   authors = {it["name"]: it for it in items if "name" in it and "dblp" in it and it["dblp"]}
   return authors

def csv_dump(db, out):
   for (ref, entry) in db.items():
      if "main" in entry["groups"]:
         entry["groups"].remove("main")
      entry["groups"] = ", ".join(entry["groups"])
      out.write("%(authors)s \t %(title)s \t %(year)s \t %(groups)s \t %(link)s \t %(source)s\n" % entry)

def bibliography(ids_file, year, out_yaml, out_csv):
   authors = read_authors(ids_file)
   db = download_db(authors, year)
   if out_yaml:
      with open(out_yaml, "w") as out: yaml.dump(db, out)
   if out_csv:
      with open(out_csv, "w") as out: csv_dump(db, out)

if __name__ == "__main__":
   import argparse

   parser = argparse.ArgumentParser(
      description='Automatically update publication list from DBLP.')
   parser.add_argument('ids_file', type=str,
      help="YAML file with DBLP ids for each author")
   parser.add_argument("-y", "--year", metavar="YEAR", type=int, nargs=1,
      help="Consider only a specific year.")
   parser.add_argument("--csv", 
      help="output CSV file")
   parser.add_argument("--yaml", 
      help="output YAML file")
   args = parser.parse_args()

   bibliography(args.ids_file, args.year, args.yaml, args.csv)

