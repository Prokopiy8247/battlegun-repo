from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django.utils.translation import gettext_lazy as _

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')
        error_messages = {
            'username': {
                'unique': _("This username is not available."),
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = _('Letters, digits and @/./+/-/_ only.')
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'w-full bg-[#2a2a2a] text-white border-none rounded h-10 px-4 focus:ring-1 focus:ring-orange-500 text-sm outline-none'
            if field_name == 'email':
                field.required = True

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'w-full bg-[#2a2a2a] text-white border-none rounded h-10 px-4 focus:ring-1 focus:ring-orange-500 text-sm outline-none'
