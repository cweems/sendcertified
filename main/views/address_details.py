from django.shortcuts import render, redirect
from django.urls import reverse
from ..forms import AddressDetails

def address_details(request):
    initial = {'address_details': request.session.get('address_details', None)}
    form = AddressDetails(request.POST or None, initial=initial)
    if request.method == 'POST':
        if form.is_valid():
            for item in form.cleaned_data:
                request.session['address_details'] = form.cleaned_data
            return redirect(reverse('draft-letter'))

    if request.session['address']:
        main_address = request.session['address']
    else:
        return redirect('/')
    return render(request, 'orderform/address_details.html', {'form': form, 'main_address': main_address})
