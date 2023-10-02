from django.core.exceptions import ValidationError


def validate_expiry_time(expiry_time):
    min_time = 300
    max_time = 30000
    if not min_time <= expiry_time <= 30000:
        raise ValidationError(f"Expiry time must be between {min_time} and {max_time}")
