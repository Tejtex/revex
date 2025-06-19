# Revex — Reverse Regex String Generator & Parser Library

[![Contributions Welcome](https://img.shields.io/badge/Contributions-welcome-brightgreen.svg?style=flat)](https://github.com/tejtex/revex/issues)
[![Discord](https://img.shields.io/discord/000000000000000000?label=Discord&logo=discord&color=7289da)](https://discord.gg/yWaxzJenSW)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/twoje/repo/main.svg)](https://results.pre-commit.ci/latest/github/tejtex/revex/main)

**Revex** is a powerful Python library designed to parse simplified regex patterns and **generate random strings that match these patterns** — basically, the reverse of traditional regex matching.

## Overview
Regular expressions (regex) are widely used for pattern matching and validation. Revex flips this concept by taking a regex pattern as input and producing random strings that conform to it. This is useful for:

- Testing applications with randomized valid inputs

- Fuzz testing and automated input generation

- Educational purposes to understand regex behavior by example

## Usage
```python
from revex.parser import Parser

pattern = "(a|b)+c*"
parser = Parser()
generator = parser.parse(pattern)

# Generate a random string matching the regex
random_string = generator.generate({"max_repeats": 5})
print(random_string)  # e.g., "abaccc"
```

## Contributions
Contributions are highly welcomed! If you want to improve Revex, please:

- Fork the repository and create your feature branch

- Ensure your code follows the existing style and conventions

- Write tests covering your changes

- Open a pull request with a detailed description of your changes

- Feel free to submit issues for bugs, feature requests, or general feedback.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For questions or support, reach out via GitHub at `tejtex`.