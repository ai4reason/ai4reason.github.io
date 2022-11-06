#!/usr/bin/env python

import pandas as pd
import sys

HEADS = ["Authors", "Title", "Year", "Group", "Link", "Venue"]

read_file = pd.read_csv (sys.argv[1] + '.csv',sep="\t",header=None)
read_file.to_excel (sys.argv[1] + '.xlsx', index = None, header=HEADS)
