from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'email', 'phone', 
            'address', 'city', 'postal_code', 'country', 'notes'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'Phone'}),
            'address': forms.Textarea(attrs={'class': 'w-full p-2 border rounded', 'rows': 3, 'placeholder': 'Address'}),
            'city': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'City'}),
            'postal_code': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'Postal Code'}),
            'country': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'Country'}),
            'notes': forms.Textarea(attrs={'class': 'w-full p-2 border rounded', 'rows': 3, 'placeholder': 'Notes (optional)'}),
        }
