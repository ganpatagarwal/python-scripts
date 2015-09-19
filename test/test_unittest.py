import unittest

def multiply(a,b):
	return a*b
	
class TestUM(unittest.TestCase):
 
    def setp(self):
        pass
 
    def testnumbers_3_4(self):
        self.assertEqual( multiply(3,4), 12)
 
    def teststrings_a_3(self):
        self.assertEqual( multiply('a',3), 'aaaaa')
 
if __name__ == '__main__':
    unittest.main()