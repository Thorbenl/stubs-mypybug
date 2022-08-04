from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from dns.resolver import resolve, NXDOMAIN, NoAnswer


class EmailDnsValidator(EmailValidator):
    """
    extends default pattern-matching behaviour to also reject email address
    if domain doesn't exist or has no MX record
    """
    from django.conf import settings
    test_mode = settings.RUNNING_TESTS

    def __call__(self, value):
        super().__call__(value)

        if self.test_mode:
            return
        user_part, domain_part = value.rsplit('@', 1)
        try:
            records_found = resolve(domain_part, 'MX')
        except (NXDOMAIN, NoAnswer):
            raise ValidationError(self.message, code=self.code)

        mx_record_found = len(records_found) > 0
        if not mx_record_found:
            raise ValidationError(self.message, code=self.code)