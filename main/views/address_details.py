from django.shortcuts import render, redirect
from django.urls import reverse
from ..forms import AddressForm

def address_details(request):
    initial = request.session.get('address', None)
    if request.GET.get('clear') == 'true':
        initial = []
    form = AddressForm(request.POST or None, initial=initial)
    if request.method == 'POST':
        if form.is_valid():
            for item in form.cleaned_data:
                request.session['cleaned_address'] = form.cleaned_data
            return redirect(reverse('draft-letter'))
        else:
            return redirect('/')

    return render(request, 'orderform/address_details.html', {'form': form })
