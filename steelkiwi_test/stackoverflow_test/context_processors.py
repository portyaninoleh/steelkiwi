import forms


def navbar_login_form(request):
    return {'login_form': forms.LoginForm(),
            'user': request.user}