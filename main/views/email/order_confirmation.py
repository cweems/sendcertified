from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_confirmation(email, order_number):
    print(email, order_number)
    msg_plain = render_to_string('emails/order_confirmation/message_body.txt', {'order_number': order_number})
    msg_html = render_to_string('emails/order_confirmation/message_body.html', {'order_number': order_number})

    send_mail(
        'Sendcertified Order Received',
        msg_plain,
        'no-reply@sendcertified.co',
        [email],
        html_message=msg_html,
    )
