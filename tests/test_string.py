from revex.parser import Parser
from revex.generators import (
    StringGenerator,
    GroupGenerator,
    OrGenerator,
    RepeatGenerator,
)
import pytest


def test_string_generator():
    gen = StringGenerator("hello")
    assert gen.generate({}) == "hello"


def test_string_parser():
    parser = Parser()
    gen = parser.parse("hello")
    assert isinstance(gen, StringGenerator)
    assert gen.generate({}) == "hello"
