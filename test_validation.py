import unittest
from src.app import validate_create, parse_json

class ValidationTests(unittest.TestCase):
    def test_good_request(self):
        result = validate_create({'title': 'VPN outage', 'description': 'Cannot connect to VPN'})
        self.assertEqual(result['priority'], 'medium')
        self.assertEqual(result['category'], 'other')

    def test_reject_invalid_title(self):
        with self.assertRaises(ValueError):
            validate_create({'title': 'x', 'description': 'Problem connecting'})

    def test_reject_invalid_category(self):
        with self.assertRaises(ValueError):
            validate_create({'title': 'VPN outage', 'description': 'Cannot connect', 'category': 'secret'})

    def test_reject_array_body(self):
        with self.assertRaises(ValueError):
            parse_json({'body': '[]'})

if __name__ == '__main__':
    unittest.main()
