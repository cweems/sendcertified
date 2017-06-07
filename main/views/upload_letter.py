from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse

from ..forms import DocumentUploader

def upload_letter(request):
    print('endpoint hit')
    form = DocumentUploader(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            request.session['pdf_url'] = form.cleaned_data
            return redirect(reverse('identification'))
