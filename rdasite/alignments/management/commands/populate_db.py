from django.core.management.base import BaseCommand
from alignments.models import *

import json
from tqdm import tqdm

class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'Given a json file, update database for alignments'

    def add_arguments(self, parser):
        parser.add_argument('input_file', type=str)

    def _load_data(self, input_file):
        with open(input_file, 'r') as f:
            return json.loads(f.read())

    def handle(self, *args, **options):
        json_obj = self._load_data(options["input_file"])

        #for text_row in tqdm(json_obj["text"]):
        #    textnode = Text(
        #            comment_supernote=text_row["comment_supernote"],
        #            chunk_idx=int(text_row["chunk_idx"]),
        #            sentence_idx=int(text_row["sentence_idx"]),
        #            token_idx=int(text_row["token_idx"]),
        #            token=text_row["token"],
        #            )
        #    textnode.save()

        AnnotatedPair.objects.all().delete()
        AlignmentAnnotation.objects.all().delete()

        for node in json_obj["metadata"][:10]:
            rebuttal_chunk_maps = Text.objects.values(
                "chunk_idx").filter(
                comment_supernote=node["comment_supernote"]).distinct()
            num_rebuttal_chunks = max(x["chunk_idx"]
                    for x in rebuttal_chunk_maps) + 1
            for i in range(num_rebuttal_chunks):
                annotation = AlignmentAnnotation(
                        review_supernote = node["parent_supernote"],
                        rebuttal_supernote = node["comment_supernote"],
                        rebuttal_chunk = i,
                        label = "",
                        comment = ""
                        )
                annotation.save()
            print(node.keys())
            annotated_pair = AnnotatedPair(
                review_supernote = node["parent_supernote"],
                rebuttal_supernote = node["comment_supernote"],
                annotator="", 
                status=Statuses.UNANNOTATED,
                title=node["title"],
                reviewer=node["parent_author"]
                    )
            annotated_pair.save()
            

        
