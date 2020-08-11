from django.core.management.base import BaseCommand
from annotate.models import *

import json

def clean_tokens(tokens):
    return [tok.replace(",", "COM") for tok in tokens]

class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'Given a json file, update database'

    def add_arguments(self, parser):
        parser.add_argument('input_file', type=str)

    def _load_data(self, input_file):
        with open(input_file, 'r') as f:
            return json.loads(f.read())

    def handle(self, *args, **options):
        print(SuperNode.objects.all())


        print(options["input_file"])
        json_obj = self._load_data(options["input_file"])
        for node in json_obj["nodes"]:
            super_node = SuperNode(
                    comment_id=node["node_id"],
                    tokens=clean_tokens(node["tokens"]))
            super_node.save()
        for question in json_obj["questions"]:
            super_node = SuperNode.objects.get(
                    comment_id=question["supnode_id"])
            span = Span(super_node=super_node,
            span_start=question["start"],
            span_exclusive_end=question["exclusive_end"])
            span.save()
            question = Question(span=span)
            question.save()
