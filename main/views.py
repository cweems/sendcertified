import stripe

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import AddressDetails, AddressForm, DocumentEditor, OrderEmail, Payment
from .models import MailOrder, User

# Create your views here.
def index(request):
    initial = {'address': request.session.get('address', None)}
    form = AddressForm(request.POST or None, initial=initial)
    if request.method == 'POST':
        if form.is_valid():
            request.session['address'] = form.cleaned_data
            return HttpResponseRedirect(reverse('address-details'))
    return render(request, 'index.html', {'form': form})

def address_details(request):
    initial = {'address_details': request.session.get('address_details', None)}
    form = AddressDetails(request.POST or None, initial=initial)
    if request.method == 'POST':
        if form.is_valid():
            for item in form.cleaned_data:
                request.session['address_details'] = form.cleaned_data
            return HttpResponseRedirect(reverse('draft-letter'))

    if request.session['address']:
        main_address = request.session['address']
    else:
        return HttpResponseRedirect('/')
    return render(request, 'orderform/address_details.html', {'form': form, 'main_address': main_address})

def draft_letter(request):
    initial = {'letter': request.session.get('letter', None)}
    letter = initial['letter']
    form = DocumentEditor(request.POST or None, initial=letter)
    if request.method == 'POST':
        if form.is_valid():
            request.session['letter'] = form.cleaned_data
            return HttpResponseRedirect(reverse('identification'))
    return render(request, 'orderform/draft_letter.html', {'form': form})

def login_returning_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse('payment'))
        else:
            print('FORM INVALID')
            return HttpResponseRedirect(reverse('identification'))

def continue_as_guest(request):
    if request.method == 'POST':
        form = OrderEmail(request.POST)
        if form.is_valid():
            request.session['email'] = form.cleaned_data
            return HttpResponseRedirect(reverse('payment'))

        else:
            return HttpResponseRedirect(reverse('identification'))

def identification(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('payment'))

    returning_user_form = AuthenticationForm()
    guest_user_form = OrderEmail()
    return render(request, 'orderform/identification.html', {'returning_user_form': returning_user_form, 'guest_user_form': guest_user_form})

def payment(request):
    form = Payment(request.POST)
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
                email = request.session['email']

                order = MailOrder(
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

                    letter=letter,

                    email=email,
                    payment_received=True,

                )
                order.save()
                return HttpResponseRedirect('/confirmation')

            except stripe.error.CardError as e:
              # Since it's a decline, stripe.error.CardError will be caught
              body = e.json_body
              err  = body['error']

              print("Status is: %s" % e.http_status)
              print("Type is: %s" % err['type'])
              print("Code is: %s" % err['code'])
              # param is '' in this case
              print("Param is: %s" % err['param'])
              print("Message is: %s" % err['message'])
              print('here')
              return render(request, 'orderform/payment.html', {'errors': err['message']})
            except stripe.error.RateLimitError as e:
              # Too many requests made to the API too quickly
              pass
            except stripe.error.InvalidRequestError as e:
              # Invalid parameters were supplied to Stripe's API
              pass
            except stripe.error.AuthenticationError as e:
              # Authentication with Stripe's API failed
              # (maybe you changed API keys recently)
              pass
            except stripe.error.APIConnectionError as e:
              # Network communication with Stripe failed
              pass
            except stripe.error.StripeError as e:
              # Display a very generic error to the user, and maybe send
              # yourself an email
              pass
            except Exception as e:
              # Something else happened, completely unrelated to Stripe
              pass

    address = request.session.get('address', None)
    address_details = request.session.get('address_details', None)
    letter = request.session.get('letter', None)

    if request.user.is_authenticated():
        user = User.objects.get(id=request.user.id)
        email = user.username

    else:
        email = request.session.get('email', None)

    return render(request, 'orderform/payment.html', {'address': address, 'address_details': address_details, 'letter': letter, 'email': email, 'payment_form': form})

def confirmation(request):
    return render(request, 'orderform/confirmation.html')

def profile(request):
    if request.user.is_authenticated():
        orders = MailOrder.objects.filter(user=request.user)
        return render(request, 'profile.html', {'orders': orders})
    else:
        return HttpResponseRedirect('/login')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
