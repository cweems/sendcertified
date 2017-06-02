from django.shortcuts import render, redirect
from django.urls import reverse
from ..forms import GoogleAddressForm

def index(request):
    initial = request.session.get('address', None)
    form = GoogleAddressForm(request.POST or None, initial=initial)
    if request.method == 'POST':
        if form.is_valid():
            print('FOrm valid')
            request.session['address'] = form.cleaned_data
            return redirect(reverse('address-details'))
    return render(request, 'index.html', {'form': form})
