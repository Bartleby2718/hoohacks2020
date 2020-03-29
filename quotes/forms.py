from django import forms
from django.core.validators import RegexValidator


class SendTextForm(forms.Form):
    number_validator = RegexValidator(
        # Support US only for now
        regex='^[0-9]{10}$',
        message='Phone number should be exactly 10 digits.'
    )
    number = forms.CharField(
        min_length=10, max_length=10,
        validators=[number_validator]
    )
