from django.forms import ModelForm, Textarea
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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


class SignupForm(UserCreationForm):
    email = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_email(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data["email"]
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Duplicated email')


    def save(self, commit=True):
        user = super(SignupForm, self).save(False)
        user.is_active = False
        user.save()
        return user


class RestorePasswordForm(forms.Form):
    email = forms.EmailField()