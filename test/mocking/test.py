import unittest,mock
from mock_test import method,Target

class MethodTestCase(unittest.TestCase):

	@mock.patch.object(Target, 'apply',autospec=True)
	def test_method(self,mock_apply):
		target = Target()
		method(target, "value")
		mock_apply.assert_called_with("value")

if __name__ == "__main__":
	unittest.main()

