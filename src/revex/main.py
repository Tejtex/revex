import re

import parser

print(parser.Parser().parse(input()).generate({"max_repeats": 30}))
