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
from django.contrib.auth.models import User
from django.contrib.sites.models import get_current_site

from models import Question
from models import Response
from config import MAIL_CONFIG
import forms


class QuestionView(View):
    template = 'question_list.html'

    def single_question(self, request):
        self.template = 'question.html'
        question = Question.objects.get(id=request.GET['question'])
        return render(request, self.template, {'question': question,
                                               'responses': question.response_set.all()})

    def get(self, request, *args, **kwargs):
        # form = forms.QuestionForm()
        if request.GET.get('question', False):
            return self.single_question(request)
        question_list = Question.objects.all()
        return render(request, self.template, {'questions': question_list})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = forms.QuestionForm(request.POST)
        if form.is_valid():
            form.save()
        return render(request, self.template, {'form': form})


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
        return render(request, self.template)

    def post(self, request):
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user and user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect('/activation/')
        else:
            return render(request, self.template)


class LogoutView(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')


class SignupView(View):
    template = 'signup.html'

    def get_message(self, request, user):
        template = "Hi {0}!\nYou are trying to sign up on stackoverflow site. " \
                   "Please click on <a href='{1}'>this link</a> to activate your account:\n"
        url = 'http://{0}/activation/?account={1}'.format(get_current_site(request).domain, base64.urlsafe_b64encode(user.email))
        return template.format(user.username, url)


    def get(self, request):
        return render(request, self.template, {'form': forms.SignupForm()})

    def post(self, request):
        user_form = forms.SignupForm(request.POST)
        if user_form.is_valid():
            user = User()
            user.username = user_form.cleaned_data['username']
            user.password = user_form.cleaned_data['password']
            user.email = user_form.cleaned_data['email']
            user.is_active = False
            user.save()
            send_mail('Activation Stackoverflow Account',
                      self.get_message(request, user),
                      MAIL_CONFIG['mail_from'],
                      [user.email])
            return HttpResponseRedirect('/activation/')
        else:
            return render(request, self.template, {'form': user_form})
