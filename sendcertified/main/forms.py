from django import forms
from .models import MailOrder
from tinymce.widgets import TinyMCE

class AddressForm(forms.ModelForm):
    class Meta:
        model = MailOrder
        widgets = {
            'sender_street_number': forms.HiddenInput(),
            'sender_route': forms.HiddenInput(),
            'sender_locality': forms.HiddenInput(),
            'sender_state': forms.HiddenInput(),
            'sender_country': forms.HiddenInput(),
            'sender_postal_code': forms.HiddenInput(),

            'recipient_street_number': forms.HiddenInput(),
            'recipient_route': forms.HiddenInput(),
            'recipient_locality': forms.HiddenInput(),
            'recipient_state': forms.HiddenInput(),
            'recipient_country': forms.HiddenInput(),
            'recipient_postal_code': forms.HiddenInput(),
        }
        fields = [
            'sender_street_number',
            'sender_route',
            'sender_locality',
            'sender_state',
            'sender_country',
            'sender_postal_code',

            'recipient_street_number',
            'recipient_route',
            'recipient_locality',
            'recipient_state',
            'recipient_country',
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
