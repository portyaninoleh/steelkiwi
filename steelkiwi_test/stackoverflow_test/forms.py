from django.forms import ModelForm, Textarea
from django import forms

from models import Question


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['subject', 'body', 'user']
        widgets = {
            'body': Textarea()
        }


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password'}))


class SignupForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField()