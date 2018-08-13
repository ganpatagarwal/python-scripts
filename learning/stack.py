class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None


class Stack(object):
    def __init__(self):
        self.top = None
        self.size = 0

    def push(self, data):
        node = Node(data)
        if self.top:
            node.next = self.top
            self.top = node
        else:
            self.top = node
        self.size += 1

    def pop(self):
        if self.top:
            data = self.top.data
            self.size -= 1
            if self.top.next:
                self.top = self.top.next
            else:
                self.top = None
            return data
        else:
            return None

    def peek(self):
        if self.top:
            return self.top.data
        else:
            return None


def check_brackets(statement):
    stack = Stack()
    last = None
    for ch in statement:
        if ch in ('{', '[', '('):
            stack.push(ch)
            continue
        if ch in ('}', ']', ')'):
            last = stack.pop()
        if last is None:
            continue
        elif last is '{' and ch is '}':
            continue
        elif last is '[' and ch is ']':
            continue
        elif last is '(' and ch is ')':
            continue
        else:
            return False

    if stack.size > 0:
        return False
    else:
        return True

sl = (
   "{(foo)(bar)}[hello](((this)is)a)test",
   "{(foo)(bar)}[hello](((this)is)atest",
   "{(foo)(bar)}[hello](((this)is)a)test))",
    "{hello}"
)
for s in sl:
   m = check_brackets(s)
   print("{}: {}".format(s, m))