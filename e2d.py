#!/usr/bin/python3

import sys, select, re
from datetime import datetime
epoch_regex = "(?:\b|\D)([0-9]{10})(?:\b|\D)"
rawdata = ""
if select.select([sys.stdin,],[],[],0.0)[0]:
    for line in sys.stdin:
        pattern = re.compile(epoch_regex)
        pattern_match = pattern.findall(line)
        if len(pattern_match) > 0:
            for epochstr in pattern_match:
                datetime = datetime.fromtimestamp(float(epochstr))
                line = line.replace(epochstr, str(datetime))
            print(line, end = '')
        else:
            print(line, end = '')
else:
    print("No input")
    exit(1)
