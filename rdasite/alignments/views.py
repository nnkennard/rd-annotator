from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from .models import AlignmentAnnotation, AnnotatedPair, Text
from .forms import AnnotationForm

def index(request):
    pair_list = AnnotatedPair.objects.all()
    template = loader.get_template('alignments/index.html')
    context = {"pair_list": pair_list,}
    return HttpResponse(template.render(context, request))


def crunch_supernote(supernote):
    rows = Text.objects.filter(comment_supernote=supernote)
    chunks = []
    current_chunk = []
    current_chunk_idx = 0
    for row in rows:
        if current_chunk_idx == row.chunk_idx:
            current_chunk.append(row.token)
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = [row.token]
            current_chunk_idx = row.chunk_idx
    if current_chunk:
        chunks.append(current_chunk)

    return [" ".join(chunk_tokens) for chunk_tokens in chunks]

        

def detail(request, review_supernote, rebuttal_supernote):
    review_text = crunch_supernote(review_supernote)
    rebuttal_text = crunch_supernote(rebuttal_supernote)
    title = AnnotatedPair.objects.get(
            review_supernote=review_supernote,
            rebuttal_supernote=rebuttal_supernote
            ).title
    context = {
            "paper_title":title,
            "review": review_text,
            "rebuttal": rebuttal_text}
    template = loader.get_template('alignments/detail.html')
    return HttpResponse(template.render(context, request))

def submitted(request):
    template = loader.get_template('alignments/submitted.html')
    form = AnnotationForm(request.POST)
    print(form.is_valid())
    print(form.cleaned_data)
    context = {}
    return HttpResponse(template.render(context, request))
