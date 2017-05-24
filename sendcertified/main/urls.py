from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^address-details$', views.address_details, name='address-details'),
    url(r'^draft-letter$', views.draft_letter, name='draft-letter'),
    url(r'^payment$', views.payment, name='payment'),
    url(r'^submit_mail_order$', views.submit_mail_order, name='submit_mail_order'),
]
