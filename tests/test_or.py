from revex.parser import Parser
from revex.generators import StringGenerator, GroupGenerator, OrGenerator, RepeatGenerator
import pytest
import re

def test_or_generator():
    gen = OrGenerator(StringGenerator("a"), StringGenerator("b"))
    assert gen.generate({}) in ["a", "b"]

def test_or_parser():
    parser = Parser()
    tests = ['a|b', 'ab|c', 'a|b|c']

    for test in tests:
        for i in range(100):
            gen = parser.parse(test)
            assert re.match(f'^{test}$', gen.generate({'max_repeats': 3}))