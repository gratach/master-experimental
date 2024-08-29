#!/usr/bin/env python3

import requests
from os import environ
from sys import argv
from pathlib import Path
from json import loads, dumps

# Get the paper ID from the command line
paper_id = argv[1]

res = requests.get(f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}?fields=title,abstract,openAccessPdf", headers={"x-api-key": environ["SEMSCHOLAR_KEY"]})
print(dumps(res.json(), indent=2))