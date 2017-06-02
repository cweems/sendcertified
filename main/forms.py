from django import forms
from .models import MailOrder
from tinymce.widgets import TinyMCE

class GoogleAddressForm(forms.Form):
    sender_street_number = forms.CharField(max_length=100, required=False, widget=forms.HiddenInput())
    sender_route = forms.CharField(max_length=100, required=False, widget=forms.HiddenInput())
    sender_locality = forms.CharField(max_length=100, required=False, widget=forms.HiddenInput())
    sender_state = forms.CharField(max_length=100, required=False, widget=forms.HiddenInput())
    sender_postal_code = forms.CharField(max_length=100, required=False, widget=forms.HiddenInput())

    recipient_street_number = forms.CharField(max_length=100, required=False, widget=forms.HiddenInput())
    recipient_route = forms.CharField(max_length=100, required=False, widget=forms.HiddenInput())
    recipient_locality = forms.CharField(max_length=100, required=False, widget=forms.HiddenInput())
    recipient_state = forms.CharField(max_length=100, required=False, widget=forms.HiddenInput())
    recipient_postal_code = forms.CharField(max_length=100, required=False, widget=forms.HiddenInput())

class AddressForm(forms.ModelForm):
    class Meta:
        model = MailOrder
        fields = [
            'sender_name',
            'sender_unit',
            'sender_street_number',
            'sender_route',
            'sender_locality',
            'sender_state',
            'sender_postal_code',

            'recipient_name',
            'recipient_unit',
            'recipient_street_number',
            'recipient_route',
            'recipient_locality',
            'recipient_state',
            'recipient_postal_code',
        ]

class DocumentEditor(forms.ModelForm):
    class Meta:
        model = MailOrder
        fields = [
            'letter',
        ]

class AddressDetails(forms.ModelForm):
    class Meta:
        model = MailOrder
        fields = [
            'sender_name',
            'sender_unit',
            'recipient_name',
            'recipient_unit',
        ]

class OrderEmail(forms.ModelForm):
    class Meta:
        model = MailOrder
        fields = [
            'email'
        ]

class Payment(forms.Form):
    stripe_token = forms.CharField(label='Stripe token', max_length=100, widget=forms.HiddenInput(), required=False)
