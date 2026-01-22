from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'email', 'phone', 
            'address', 'city', 'postal_code', 'country', 'notes'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': _('First Name')}),
            'last_name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': _('Last Name')}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': _('Email')}),
            'phone': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': _('Phone')}),
            'address': forms.Textarea(attrs={'class': 'w-full p-2 border rounded', 'rows': 3, 'placeholder': _('Address')}),
            'city': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': _('City')}),
            'postal_code': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': _('Postal Code')}),
            'country': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': _('Country')}),
            'notes': forms.Textarea(attrs={'class': 'w-full p-2 border rounded', 'rows': 3, 'placeholder': _('Notes (optional)')}),
        }
