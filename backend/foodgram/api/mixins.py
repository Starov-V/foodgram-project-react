from users.validators import validate_username


class UsernameValidationMixin(object):
    def validate_username(self, value):
        return validate_username(value)
