from django.conf import settings
from django.shortcuts import render, redirect
from ..models import MailOrder

def profile(request):
    if request.user.is_authenticated():
        orders = MailOrder.objects.filter(user=request.user)
        return render(request, 'profile.html', {'orders': orders})
    else:
        return redirect('/login')
