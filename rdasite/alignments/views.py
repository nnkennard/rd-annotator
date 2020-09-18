from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from .models import AlignmentAnnotation, AnnotatedPair, Text

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

    return [" ".join(chunk_tokens) for chunk_tokens in chunks]

        

def detail(request, review_supernote, rebuttal_supernote):
    review_text = crunch_supernote(review_supernote)
    rebuttal_text = crunch_supernote(rebuttal_supernote)[0]

    context = {"review": review_text,
            "rebuttal": rebuttal_text}
    template = loader.get_template('alignments/detail.html')
    return HttpResponse(template.render(context, request))

#
