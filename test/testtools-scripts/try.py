import testtools
import project

class TestSquare(testtools.TestCase):
    def test_square(self):
        # 'square' takes a number and multiplies it by itself.
        result = project.square(7)
        self.assertEqual(result, 49)

    def test_square_bad_input(self):
        # 'square' raises a TypeError if it's given bad input, say a
        # string.
        self.assertRaises(TypeError, project.square, "orange")

    def test_square_root_bad_input_2(self):
        # 'square' raises a TypeError if it's given bad input, say a
        # string.
        with testtools.ExpectedException(TypeError, "c.*"):
            project.square('orange')
    
    def test_assert_is_example(self):
        foo = [None]
        foo_alias = foo
        bar = [None]
        self.assertIs(foo, foo_alias)
        self.assertIsNot(foo, bar)
        self.assertEqual(foo, bar) # They are equal, but not identical
    
    def test_expect_failure_example(self):
        self.expectFailure(
            "cats should be dogs", self.assertEqual, 'cats', 'cats')
        