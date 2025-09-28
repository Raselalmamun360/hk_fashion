from django import forms
from django.core.validators import EmailValidator

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Name',
            'autocomplete': 'name'
        })
    )
    
    email = forms.EmailField(
        max_length=100,
        required=True,
        validators=[EmailValidator()],
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Email',
            'autocomplete': 'email'
        })
    )
    
    subject = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Subject',
            'autocomplete': 'off'
        })
    )
    
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Your Message',
            'rows': 5
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        # Add any additional validation here if needed
        return cleaned_data
