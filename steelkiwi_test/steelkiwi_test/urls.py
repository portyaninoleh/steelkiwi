from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from stackoverflow_test.views import QuestionView
from stackoverflow_test.views import LoginView
from stackoverflow_test.views import LogoutView
from stackoverflow_test.views import ResponseView
from stackoverflow_test.views import SignupView
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'steelkiwi_test.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', QuestionView.as_view()),
    url(r'^login/$', LoginView.as_view()),
    url(r'^logout/$', LogoutView.as_view()),
    url(r'^response/$', ResponseView.as_view()),
    url(r'^signup/$', SignupView.as_view()),
)
