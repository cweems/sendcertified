from django.conf.urls import url
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^address-details$', views.address_details, name='address-details'),
    url(r'^draft-letter$', views.draft_letter, name='draft-letter'),
    url(r'^identification$', views.identification, name='identification'),
    url(r'^login-returning-user$', views.login_returning_user, name='login_returning_user'),
    url(r'^continue-as-guest$', views.continue_as_guest, name='continue_as_guest'),
    url(r'^payment$', views.payment, name='payment'),
    url(r'^confirmation$', views.confirmation, name='confirmation'),
    url(r'^logout$', views.logout_view, name='logout'),
    url('^register/', CreateView.as_view(
            template_name='register.html',
            form_class=UserCreationForm,
            success_url='/'
    )),
    url(r'^accounts/profile/$', views.profile, name='profile')
]
