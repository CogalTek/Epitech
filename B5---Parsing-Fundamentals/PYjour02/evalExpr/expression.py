from pyrser import grammar, meta
from pyrser.directives import ignore

class Expression(grammar.Grammar):
    last_oper = None
    last_right = None
    entry = 'EvalExpr'
    grammar = '''
    EvalExpr = [ #is_begin(_) [Expression:expr #add_expression(_, expr) ]*eof]

    Expression = [ #is_begin_expr(_) Value:v #add_first(_, v) [ Product:p Value:v #is_add_product(_, p, v) ]* ]

    Product = [ '*' | '/' | '%' | '+' | '-' ]

    Value = [ num:n #is_add_value(_, n) ]
    '''

@meta.hook(Expression)
def is_begin(self, ast):
    ast.results = []
    return True

@meta.hook(Expression)
def add_expression(self, ast, expr):
    if (self.last_oper == '+'):
        expr.res += self.last_right
    elif (self.last_oper == '-'):
        expr.res -= self.last_right
    ast.results.append(expr.res)
    return True

@meta.hook(Expression)
def is_begin_expr(self, ast):
    ast.res = 0
    self.last_oper = None
    self.last_right = None
    return True

@meta.hook(Expression)
def add_first(self, ast, value):
    ast.res = int(self.value(value))
    return True

@meta.hook(Expression)
def is_add_product(self, ast, product, value):
    right = int(self.value(value))

    if self.value(product) == '*':
        if (self.last_oper == '+'):
            ast.res = ast.res + self.last_right * right
        elif (self.last_oper == '-'):
            ast.res = ast.res - self.last_right * right
        else:
            ast.res *= right
        self.last_oper = None
        self.last_right = None
    elif self.value(product) == '/':
        if (self.last_oper == '+'):
            ast.res = ast.res + self.last_right / right
        elif (self.last_oper == '-'):
            ast.res = ast.res - self.last_right / right
        else:
            ast.res /= right
        self.last_oper = None
        self.last_right = None

    elif self.value(product) == '%':
        if (self.last_oper == '+'):
            ast.res = ast.res + self.last_right % right
        elif (self.last_oper == '-'):
            ast.res = ast.res - self.last_right % right
        else:
            ast.res %= right
        self.last_oper = None
        self.last_right = None
    elif self.value(product) == '+':
        if (self.last_oper == '+'):
            ast.res += self.last_right
        elif (self.last_oper == '-'):
            ast.res -= self.last_right
        self.last_oper = self.value(product)
        self.last_right = right

    elif self.value(product) == '-':
        if (self.last_oper == '+'):
            ast.res += self.last_right
        elif (self.last_oper == '-'):
            ast.res -= self.last_right
        self.last_oper = self.value(product)
        self.last_right = right

    return True

@meta.hook(Expression)
def is_add_value(self, ast, value):
    return True