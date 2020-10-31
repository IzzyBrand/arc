class Type(list):
    def __init__(self, *args):
        super(Type, self).__init__(args)

    def __str__(self):
        if len(self) == 1:
            return str(self[0])
        else:
            return ', '.join(str(t) for t in self)

class FuncType(Type):
    def __str__(self):
        input_str = str(self[0])
        if len(self[0]) > 1: 
            input_str = f'({input_str})'

        output_str = str(self[1])
        if len(self[1]) > 1: 
            output_str = f'({output_str})'

        return f"{input_str} -> {output_str}"

if __name__ == '__main__':
    i_T = Type("Int")
    c_T = Type("Color")
    a_T = Type("Array")

    # example of a function that counts the number of pixels of
    # a certain color
    colorcount_T = FuncType(Type(a_T, c_T), Type(i_T))

    print(colorcount_T)
