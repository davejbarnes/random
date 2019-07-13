#!/usr/bin/python
import sys

# Takes input from "yum list ...." and converts the output
# to a CSV file.  Long package names span 2 lines in the
# output from yum which makes direct processing difficult.
#
# NOTE: only provide the "data lines" from the output
# (eg. grep the output for only package information)
#
# Compatible with Python 2 and Python 3

last_rpm="Unknown"
broken=False
for line in sys.stdin:
    line=line.replace("\n", "")
    while line.count("  "): # yum output is space aligned
        line=line.replace("  ", " ")  # reduce all that space to just one
    vals=line.split(" ")
    if len(vals)==1: # found a split line... 
        last_rpm=vals[0] # ...remember the package...
        continue # ... and move on to the next line which should be a continuation
    if vals[0]=='' and len(vals)==3: # found a continuation...
        vals[0]=last_rpm # ...use remembered package
        last_rpm="Unknown" # Avoid re-using remembered package
    outline="" # make sure our output is empty
    for val in vals:
        outline=outline+val + "," # make a line of the CSV
    if outline.count("Unknown") > 0: # has something gone wrong?
        broken=True
    if not broken:
        outline=outline[0:-1] # get rid of trailing ,
        print(outline)
    else:
        print("Unable to process input")
