class Identifier(object):
    """Identifier"""

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Apply(object):
    """Function application"""

    def __init__(self, fn, arg):
        self.fn = fn
        self.arg = arg

    def __str__(self):
        return f"({self.fn} {self.arg})"

class Lambda(object):
    """Lambda abstraction"""

    def __init__(self, v, body):
        self.v = v
        self.body = body

    def __str__(self):
        return f"(fn {self.v} => {self.body})"


class Let(object):
    """Let binding"""

    def __init__(self, v, defn, body):
        self.v = v
        self.defn = defn
        self.body = body

    def __str__(self):
        return f"(let {self.v} = {self.defn} in {self.body})"


class Letrec(object):
    """Letrec binding"""

    def __init__(self, v, defn, body):
        self.v = v
        self.defn = defn
        self.body = body

    def __str__(self):
        return f"(letrec {self.v} = {self.defn} in {self.body})"