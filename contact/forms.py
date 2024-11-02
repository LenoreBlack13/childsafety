# contact/forms.py

from django import forms
from .models import Contact
import re

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'phone', 'email', 'project']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ваше имя', 'required': True}),
            'phone': forms.TextInput(attrs={'placeholder': 'Ваш номер телефона', 'required': True}),
            'email': forms.EmailInput(attrs={'placeholder': 'Ваш email', 'required': True}),
            'project': forms.Select(attrs={'required': True})
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Удаление пробелов и специальных символов, кроме "+"
        clean_phone = re.sub(r'[^\d+]', '', phone)
        pattern = re.compile(r'^\+(\d{10,15})$|^(\d{10,15})$')
        if not pattern.match(clean_phone):
            raise forms.ValidationError(
                'Введите корректный номер телефона, начинающийся с + или состоящий только из цифр.')
        return clean_phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email