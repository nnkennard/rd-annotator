import json

from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from .models import AlignmentAnnotation, AnnotatedPair, Text
from .forms import AnnotationForm

def index(request):
    pair_list = AnnotatedPair.objects.all()
    examples = []
    for obj in pair_list:
        temp = dict(obj.__dict__)
        del temp["_state"]
        temp["previous_annotators"] =  ", ".join(sorted(set(x["annotator"] for x in AlignmentAnnotation.objects.values("annotator").filter(
                review_supernote=temp["review_supernote"],
                rebuttal_supernote=temp["rebuttal_supernote"],
                ).values())))
        print(temp)
        examples.append(temp)
    template = loader.get_template('alignments/index.html')
    context = {"examples": examples,}
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
            "rebuttal": rebuttal_text,
            "review_supernote": review_supernote,
            "rebuttal_supernote": rebuttal_supernote}
    template = loader.get_template('alignments/detail.html')
    return HttpResponse(template.render(context, request))

def submitted(request):
    template = loader.get_template('alignments/submitted.html')
    form = AnnotationForm(request.POST)
    if form.is_valid():
        annotation_obj = json.loads(form.cleaned_data["annotation"])
        for rebuttal_chunk_idx, review_chunk_map in annotation_obj["alignments"].items():
            print(review_chunk_map.values())
            label = "|".join(review_chunk for review_chunk, val in review_chunk_map.items() if val == True)
            print(label)
            if label:
                annotation = AlignmentAnnotation(
                        review_supernote = annotation_obj["review_supernote"],
                        rebuttal_supernote = annotation_obj["rebuttal_supernote"],
                        rebuttal_chunk = int(rebuttal_chunk_idx),
                        annotator = annotation_obj["annotator"],
                        label = label,
                        comment = annotation_obj["comments"],
                        review_chunking_error = rebuttal_chunk_idx in annotation_obj["errors"]["review_errors"],
                        rebuttal_chunking_error = rebuttal_chunk_idx in annotation_obj["errors"]["rebuttal_errors"],
                        )
                annotation.save()
    print(form.is_valid())
    print(form.cleaned_data)
    context = {}
    return HttpResponse(template.render(context, request))
