import unittest
class TestStringMethods(unittest.TestCase):

    def test_valid_cidr_to_mask(self):
        self.assertEqual('128.0.0.0', conversions.cidr_to_mask('1'))

    def test_valid_mask_to_cidr(self):
        self.assertEqual('1', conversions.mask_to_cidr('128.0.0.0'))

    def test_invalid_cidr_to_mask(self):
        self.assertEqual('Invalid', conversions.cidr_to_mask('0'))

    def test_invalid_mask_to_cidr(self):
        self.assertEqual('Invalid', conversions.mask_to_cidr('0.0.0.0'))

    def test_valid_ipv4(self):
        self.assertTrue(conversions.is_valid_ipv4('127.0.0.1'))

    def test_invalid_ipv4(self):
        self.assertFalse(conversions.is_valid_ipv4('192.168.1.2.3'))


if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
        from methods import conversions
    else:
        from ..methods import conversions
    unittest.main()
