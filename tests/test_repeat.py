from revex.parser import Parser
from revex.generators import StringGenerator, GroupGenerator, OrGenerator, RepeatGenerator
import pytest
import re

def test_repeat_generator():
    gen = RepeatGenerator(StringGenerator("a"), min_repeats=1, max_repeats=3)
    assert gen.generate({}) in ["a", "aa", "aaa"]

def test_repeat_parser():
    parser = Parser()
    tests = ['a+', 'aa+', 'b*a+', 'c?a*']

    for test in tests:
        gen = parser.parse(test)
        assert  re.match(f'^{test}$', gen.generate({'max_repeats': 3}))