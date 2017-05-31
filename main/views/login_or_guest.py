from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from ..forms import OrderEmail

def identification(request):
    if request.user.is_authenticated():
        return redirect(reverse('payment'))

    returning_user_form = AuthenticationForm()
    guest_user_form = OrderEmail()
    return render(request, 'orderform/identification.html', {'returning_user_form': returning_user_form, 'guest_user_form': guest_user_form})

def login_returning_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(reverse('payment'))
        else:
            print('FORM INVALID')
            return redirect(reverse('identification'))

def continue_as_guest(request):
    if request.method == 'POST':
        form = OrderEmail(request.POST)
        if form.is_valid():
            request.session['email'] = form.cleaned_data
            return redirect(reverse('payment'))

        else:
            return redirect(reverse('identification'))
