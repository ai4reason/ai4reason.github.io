#!/usr/bin/env python3
# -*- coding: utf-8 -*-


if __name__ == "__main__":
   import argparse

   parser = argparse.ArgumentParser(
      description='Automatically update publication list from DBLP.')
   parser.add_argument("-y", "--year", metavar="YEAR", type=int, nargs=1,
      help="Consider only a specific year.")
   group = parser.add_mutually_exclusive_group(required=True)
   group.add_argument("--html", action="store_true",
      help="output HTML format")
   group.add_argument("--csv", action="store_true",
      help="output CSV format")
   group.add_argument("--yaml", action="store_true",
      help="output YAML format")
   args = parser.parse_args()

   print("year", args.year)

