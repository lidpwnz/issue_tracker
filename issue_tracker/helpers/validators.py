from django.core.exceptions import ValidationError


def title_with_create_input(string: str) -> None:
    if string.lower() == 'create':
        raise ValidationError('Summary cannot be "create"!', code='invalid_title')


def body_at_least_7(string: str) -> None:
    if len(string) < 7:
        raise ValidationError('Description length must be >= 7 or empty!', code='invalid_body_length')

