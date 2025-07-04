from revex.parser import Parser
from revex.generators import (
    StringGenerator,
    GroupGenerator,
    OrGenerator,
    RepeatGenerator,
)
import pytest
import re


def test_parser():
    parser = Parser()
    tests = ["(a|b)*c+", "a|(b(c|a)?)", "(a+b*c?d|e)+", "x?y*z+", "a(b|c)*d+"]

    for test in tests:
        for i in range(100):
            gen = parser.parse(test)
            assert re.match(f"^{test}$", gen.generate({"max_repeats": 3}))
