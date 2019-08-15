#!/usr/bin/python3

# What Separated Value

# Read input from stdin and try to identify which character
# is used to delimiter fields, such as ',' in a CSV
# Only works with a perfect text delimited data set

import fileinput

## Configuration
# Delimiters to look for
delims = ["!", ";", ",", "\t", " ", "~", "|"]
# Minimum number of sample lines needed
min_lines = 3
# Maximum number of lines sampled
max_lines = 8

num_delims = len(delims)
line_delims = []
found_delims = [False] * num_delims

line_count = 0
with fileinput.input() as lines:
    for line in lines:
        d = 0
        delim_count = [0] * num_delims
        for delim in delims:
            delim_count[d] = line.count(delim)
            d += 1
        line_delims.append(delim_count)
        line_count += 1
        if line_count == max_lines:
            break

    if line_count < min_lines:
        print("Not enough lines - need minimum of", min_lines)
        exit(1)
    #DEBUG: print the 'table'
    # for item in line_delims:
    #     print(item)

    for D in range(0, num_delims):
        first = line_delims[0][D]
        found_delims[D] = False
        if first != 0:
            for L in range(1, line_count):
                if line_delims[L][D] == first:
                    found_delims[D] = True
                    first = line_delims[L][D]
                else:
                    found_delims[D] = False
                    break

    candidates = found_delims.count(True)
    if candidates > 1:
        print("Can't identify exact match, found", candidates, "candidates. Try increasing sample size")
        exit(candidates)
    
    if candidates < 1:
        print("Can't identify delimeter, found no candidates")
        exit(1)

    for index, delim in enumerate(found_delims):
        if delim:
            print(delims[index])
