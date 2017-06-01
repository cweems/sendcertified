import stripe

from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from ..forms import Payment
from ..models import MailOrder, User
from django.core.mail import send_mail

def payment(request):
    form = Payment(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            stripe.api_key = settings.STRIPE_KEY
            cleaned_form = form.cleaned_data
            stripe_token = cleaned_form['stripe_token']
            try:
                charge = stripe.Charge.create(
                  amount=900,
                  currency="usd",
                  description="Example charge",
                  source=stripe_token,
                )

                address = request.session['address']
                address_details = request.session['address_details']
                letter = request.session['letter']
                email = request.session.get('email', None)

                if request.user.is_authenticated():
                    user = User.objects.get(id=request.user.id)
                else:
                    user = None

                order = MailOrder(
                    user = user,

                    sender_street_number=address['sender_street_number'],
                    sender_route=address['sender_route'],
                    sender_locality=address['sender_locality'],
                    sender_state=address['sender_state'],
                    sender_country=address['sender_country'],
                    sender_postal_code=address['sender_postal_code'],

                    recipient_street_number=address['recipient_street_number'],
                    recipient_route=address['recipient_route'],
                    recipient_locality=address['recipient_locality'],
                    recipient_state=address['recipient_state'],
                    recipient_country=address['recipient_country'],
                    recipient_postal_code=address['recipient_postal_code'],

                    sender_name=address_details['sender_name'],
                    sender_unit=address_details['sender_unit'],

                    recipient_name=address_details['recipient_name'],
                    recipient_unit=address_details['recipient_unit'],

                    letter=letter['letter'],

                    email=email['email'],
                    payment_received=True,

                )
                order.save()
                order_number = str(order.order_number)
                send_mail("We received a new order!", "The order number is: " + order_number,
                    "Sendcertified <no-reply@sendcertified.co>", ["charlie.weems@gmail.com"])

                send_mail("Order received!", "Thanks for using Sendcertified. Your order number is: " + order_number,
                    "Sendcertified <no-reply@sendcertified.co>", [email['email']])
                return redirect('/confirmation/' + order_number)

            except stripe.error.CardError as e:
              # Since it's a decline, stripe.error.CardError will be caught
              body = e.json_body
              err  = body['error']

              print("Status 1 is: %s" % e.http_status)
              print("Type is: %s" % err['type'])
              print("Code is: %s" % err['code'])
              # param is '' in this case
              print("Param is: %s" % err['param'])
              print("Message is: %s" % err['message'])
              print('here')
              return render(request, 'orderform/payment.html', {'errors': err['message']})
            except stripe.error.RateLimitError as e:
              # Too many requests made to the API too quickly
              print("Status 2 is: %s" % e)
              return render(request, 'orderform/payment.html', {'errors': "We're sorry, there's been an error with our payment system. Your card was not charged. Please try again in a bit."})
            except stripe.error.InvalidRequestError as e:
              print("Status 3 is: %s" % e)
              # Invalid parameters were supplied to Stripe's API
              return render(request, 'orderform/payment.html', {'errors': "We're sorry, there's been an error with our payment system. Your card was not charged. Please try again in a bit."})
            except stripe.error.AuthenticationError as e:
              print("Status 4 is: %s" % e)
              # Authentication with Stripe's API failed
              # (maybe you changed API keys recently)
              return render(request, 'orderform/payment.html', {'errors': "We're sorry, there's been an error with our payment system. Your card was not charged. Please try again in a bit."})
            except stripe.error.APIConnectionError as e:
              print("Status 5 is: %s" % e)
              # Network communication with Stripe failed
              return render(request, 'orderform/payment.html', {'errors': "We're sorry, there's been an error with our payment system. Your card was not charged. Please try again in a bit."})
            except stripe.error.StripeError as e:
              print("Status 6 is: %s" % e)
              # Display a very generic error to the user, and maybe send
              # yourself an email
              return render(request, 'orderform/payment.html', {'errors': "We're sorry, there's been an error with our payment system. Your card was not charged. Please try again in a bit."})
            except Exception as e:
              print("Status 7 is: %s" % e)
              # Something else happened, completely unrelated to Stripe
              return render(request, 'orderform/payment.html', {'errors': "We're sorry, there's been an error with our payment system. Your card was not charged. Please try again in a bit."})

    address = request.session.get('address', None)
    address_details = request.session.get('address_details', None)
    letter = request.session.get('letter', None)

    if request.user.is_authenticated():
        user = User.objects.get(id=request.user.id)
        email = user.username

    else:
        email = request.session.get('email', None)

    return render(request, 'orderform/payment.html', {'address': address, 'address_details': address_details, 'letter': letter, 'email': email, 'payment_form': form})


def confirmation(request, uuid):
    try:
        order = MailOrder.objects.get(order_number=uuid)
        return render(request, 'orderform/confirmation.html', {'order': order})
    except:
        return redirect('/')
