""" Massachusetts Institute of Technology

Izzybrand, 2020

I wrote some typestrings for my higher order primitives, which means
at some point we'll need a typestring parser in order to make sure we can
typecheck programs using these primitives
"""

class FuncType:
    def __init__(self, input_type, output_type):
        self.input_type = input_type
        self.output_type = output_type

    def __str__(self):
        return f'({str(self.input_type)} -> {str(self.output_type)})'


class Type:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class TupleType:
    def __init__(self, L):
        self.items = L

    def __str__(self):
        return '(' + ', '.join(str(i) for i in self.items) + ')'


class ListType:
    def __init__(self, element_type):
        self.element_type = element_type

    def __str__(self):
        return f'List<{str(self.element_type)}>'


def tokenize(type_string):
    # pad symbols with spaces
    type_string = type_string.replace('(', ' ( ').replace(')', ' ) ')
    type_string = type_string.replace('->', ' -> ').replace(',', ' , ')
    # and then split the string at the spaces
    return type_string.split()

def parse_tokens(tokens, in_tuple_or_func=False):
    if in_tuple_or_func: L = []
    while tokens:
        token = tokens.pop(0)

        if token == '->':
            assert in_tuple_or_func, 'Unexpected operator without enclosing parens'
            prev_item = L.pop(-1)
            next_item = parse_tokens(tokens, in_tuple_or_func=False)
            item = FuncType(prev_item, next_item)
            assert tokens.pop(0) == ')', 'Expect a closing paren after function type'
            in_tuple_or_func = False
        elif token == '(':
            item = parse_tokens(tokens, in_tuple_or_func=True)
        elif token == ')':
            assert in_tuple_or_func, 'Unexpected closing paren'
            return TupleType(L)
        elif token == ',':
            assert in_tuple_or_func, 'Unexpected comma without enclosing parens' 
            continue
        elif token.startswith('List'):
            # TODO(izzy): At this point I'm making the naive assumtion that the
            # list type only contains a base-level type (ie we don't have a list
            # of typle types). To handle more complicated list types i'd need to
            # call parse tokens recursively at this point. The reason I don't do that
            # is because then I need to split the tokens again at "<" and ">" and look
            # for the closing ">" token. I'll get around to that at some point...
            element_token = token[5:-1]
            element_type = Type(element_token)
            item = ListType(element_type)

        else:
            item = Type(token)

        if in_tuple_or_func:
            L.append(item)
        if not in_tuple_or_func:
            return item

def parse(type_string):
    tokens = tokenize(type_string)
    return parse_tokens(tokens)


if __name__ == '__main__':
    # try out the type parse on some higher order types
    from map_filter_reduce import Map, Filter, Reduce
    for primitive in [Map, Filter, Reduce]:
        T = parse(primitive.type_string)
        print('Reference:\t', primitive.type_string)
        print('Post Parse:\t', T)
