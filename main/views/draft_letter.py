from django.shortcuts import render, redirect
from django.urls import reverse
from ..forms import DocumentEditor, DocumentUploader

def draft_letter(request):
    initial = {'letter': request.session.get('letter', None)}
    letter = initial['letter']
    form = DocumentEditor(request.POST or None, initial=letter)
    pdf_uploader = DocumentUploader()

    if request.method == 'POST':
        if form.is_valid():
            request.session['letter'] = form.cleaned_data
            return redirect(reverse('identification'))
    return render(request, 'orderform/draft_letter.html', {'form': form, 'pdf_uploader': pdf_uploader})
