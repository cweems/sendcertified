from django.shortcuts import render, redirect
from django.urls import reverse
from ..forms import AddressForm

def index(request):
    initial = {'address': request.session.get('address', None)}
    form = AddressForm(request.POST or None, initial=initial)
    if request.method == 'POST':
        if form.is_valid():
            request.session['address'] = form.cleaned_data
            return redirect(reverse('address-details'))
    return render(request, 'index.html', {'form': form})
