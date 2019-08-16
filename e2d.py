#!/usr/bin/python3

import fileinput, re
from datetime import datetime

epoch_regex = "(?:\b|\D)([0-9]{10})(?:\b|\D)"
with fileinput.input('-') as lines:
    for line in lines:
        pattern = re.compile(epoch_regex)
        pattern_match = pattern.findall(line)
        if len(pattern_match) > 0:
            for epochstr in pattern_match:
                datetime = datetime.fromtimestamp(float(epochstr))
                line = line.replace(epochstr, str(datetime))
            print(line, end = '')
        else:
            print(line, end = '')
