from django.conf.urls import url, include
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^address-details$', views.address_details, name='address-details'),
    url(r'^draft-letter$', views.draft_letter, name='draft-letter'),
    url(r'^upload-letter$', views.upload_letter, name='upload-letter'),
    url(r'^sign_s3$', views.sign_s3, name='sign_s3'),
    url(r'^identification$', views.identification, name='identification'),
    url(r'^login-returning-user$', views.login_returning_user, name='login_returning_user'),
    url(r'^continue-as-guest$', views.continue_as_guest, name='continue_as_guest'),
    url(r'^payment$', views.payment, name='payment'),
    url(r'^confirmation/(?P<uuid>[0-9a-f]{8}\-[0-9a-f]{4}\-4[0-9a-f]{3}\-[89ab][0-9a-f]{3}\-[0-9a-f]{12})/$', views.confirmation, name='confirmation'),
    url(r'^logout$', views.logout_view, name='logout'),
    url('^register/', CreateView.as_view(
            template_name='register.html',
            form_class=UserCreationForm,
            success_url='/'
    )),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^accounts/profile/$', views.profile, name='profile'),
    url(r'^privacy$', TemplateView.as_view(template_name='privacy.html'), name="privacy")
]
