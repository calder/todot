import re
import string

indent_re = re.compile(" *")
symbol_re = re.compile("\S+")

class Symbol:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return ":"+self.name
    def stringify(self, indent):
        return self.name

class String(str):
    def stringify(self, indent):
        return repr(self)

class Block(list):
    def __repr__(self):
        return self.stringify(0)
    def stringify(self, indent):
        if len(self) == 0:
            return ""
        elif len(self) == 1:
            return self[0].stringify(indent+1)
        else:
            return ("\n"+"    "*indent).join([e.stringify(indent+1) for e in self])

class ParseException(RuntimeError): pass

def leading_spaces(line):
    return len(indent_re.match(line).group(0))

def parse_string(line, start):
    end = string.find(line, '"', start+1)
    if end == -1: raise ParseException("Unterminated quote.")
    return String(line[start+1:end]), end+1

def parse_symbol(line, start):
    end = start + len(symbol_re.match(line[start:]).group(0))
    return Symbol(line[start:end]), end

def parse_line(line):
    tokens = Block()

    i = leading_spaces(line)
    while i < len(line):
        if   line[i] == '#': break
        elif line[i] == '"': token, i = parse_string(line, i)
        else:                token, i = parse_symbol(line, i)
        tokens.append(token)
        i += leading_spaces(line[i:])

    return tokens

def parse_block(lines, indent, start):
    block = Block()

    i = start
    while i < len(lines):
        line = lines[i]
        line_indent = leading_spaces(line)

        if line_indent > indent:
            if len(block) == 0: raise ParseException("Unexpected indent.")
            inner_block, i = parse_block(lines, line_indent, i)
            block[-1] += inner_block
        elif line_indent < indent:
            return block, i
        else:
            tokens = parse_line(line)
            if   len(tokens) == 0: pass
            elif len(tokens) == 1: block.append(tokens[0])
            else:                  block.append(tokens)
            i += 1

    return block, i

def parse_lines(lines):
    return parse_block(lines, 0, 0)[0]

def parse_file(file_name):
    lines = open(file_name).readlines()
    lines = [line.rstrip() for line in lines]
    return parse_lines(lines)