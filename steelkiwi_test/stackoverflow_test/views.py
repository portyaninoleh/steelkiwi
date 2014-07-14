import base64

from django.core.mail import send_mail
from django.shortcuts import render
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.contrib.sites.models import get_current_site
from django.contrib.auth.models import User
from django.core.paginator import Paginator

from models import Question
from models import Response
from config import MAIL_CONFIG
import forms


class NewQuestionView(View):
    template = 'new_question.html'

    def get(self, request):
        return render(request, self.template, {'form': forms.QuestionForm()})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = forms.QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
        else:
            return render(request, self.template, {'form': form})


class QuestionView(View):
    template = 'question_list.html'

    def single_question(self, request):
        self.template = 'question.html'
        question = Question.objects.get(id=request.GET['question'])
        return render(request, self.template, {'question': question,
                                               'responses': question.response_set.all()})

    def get(self, request, *args, **kwargs):
        if request.GET.get('question', False):
            return self.single_question(request)
        page = request.GET.get('page')
        if not page:
            page = 1
        question_list = Paginator(Question.objects.all(), 2).page(page)
        return render(request, self.template, {'questions': question_list})


class ResponseView(View):

    @method_decorator(login_required)
    def post(self, request):
        if request.POST.get('response', False):
            response = Response()
            question = Question.objects.get(id=request.POST['question'])
            response.message = request.POST['response']
            response.question = question
            response.user = request.user
            response.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class LoginView(View):
    template = 'login.html'

    def get(self, request):
        return render(request, self.template, {'login_form': forms.LoginForm()})

    def post(self, request):
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                if user.is_active:
                    return HttpResponseRedirect('/')
                else:
                    return HttpResponseRedirect('/activation/')
            else:
                return render(request, self.template, {'login_form': login_form,
                                                       'authentication': 'Authentication failed'})
        else:
            return render(request, self.template, {'login_form': login_form})


class LogoutView(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')


class SignupView(View):
    template = 'signup.html'

    def get_message(self, request, user):
        template = "Hi {0}!\nYou are trying to sign up on stackoverflow site. " \
                   "Please click on <a href='{1}'>this link</a> to activate your account:\n"
        url = 'http://{0}/activation/?account={1}'.format(get_current_site(request).domain,
                                                          base64.urlsafe_b64encode(user.cleaned_data['email']))
        return template.format(user.cleaned_data['username'], url)

    def get(self, request):
        return render(request, self.template, {'form': forms.SignupForm()})

    def post(self, request):
        user_form = forms.SignupForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            user = authenticate(username=user_form.cleaned_data['username'],
                                password=user_form.cleaned_data['password1'])
            login(request, user)
            send_mail('Activation Stackoverflow Account',
                      self.get_message(request, user_form),
                      MAIL_CONFIG['mail_from'],
                      [user_form.cleaned_data['email']])
            print(self.get_message(request, user_form))
            return HttpResponseRedirect('/activation/')
        else:
            return render(request, self.template, {'form': user_form})


class ActivationView(View):
    template = 'activation.html'

    def get(self, request):
        account = request.GET.get('account')
        if account:
            email = base64.urlsafe_b64decode(account.encode('utf-8'))
            user = User.objects.get(email=email)
            user.is_active = True
            user.save()
            return HttpResponseRedirect('/')
        return render(request, self.template)


class RestorePasswordView(View):
    template = 'restore_password.html'

    def get(self, request):
        return render(request, self.template, {'form': forms.RestorePasswordForm()})

    def post(self, request):
        form = forms.RestorePasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            password = User.objects.make_random_password()
            user.set_password(password)
            print password
            user.save()
            send_mail('Your New Password',
                      'Please find your password bellow\n{0}'.format(password),
                      MAIL_CONFIG['mail_from'],
                      [email])
            return HttpResponseRedirect('/login/')
        return render(request, self.template, {'form': form})