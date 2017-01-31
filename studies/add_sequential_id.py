#!/usr/bin/env python3.5

import sys
import json

try:
    input_file = sys.argv[1]
except IndexError:
    sys.exit("Please provide a filename")

with open(input_file, 'r') as fh:
    data = json.load(fh)

result = []
for i,d in enumerate(data):
    d['id'] = i
    result.append(d)

output_file = input_file.split('.json')[0] + "-id.json"
with open(output_file, 'w') as fh:
    json.dump(result, fh, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)

