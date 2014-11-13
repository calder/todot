import re
import string

name = "[\w-]+"
task_re = re.compile(r"(%s)\s*=\s*(.*?)\s*\[(%s)\]$" % (name, name))
dpnd_re = re.compile(r"(%s)\s*>\s*(%s)$" % (name, name))

class ParseException(RuntimeError): pass

class Task:
    def __init__(self, name, description, status):
        self.name = name
        self.description = description
        self.status = status
        self.children = set()
        self.parents = set()
    def __repr__(self):
        return "%s:%s" % (self.name, self.status)

def parse_file(file_name):
    tasks = {}
    dependencies = set()

    line_number = 0
    for line in open(file_name):
        line_number += 1
        comment = line.find("#")
        if comment > 0: line = line[:comment]
        line = line.strip()

        task = task_re.match(line)
        dpnd = dpnd_re.match(line)
        if line == "":
            continue
        elif task:
            name = task.group(1)
            description = task.group(2)
            status = task.group(3)
            tasks[name] = Task(name, description, status)
        elif dpnd:
            parent = dpnd.group(1)
            child = dpnd.group(2)
            dependencies.add((parent,child))
        else:
            raise ParseException("Syntax error: %s:%d" % (file_name, line_number))

    for d in dependencies:
        if not tasks.has_key(d[0]): raise ParseException("Task '%s' was never defined." % d[0])
        if not tasks.has_key(d[1]): raise ParseException("Task '%s' was never defined." % d[1])
        tasks[d[0]].children.add(d[1])
        tasks[d[1]].parents.add(d[0])

    return tasks

for v in parse_file("sample.txt").values(): print v