from revex.generators import (
    ClassGenerator,
    Generator,
    GroupGenerator,
    OrGenerator,
    RepeatGenerator,
    StringGenerator,
)
import string


class Parser:
    def parse(self, text: str = "") -> Generator:
        blocks: list[Generator] = []
        current_index: int = 0
        while current_index < len(text):
            char = text[current_index]

            if char == "+":
                blocks[-1] = RepeatGenerator(blocks[-1], min_repeats=1)
            elif char == "*":
                blocks[-1] = RepeatGenerator(blocks[-1], min_repeats=0)
            elif char == "?":
                blocks[-1] = RepeatGenerator(blocks[-1], min_repeats=0, max_repeats=1)
            elif char == ".":
                blocks.append(ClassGenerator(string.printable))
            elif char == "[":
                clas = self.parse_class(text, current_index)
                blocks.append(clas[0])
                current_index = clas[1]
            elif char == "\\":
                current_index += 1
                if current_index >= len(text):
                    raise ValueError("Invalid escape sequence in regex")
                next_char = text[current_index]
                blocks.append(StringGenerator(next_char))

            elif char == "|":
                # Handle OR operation
                left = GroupGenerator(blocks)
                blocks = []
                current_index += 1
                right = self.parse(text[current_index:])
                blocks.append(OrGenerator(left, right))
            elif char == "(":
                start_index = current_index + 1
                level = 0
                current_index += 1
                while current_index < len(text):
                    if text[current_index] == "(":
                        level += 1
                    elif text[current_index] == ")":
                        if level == 0:
                            break
                        level -= 1
                    current_index += 1
                if current_index >= len(text):
                    raise ValueError("Unclosed group in regex")
                block = self.parse(text[start_index:current_index])
                blocks.append(block)

            elif char == "{":
                current_index += 1
                number_str = ""
                min_repeats = None
                max_repeats = None

                while current_index < len(text) and text[current_index].isdigit():
                    number_str += text[current_index]
                    current_index += 1
                if number_str == "":
                    raise ValueError("Expected number after '{'")
                min_repeats = int(number_str)
                number_str = ""

                if current_index < len(text) and text[current_index] == ",":
                    current_index += 1
                    while current_index < len(text) and text[current_index].isdigit():
                        number_str += text[current_index]
                        current_index += 1
                    if number_str != "":
                        max_repeats = int(number_str)
                    else:
                        max_repeats = None
                else:
                    max_repeats = min_repeats

                if current_index >= len(text) or text[current_index] != "}":
                    raise ValueError("Unclosed repeat bracket '}'")
                current_index += 1

                blocks[-1] = RepeatGenerator(
                    blocks[-1], min_repeats=min_repeats, max_repeats=max_repeats
                )

                continue

            else:
                atom = char
                current_index += 1
                while (
                    current_index < len(text)
                    and text[current_index]
                    in string.ascii_letters + string.digits + "_"
                ):
                    atom += text[current_index]
                    current_index += 1
                blocks.append(StringGenerator(atom))
                continue
            current_index += 1
        return GroupGenerator(blocks) if blocks else StringGenerator("")

    def parse_class(self, text: str, start_index: int) -> tuple[ClassGenerator, int]:
        def is_valid_range(start_char, end_char):
            if start_char.isupper() and end_char.isupper():
                return True
            if start_char.islower() and end_char.islower():
                return True
            if start_char.isdigit() and end_char.isdigit():
                return True
            return False

        end_index = start_index + 1
        while end_index < len(text) and text[end_index] != "]":
            end_index += 1
        if end_index >= len(text):
            raise ValueError("Unclosed character class in regex")
        raw = text[start_index + 1 : end_index]

        characters = []
        i = 0
        while i < len(raw):
            if i + 2 < len(raw) and raw[i + 1] == "-":
                start_char = raw[i]
                end_char = raw[i + 2]
                if is_valid_range(start_char, end_char) and ord(start_char) <= ord(
                    end_char
                ):
                    characters.extend(
                        [chr(c) for c in range(ord(start_char), ord(end_char) + 1)]
                    )
                    i += 3
                    continue
                else:
                    characters.append(start_char)
                    i += 1
            else:
                characters.append(raw[i])
                i += 1

        characters = "".join(set(characters))  # Remove duplicates

        return ClassGenerator(characters), end_index
