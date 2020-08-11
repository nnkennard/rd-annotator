from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from .models import SuperNode, Question

def index(request):
    supernode_list = SuperNode.objects.all()
    template = loader.get_template('annotate/index.html')
    context = {"supernode_list": supernode_list,}
    return HttpResponse(template.render(context, request))

def detail(request, supernode_id):
    supernode = SuperNode.objects.get(comment_id=supernode_id)
    questions = Question.objects.all()
    relevant_questions = [q for q in questions if q.span.super_node.id ==
            supernode_id]
    context = {"tokens": supernode.tokens,
            "questions": relevant_questions}
    template = loader.get_template('annotate/question.html')
    return HttpResponse(template.render(context, request))

# Create your views here.
