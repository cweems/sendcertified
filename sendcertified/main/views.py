from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import AddressDetails, AddressForm, DocumentEditor, OrderEmail
from .models import MailOrder, User
import stripe
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
    if request.method == 'POST':
        # TODO - Implement Stripe Here
        return HttpResponseRedirect('/')

    address = request.session.get('address', None)
    address_details = request.session.get('address_details', None)
    letter = request.session.get('letter', None)

    if request.user.is_authenticated():
        user = User.objects.get(id=request.user.id)
        email = user.username
        print("EMAIL:")
        print(email)
    else:
        email = request.session.get('email', None)

    return render(request, 'orderform/payment.html', {'address': address, 'address_details': address_details, 'letter': letter, 'email': email})

def profile(request):
    if request.user.is_authenticated():
        orders = MailOrder.objects.filter(user=request.user)
        return render(request, 'profile.html', {'orders': orders})
    else:
        return HttpResponseRedirect('/login')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
