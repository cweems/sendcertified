from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField

class MailOrder(models.Model):
    class Meta:
        app_label = 'main'
    user = models.ForeignKey(User, blank=True, null=True)

    # Step 1: Landing Page Address
    sender_street_number = models.CharField(max_length=200)
    sender_route = models.CharField(max_length=200)
    sender_locality = models.CharField(max_length=200)
    sender_state = models.CharField(max_length=200)
    sender_country = models.CharField(max_length=200)
    sender_postal_code = models.CharField(max_length=200)

    recipient_street_number = models.CharField(max_length=200)
    recipient_route = models.CharField(max_length=200)
    recipient_locality = models.CharField(max_length=200)
    recipient_state = models.CharField(max_length=200)
    recipient_country = models.CharField(max_length=200)
    recipient_postal_code = models.CharField(max_length=200)

    #Step 2: Additional Details
    sender_name = models.CharField(max_length=200)
    sender_unit = models.CharField(max_length=200, blank=True, null=True)

    recipient_name = models.CharField(max_length=200)
    recipient_unit = models.CharField(max_length=200, blank=True, null=True)

    #Step 3: Message

    letter = HTMLField()

    #Step 4: Payment & Delivery
    email = models.CharField(max_length=200)
    payment_received = models.BooleanField(blank=True, default=False)
    printed = models.BooleanField(blank=True, default=False)
    delivered_to_post_office = models.BooleanField(blank=True, default=False)

    def __str__(self):
        return '%s %s' % (self.sender_name, self.recipient_name)
