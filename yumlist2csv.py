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
    while line.count("  "):
        line=line.replace("  ", " ")
    vals=line.split(" ")
    if len(vals)==1: # found a split line, remember the package
        last_rpm=vals[0]
        continue
    if vals[0]=='': # found a continuation, use remembered package
        vals[0]=last_rpm
        last_rpm="Unknown" # Avoid re-using remembered package
    outline=""
    for val in vals:
        outline=outline+val + ","
        if outline.count("Unknown") > 0:
            broken=True
    if not broken:
        outline=outline[0:-1]
        print(outline)
    else:
        print("Unable to process input")
