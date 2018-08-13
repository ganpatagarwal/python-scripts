class my_class():
    num = 0
    def __init__(self, greet):
        self.greet = greet
        my_class.num += 1

    def __repr__(self):
        print(dir(self))
        self.print_twice("a")
        self.print_thrice("b")
        self.print_num()
        return 'a custom object of %s %r' % (my_class.__name__, self.greet)

    def print_twice(self, data):
        print data * 2

    @staticmethod
    def print_thrice(data):
        print data * 3

    @classmethod
    def print_num(cls):
        print cls.num


a = my_class("hello")
print(a)
a.print_num()