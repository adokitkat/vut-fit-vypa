#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project name: Compiler Implementation for VYPlanguage Programming Language
# Authors: Adam Múdry (xmudry01), Daniel Paul (xpauld00)

from vypa_compiler.internals._models import symbol_table, Function

class Node:
    def __init__(self, name = None, left= None, right = None, type = None, value= None ):
        self.name = name
        self.left  = left
        self.right = right
        self.type = type
        self.value = value

    def insert_left(self,node):
        self.left = node
        return self.left

    def insert_right(self,node):
        self.right = node
        return self.right

    def display(self):
        lines, *_ = self._display_aux()
        for line in lines:
            print(line)

    def _display_aux(self):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if self.right is None and self.left is None:
            line = '%s' % str(self)
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if self.right is None:
            lines, n, p, x = self.left._display_aux()
            s = '%s' % str(self)
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if self.left is None:
            lines, n, p, x = self.right._display_aux()
            s = '%s' % str(self)
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self.left._display_aux()
        right, m, q, y = self.right._display_aux()
        s = '%s' % str(self)
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2

    def __str__(self):
        output = [self.name]
        if self.type:
            output.append(self.type)
        if self.value:
            output.append(self.value)
        return str(output)

    def __repr__(self):
        ret = []
        if self.name:
            ret.append(str(self.name))
        if self.type:
            ret.append(str(self.type))
        if self.value:
            ret.append(str(self.value))
        return ' | '.join(ret)

built_in_functions = ['readInt', 'readString', 'length', 'subStr', 'print']
def generate_functions(sym_tab) -> list[Node]:
    asts = []
    for key, value in sym_tab[0].scope.items():
        if key not in built_in_functions and isinstance(value, Function):
            root = Node('root', type='Function', value=value.name, right = Node())
            generate(root.right, value.body[0])
            root.display()
            asts.append(root)
    return asts
    
            

def generate(root, body):
    
    if body == None:
        return

    if body[0] == 'statement-scope':
        # statement-scope
        root.name = 'Statement-scope'
        root.right = Node()
        generate(root.right, body[1])

    if body[0] == 'statement':
        # ("statement", special_stmt, stmt/None)
        root.name = 'Statement'
        root.left = Node()
        generate(root.left, body[1]) #(statement,(...),(statement,(...),(statement,...)))
        if (body[2] != None):
            root.right = Node()
            generate(root.right, body[2])

    if body[0] == 'variable-definition':
        # ('variable-definition', ('var-type', 'Rectangle'), 'r',  (next-var, r2,  (next-var, r3, None))
        root.name = 'Variable-definition'
        root.type = body[1][1]
        root.value = body[2]
        if (body[3] != None):
            root.left = Node(type=body[1][1])
            generate(root.left, body[3])

    if body[0] == 'next-var':
        # (next-var, width,  (next-var, height, ...)
        root.name = 'Variable-definition'
        root.value = body[1]
        if (body[2] != None):
            root.left = Node(type=root.type)
            generate(root.left, body[2]) 

    if body[0] == 'statement-id':
        root.left = Node('=', Node('.', Node('Identifier', value = body[1]), Node('Property',  value = body[2])), Node('Todo expression')) # TODO Right side expression
    
    if body[0] == 'statement-while':
        #  ("statement-while", expr, new_scope)
        root.name = 'while'
        root.left = Node()
        root.right = Node()
        generate(root.left, body[1])
        generate(root.right, body[2])
    
    if body[0] == 'statement-if':
        # ("statement-if", expr, Doif_new_scope, Doelse_new_scopes)
        root.name = 'if'
        root.left = Node()
        generate(root.left, body[1]) # Condition
        root.right = Node('else')
        root = root.right
        root.left = Node()
        generate(root.left, body[2])
        root.right = Node()
        generate(root.right, body[3])

    if body[0] == 'statement-expr':
        #  ("statement-expr", expr)
        generate(root, body[1])
    
    if body[0] == 'variable-assignment':
        # ("variable-assignment", id, expr)
        root.name = '='
        root.left = Node('Variable', value=body[1])
        root.right = Node()
        generate(root.right, body[2])

    if body[0] == 'expression-parentheses':
        # ("expression-parentheses", expr)
        generate(root, body[1])
    
    if body[0] in ['expression-arithmetic-binary', 'expression-logical-binary', 'expression-relational']:
        # ("expression-arithmetic-binary", op, expr1, expr2)
        if root is not None:
            op = body[1]
            root.name = op 
            root.type = 'Binary'
            root.left = Node()
            root.right = Node()
            generate(root.left, body[2])
            generate(root.right, body[3])

    if body[0] in ['expression-arithmetic-unary', 'expression-logical-unary']:
        # ("expression-arithmetic-unary", op, expr)
        if root is not None:
            op = body[1]
            root.name = op
            root.type = 'Unary'
            root.right = Node()
            generate(root.right, body[2])

    if body[0] == 'expression-value':
        # ("expression-value", id/type, id/value)
        if root is not None:
            if body[1] == 'int':
                root.name ='Int-Literal'
                root.value = body[2]

            elif body[1] == 'string':
                root.name = 'String-Literal'
                root.value = body[2]

            else:
                root.name = 'Identifier'
                root.value = body[2]
    
    if body[0] == 'expression-class-new':
        # ("expression-class-new", id)
        if root is not None:
            root.name = 'Class-new'
            root.value = body[1]
            
    if body[0] == 'expression-class-op':
        # ("expression-class-op", id/this/super, expr)
        root.name = '.'
        root.left = Node('Variable', value=body[1])
        generate(root.left, body[1])
        if body[2] is not None:
            root.right = Node()
            generate(root.right, body[2])

    if body[0] == 'expression-function-call':
        # ("expression-function-call", id, expr_list/None)
        if root is not None:
            root.name = 'Function-call'
            root.value = body[1]
            if body[2] is not None:
                root.right = Node()
                generate(root.right, body[2])

    if body[0] == 'expression-list':
        # ("expression-list", expr, next_expr/None)
        root.name = 'Expression-list'
        root.left = Node()
        generate(root.left, body[1])
        if body[2] is not None:
            root.right = Node()
            generate(root.right, body[2])
    
    if body[0] == 'next-expression':
        # ("next-expression", expr, next_expr/None)
        root.name = 'Next-expression'
        root.left = Node()
        generate(root.left, body[1])
        if body[2] is not None:
            root.right = Node()
            generate(root.right, body[2])

    if body[0] == 'expression-cast':
        # ("expression-cast", int/strng, expr)
        root.name = 'Expression-cast'
        root.left = Node('Cast-type', value = body[1])
        root.right = Node()
        generate(root.right, body[2])
    
    if body[0] == 'statement-return':
        # ("statement-return", expr)
        root.name = 'return'
        if body[1] != None:
            root.left = Node()
            generate(root.left, body[1])

    if body[0] == 'statement-this-assignment':
        # ("statement-this-assignment", this/super, id, expr)
        root.name = '='
        root.left = Node(".")
        root.left.left = Node("Variable", value=body[1])
        root.left.right = Node('Variable', value = body[2])
        root.right = Node()
        generate(root.right, body[3])