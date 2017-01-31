#!/usr/bin/env python3.5

import json
import random
import sys

# create randomized results for testing and as a demo

with open('./orig.json', 'r') as fh:
    data = json.load(fh)

languages = ['English', 'Korean', 'German', 'Spanish', 'Italian', 'Russian', 'Mandarin', 'Polish', 'Swaheli']
pids = range(0, 475982743857398457)

for i in data:
    # print(i)
    for r in i['results']:
        r['sent_rt'] = random.randint(4000, 12000)
        r['value'] = random.randint(0,5)
    i['demographics']['languages'] = random.sample(languages + ['none'], random.randint(0,4))
    i['demographics']['native'] = random.sample(languages + [''], 1)
    i['demographics']['gender'] = random.sample(['male', 'female', ''], 1)
    i['demographics']['age'] = random.sample(['18-29', '30-39', '40-49', '50-59', '> 60'], 1)
    i['pid'] = random.sample(pids, 1)[0]

with open('./db-owls.json', 'w') as fh:
    json.dump(data, fh)

