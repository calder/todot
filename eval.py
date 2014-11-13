from parser import *

def call_undefined():
    pass

def default_context():
    context = {}
    context["__undefined__"] = call_undefined()
    return context

def eval_block(exp, context):
    for child in exp[1:]:
        eval(child, context)

def eval(exp, context):
    if isinstance(exp, String): return exp
    elif isinstance(exp, Symbol): return eval_symbol(exp, context)
    elif isinstance(exp, Block): return eval_block(exp, context)

print eval(parse_file("sample.txt"), default_context())