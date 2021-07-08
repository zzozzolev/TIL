# User objects
- The primary attributes of the default user are:
 - username
 - password
 - email
 - first_name
 - last_name

# Validation
- `validate_password` 메서드에 `password_validators`를 `None`으로 넘겨주면 `get_default_password_validators()`를 호출한다.
    https://github.com/django/django/blob/ca9872905559026af82000e46cde6f7dedc897b6/django/contrib/auth/password_validation.py#L35-L44
- `get_default_password_validators()`는 `settings.AUTH_PASSWORD_VALIDATORS`를 사용한다.
    https://github.com/django/django/blob/ca9872905559026af82000e46cde6f7dedc897b6/django/contrib/auth/password_validation.py#L18-L19