from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Flower, Order

class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email']

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1)

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['delivery_date_time', 'address', 'comment']