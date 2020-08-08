import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.urls import reverse


from .models import Example, Chunk

Q_OPTIONS = ["No error", "Question spans multiple chunks",
        "Multiple questions present", "Answer not expected",
        "No question in vicinity", "Other (needs futher attention)"]

A_OPTIONS = ["No error", "Answer spans multiple chunks", "Answer not present",
        "Abstractive answer only", "Other (needs futher attention)"]

def format_tokens(tokens, question):
    dirty_text = " ".join(tokens)
    if question is not None:
        subs = dirty_text.find(question)
        if subs > -1:
            frags = dirty_text[:subs], dirty_text[subs:subs +
                    len(question)], dirty_text[subs+len(question):]
            dirty_text = frags[0] + "****" + frags[1] + "****" + frags[2]

    clean_text = dirty_text.replace("COM", ",").replace(
            "-LRB-", "(").replace(
            "-RRB-", ")").replace(
            "-LSB-", "[").replace(
            "-RSB-", "]")
    return dirty_text.split()


def dedup_chunks(chunks):
    seen_chunks = []
    seen_tokens = []
    for chunk in chunks:
        if chunk.chunk_tokens not in seen_tokens:
            seen_chunks.append(chunk)
            seen_tokens.append(chunk.chunk_tokens)
    return seen_chunks

def get_chunk_texts(comment_id, hl_idx, question=None):
    chunks = Chunk.objects.filter(comment_id=comment_id)
    deduped_chunks = dedup_chunks(chunks)
    return [format_tokens(chunk.chunk_tokens, question)
            for chunk in deduped_chunks]


def detail(request, example_id):
    try:
        example = Example.objects.get(pk=example_id)
        parent_text = get_chunk_texts(example.parent_comment_id,
                example.parent_chunk_idx, example.maybe_question_text)
        child_text = get_chunk_texts(example.child_comment_id,
                example.child_chunk_idx)
    except Example.DoesNotExist:
        raise Http404("Example does not exist")
    return render(request, 'qa_annotate/detail.html', {'example': example,
       'parent_chunks': json.dumps(parent_text), 'child_text':child_text,
        "q_options":Q_OPTIONS, "a_options":A_OPTIONS})

def results(request, question_id):
    example = get_object_or_404(Example, pk=example_id)
    return render(request, 'qa_annotate/results.html', {'example': example})

def index(request):
    example_list = Example.objects.all()
    template = loader.get_template('qa_annotate/index.html')
    context = {
        'example_list': example_list,
    }
    return HttpResponse(template.render(context, request))
