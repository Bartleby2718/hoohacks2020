from django import forms
from django.core.validators import RegexValidator


class SendTextForm(forms.Form):
    number_validator = RegexValidator(
        # Support US only for now
        regex='^[0-9]{10}$',
        message='Phone number should be exactly 10 digits.'
    )
    number = forms.CharField(
        min_length=10, max_length=10, label='Your phone number',
        widget=forms.TextInput(attrs={
            'class': 'form-group mx-sm-3 mb-2',
            'style': 'width: 250px',
            'aria-describedby': 'help',
            'placeholder': 'Enter your 10-digit phone number',
        }),
        validators=[number_validator]
    )
