class Hello(object):
    def __init__(self):
        self.name = 'random'
        print "In __init__"

    def get_element_by_partial_link_text(self):
        print self.name
        
#el = Hello()
#el.get_element_by_partial_link_text()