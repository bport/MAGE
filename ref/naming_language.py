# coding: utf-8

from pyparsing import alphas, Group, nums, ZeroOrMore, Forward, QuotedString, \
    Word, Suppress, Optional, Combine

def build_grammar():
    expr = Forward()
    # Our identifier definition is Python's one with the added constraint of not allowing underscores as first character.
    identifier = Combine(Word(alphas, exact=1) + Optional(Word(nums + alphas + "_")))("identifier")
    navigation = Group(Suppress("%") + identifier + ZeroOrMore(Suppress(".") + identifier))("navigation")
    text = QuotedString('"', escQuote='""')("text")
    numeric = Word(nums)('num')
    operator = Word("?|+-/*", exact=1)("operator")

    datatoken = Group(navigation | text | numeric)('datatoken')

    # expr << Group(((datatoken | Suppress("(") + expr + Suppress(")")) + ZeroOrMore(Group(operator + (datatoken | Suppress("(") + expr + Suppress(")")))('operand'))('right_group')))("expr")
    expr << Group(((datatoken | Suppress("(") + expr + Suppress(")")) + ZeroOrMore(Group(operator + (datatoken | Suppress("(") + expr + Suppress(")")))('operand'))('right_group')))("expr")

    return expr

__grammar = build_grammar()  #.setDebug()

def resolve(pattern, instance):
    expression = parse(pattern)
    return __resolve_expr(expression.expr, instance)

def parse(pattern):
    """Parses the given pattern and throws an exception if it is wrong. Used to check patterns."""
    return __grammar.parseString(pattern)

def __resolve_datatoken(datatoken, instance):
    res = ""

    if datatoken.num:
        res = int(datatoken.num)
    elif datatoken.text:
        res = datatoken.text
    elif datatoken.navigation:
        res = __resolve_navigation(datatoken.navigation, instance)

    return res

def __resolve_expr(e, instance):
    if e.expr:
        left = __resolve_expr(e.expr)
    else:
        left = __resolve_datatoken(e.datatoken, instance)

    if not e.right_group:
        return left

    for group in e.right_group:
        operator = group.operator
        if group.expr:
            right = __resolve_expr(group.expr, instance)
        else:
            right = __resolve_datatoken(group.datatoken, instance)

        if operator == "|":
            left = "%s%s" % (left, right)
        elif operator == "?":
            if left :
                return left
            if right:
                return right
        elif operator == '+':
            left = int(left) + int(right)
        elif operator == '-':
            left = int(left) - int(right)
        elif operator == '*':
            left = int(left) * int(right)
        elif operator == '/':
            left = int(left) / int(right)

    return left


def __resolve_navigation(path, instance):
    ''' Will instanciate a pattern according to the value inside the given component instance'''
    res = instance
    for segment in path:
        try:
            # if a ComponentInstance, will be translated as its proxy. If already proxy, will fail silently.
            res = res.proxy
        except:
            pass
        res = res.__getattribute__(segment)
        if not res :
            return None

    return res