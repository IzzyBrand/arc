""" Massachusetts Institute of Technology

Izzy Brand, 2021

Based on an implementation by Robert Smallshire
https://github.com/rob-smallshire/hindley-milner-python
"""

class Identifier(object):
    """Identifier"""

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Apply(object):
    """Function application"""

    def __init__(self, fn, *args):
        self.fn = fn
        self.args = args

    def __str__(self):
        return f"({self.fn} {' '.join([str(a) for a in self.args])})"


class Lambda(object):
    """Lambda abstraction"""

    def __init__(self, v, body):
        self.v = v  # variable name(s) can be either str, or list of str
        self.body = body

    def __str__(self):
        if isinstance(self.v, str):
            return f"(fn {self.v} => {self.body})"
        else:
            return f"(fn {', '.join(str(i) for i in self.v)} => {self.body})"


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
