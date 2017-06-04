import uuid
from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField

from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_order_printed(email, order_number):
    print(email, order_number)
    msg_plain = render_to_string('emails/order_printed/message_body.txt', {'order_number': order_number})
    msg_html = render_to_string('emails/order_printed/message_body.html', {'order_number': order_number})

    send_mail(
        'Sendcertified Order Printed',
        msg_plain,
        'no-reply@sendcertified.co',
        [email],
        html_message=msg_html,
    )

def send_order_delivered(email, order_number, tracking_number):
    print(email, order_number)
    msg_plain = render_to_string('emails/order_delivered/message_body.txt', {'order_number': order_number, 'tracking_number': tracking_number})
    msg_html = render_to_string('emails/order_delivered/message_body.html', {'order_number': order_number, 'tracking_number': tracking_number})

    send_mail(
        'Sendcertified Order Printed',
        msg_plain,
        'no-reply@sendcertified.co',
        [email],
        html_message=msg_html,
    )

class MailOrder(models.Model):
    class Meta:
        app_label = 'main'

    order_number = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, blank=True, null=True)

    # Step 1: Landing Page Address
    sender_street_number = models.CharField(max_length=200)
    sender_route = models.CharField(max_length=200)
    sender_locality = models.CharField(max_length=200)
    sender_state = models.CharField(max_length=200)
    sender_postal_code = models.CharField(max_length=200)

    recipient_street_number = models.CharField(max_length=200)
    recipient_route = models.CharField(max_length=200)
    recipient_locality = models.CharField(max_length=200)
    recipient_state = models.CharField(max_length=200)
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
    usps_confirmation_number = models.CharField(max_length=200, blank=True)

    def save(self):
        try:
            current_order = MailOrder.objects.get(pk=self.id)
            if current_order.printed == False and self.printed == True:
                send_order_printed(self.email, self.order_number)
            if current_order.delivered_to_post_office == False and self.delivered_to_post_office == True:
                send_order_delivered(self.email, self.order_number, self.usps_confirmation_number)
        except:
            pass
        super(MailOrder, self).save()


    def __str__(self):
        return '%s %s' % (self.sender_name, self.recipient_name)
