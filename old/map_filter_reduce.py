
class Primitive:
    name = 'Primitive'
    type_string = '(<T> -> <T>)'

    @staticmethod
    def eval(x):
        return x


class Map(Primitive):
    name = 'Map'
    type_string = '((List<T1>, (<T1> -> <T2>)) -> List<T1>)'

    @staticmethod
    def eval(l, f):
        return [f(i) for i in l]


class Filter(Primitive):
    name = 'Filter'
    type_string = '((List<T>, (<T> -> Bool)) -> List<T>)'

    @staticmethod
    def eval(l, f):
        return [i for i in l if f(i)]


class Reduce(Primitive):
    name = 'Reduce'
    type_string = '((List<T1>, ((<T1>, <T2>) -> <T2>)) -> <T2>)'

    @staticmethod
    def eval(l, f, s):
        for i in l:
            s = f(i, s)

        return s
