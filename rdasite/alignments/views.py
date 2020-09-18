from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from .models import AlignmentAnnotation, AnnotatedPair

def index(request):
    pair_list = AnnotatedPair.objects.all()
    template = loader.get_template('alignments/index.html')
    context = {"pair_list": pair_list,}
    return HttpResponse(template.render(context, request))


def crunch_supernote(supernote):
    rows = Text.objects.get(comment_supernote=supernote)

def detail(request, review, rebuttal):
    review_text = crunch_supernote(review)
    rebuttal_text = crunch_supernote(rebuttal)

    context = {"review": supernode.tokens,
            "rebuttal": relevant_questions}
    template = loader.get_template('alignments/pair.html')
    return HttpResponse(template.render(context, request))

#
