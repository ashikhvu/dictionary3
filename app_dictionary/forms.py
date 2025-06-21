from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.forms import UserCreationForm
from .models import ItemModel
from django.core.exceptions import ValidationError
# from .models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    phone = forms.CharField(max_length=15, help_text="Enter a valid phone number.")

    class Meta:
        model = User
        fields = ["first_name","last_name","username","email","password1","password2","phone","profile_image","delivery_address"]

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if not phone.isdigit():
            return ValidationError("Its not a valid phone number")
        return phone

class ItemForm(forms.ModelForm):
    class Meta:
        model = ItemModel
        fields = '__all__'