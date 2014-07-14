import social_auth

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from stackoverflow_test.views import QuestionView
from stackoverflow_test.views import LoginView
from stackoverflow_test.views import LogoutView
from stackoverflow_test.views import ResponseView
from stackoverflow_test.views import SignupView
from stackoverflow_test.views import ActivationView
from stackoverflow_test.views import RestorePasswordView
from stackoverflow_test.views import NewQuestionView
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'steelkiwi_test.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('social_auth.urls')),
    url(r'^$', QuestionView.as_view(), name='question_list'),
    url(r'^new_question/$', NewQuestionView.as_view()),
    url(r'^login/$', LoginView.as_view()),
    url(r'^logout/$', LogoutView.as_view()),
    url(r'^response/$', ResponseView.as_view()),
    url(r'^signup/$', SignupView.as_view()),
    url(r'^activation/$', ActivationView.as_view()),
    url(r'^restore_password/$', RestorePasswordView.as_view())
)
