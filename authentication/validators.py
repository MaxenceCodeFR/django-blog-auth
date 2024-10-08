from django.core.exceptions import ValidationError

class ContainLetterValidator:

    def validate(self, password, user=None):
        if not any(char.isalpha() for char in password):
            raise ValidationError(
                "Le mot de passe doit contenir une lettre", code="password_no_letter"
            )

    def get_help_text(self):
        return "Le mot de passe doit contenir une lettre"

class ContainNumberValidator:

    def validate(self, password, user=None):
        if not any(char.isdigit() for char in password):
            raise ValidationError(
                "Le mot de passe doit contenir un chiffre", code="password_no_number"
            )

    def get_help_text(self):
        return "Le mot de passe doit contenir un chiffre"