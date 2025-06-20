import random


class Generator:
    def generate(self, config) -> str:
        raise NotImplementedError("Subclasses should implement this method")

    def repr_tree(self, indent=0) -> str:
        raise NotImplementedError()

    def __repr__(self):
        return self.repr_tree()


class OrGenerator(Generator):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def generate(self, config) -> str:
        if random.choice([True, False]):
            return self.left.generate(config)
        else:
            return self.right.generate(config)

    def repr_tree(self, indent=0):
        pad = " " * indent
        return (
            f"{pad}Or\n"
            f"{self.left.repr_tree(indent + 4)}\n"
            f"{self.right.repr_tree(indent + 4)}"
        )


class RepeatGenerator(Generator):
    def __init__(self, generator, min_repeats=0, max_repeats=None):
        self.generator = generator
        self.min_repeats = min_repeats
        self.max_repeats = max_repeats

    def generate(self, config) -> str:
        if self.max_repeats == None:
            self.max_repeats = config["max_repeats"]
        num_repeats = random.randint(self.min_repeats, self.max_repeats)
        return "".join(self.generator.generate(config) for _ in range(num_repeats))

    def repr_tree(self, indent=0):
        pad = " " * indent
        return (
            f"{pad}Repeat min={self.min_repeats} max={self.max_repeats}\n"
            f"{self.generator.repr_tree(indent + 4)}"
        )


class StringGenerator(Generator):
    def __init__(self, value: str):
        self.value = value

    def generate(self, config) -> str:
        return self.value

    def repr_tree(self, indent=0):
        pad = " " * indent
        return f"{pad}String('{self.value}')"


class GroupGenerator(Generator):
    def __init__(self, generators):
        self.generators = generators

    def generate(self, config) -> str:
        return "".join(map(lambda g: g.generate(config), self.generators))

    def repr_tree(self, indent=0):
        pad = " " * indent
        child_reprs = [g.repr_tree(indent + 4) for g in self.generators]
        return f"{pad}Group\n" + "\n".join(child_reprs)


class ClassGenerator(Generator):
    def __init__(self, characters: str):
        self.characters = characters

    def generate(self, config) -> str:
        return random.choice(self.characters)

    def repr_tree(self, indent=0):
        pad = " " * indent
        return f"{pad}Class[{self.characters}]"
