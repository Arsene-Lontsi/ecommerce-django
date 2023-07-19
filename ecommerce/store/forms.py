from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from .models import Product
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password..'
    }))

class SignupForm(UserCreationForm):
    class  Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'username'
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'name@example.com'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password..'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm password..'
    }))

INPUT_CLASSES = 'form-control'
class NewProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', 'name', 'description', 'price', 'image',)

        widgets = {
            'category': forms.Select(attrs={
                'class':INPUT_CLASSES
            }),
            'name': forms.TextInput(attrs={
                'class':INPUT_CLASSES
            }),
            'description': forms.Textarea(attrs={
                'class':INPUT_CLASSES,
                'rows':3
            }),
            'price': forms.TextInput(attrs={
                'class':INPUT_CLASSES
            }),
            'image': forms.FileInput(attrs={
                'class':INPUT_CLASSES
            })
        }

class EditProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'image',)

        widgets = {
            'name': forms.TextInput(attrs={
                'class':INPUT_CLASSES
            }),
            'description': forms.Textarea(attrs={
                'class':INPUT_CLASSES,
                'rows':3
            }),
            'price': forms.TextInput(attrs={
                'class':INPUT_CLASSES
            }),
            'image': forms.FileInput(attrs={
                'class':INPUT_CLASSES
            })
        }