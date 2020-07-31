import datetime

from django.db import models
from django_mysql.models import ListCharField
from django.utils import timezone


class Annotation(models.Model):
    class Meta:
        app_label = "qa_annotate"
    span_type = models.IntegerField()

    chunk_idx = models.IntegerField()
    string = models.CharField(max_length=1000)

    error_code = models.IntegerField()
    comment = models.CharField(max_length=400)
    
class Example(models.Model):
    class Meta:
        app_label = "qa_annotate"
    parent_comment_id = models.CharField(max_length=20)
    child_comment_id = models.CharField(max_length=20)
    parent_chunk_idx = models.IntegerField()
    child_chunk_idx = models.IntegerField(null=True)

    maybe_question_text = models.CharField(max_length=500, null=True)

    question_annotation = Annotation()
    answer_annotation = Annotation()

    annotated = models.BooleanField()

class Chunk(models.Model):
    class Meta:
        app_label = "qa_annotate"
    comment_id = models.CharField(max_length=20)
    chunk_idx = models.IntegerField()
    chunk_tokens = ListCharField(
        base_field=models.CharField(max_length=30),
        size=500,
        max_length=(500 * 31)  # 6 * 10 character nominals, plus commas
    )

    def __str__(self):
        return " ".join([self.comment_id, str(self.chunk_idx)])
