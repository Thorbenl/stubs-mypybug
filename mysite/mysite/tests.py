from django.core.exceptions import ValidationError
from django.test.testcases import TestCase

from mysite.mysite.validator import EmailDnsValidator


class EmailDnsValidatorTest(TestCase):
    def test_validator(self):
        cases = {
            'username@invalid': False,
            'username@nonexistent.dk': False,
            'username@hotmale.com': False, # actual typo made by one of the BSP users
            'username@gmail.com': True,
        }
        validator = EmailDnsValidator(allowlist=[])
        validator.test_mode = False
        for email, expected_result in cases.items():
            with self.subTest(email):
                try:
                    validator(email)
                    self.assertTrue(expected_result, 'should throw validation error')
                except ValidationError:
                    self.assertFalse(expected_result, 'should validate')
