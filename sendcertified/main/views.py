from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import AddressDetails, AddressForm, DocumentEditor
from .models import MailOrder
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
            return HttpResponseRedirect(reverse('notifications'))
    return render(request, 'orderform/draft_letter.html', {'form': form})

def notifications(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('payment'))

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect(reverse('payment'))
    else:
        form = UserCreationForm()
    return render(request, 'orderform/notifications.html', {'form': form})

def payment(request):
    if request.method == 'POST':
        # TODO - Implement Stripe Here
        return HttpResponseRedirect('/')

    if request.session['address']:
        address = request.session['address']
        print(address)

    if request.session['address_details']:
        address_details = request.session['address_details']

    if request.session['letter']:
        letter = request.session['letter']
    return render(request, 'orderform/payment.html', {'address': address, 'address_details': address_details, 'letter': letter})

def submit_mail_order(request):
    form = AddressDetails(request.POST)
    if form.is_valid():
        order = form.save(commit = False)
        order.user_id = request.user.id
        order.save()

    return HttpResponseRedirect('draft-letter')

def profile(request):
    if request.user.is_authenticated():
        orders = MailOrder.objects.filter(user=request.user)
        return render(request, 'profile.html', {'orders': orders})
    else:
        return HttpResponseRedirect('/login')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
