from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import AddressDetails, AddressForm, DocumentEditor
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
    initial = {'address': request.session.get('address', None)}
    form = AddressDetails(request.POST or None, initial=initial)
    if request.method == 'POST':
        if form.is_valid():
            for item in form.cleaned_data:
                request.session['address'][item] = form.cleaned_data[item]
            print(request.session['address'])
            return HttpResponseRedirect(reverse('draft-letter'))

    if request.session['address']:
        main_address = request.session['address']
    else:
        return HttpResponseRedirect('/')
    return render(request, 'orderform/address_details.html', {'form': form, 'main_address': main_address})

def draft_letter(request):
    form = DocumentEditor()
    return render(request, 'orderform/draft_letter.html', {'form': form})

def payment(request):
    return render(request, 'orderform/payment.html')

def submit_mail_order(request):
    form = AddressDetails(request.POST)
    if form.is_valid():
        order = form.save(commit = False)
        order.user_id = request.user.id
        order.save()

    return HttpResponseRedirect('draft-letter')
