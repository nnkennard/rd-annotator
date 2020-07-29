import datetime

from django.db import models
from django_mysql.models import ListCharField
from django.utils import timezone


class Question(models.Model):
    class Meta:
        app_label = "qa_annotate"
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    class Meta:
        app_label = "qa_annotate"
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Candidate(models.Model):
    class Meta:
        app_label = "qa_annotate"
    parent_chunk_idx = models.IntegerField()
    child_chunk_idx = models.IntegerField()
    maybe_question_text = models.CharField(max_length=500)


class Example(models.Model):
    class Meta:
        app_label = "qa_annotate"
    parent_id = models.CharField(max_length=20)
    child_id = models.CharField(max_length=20)

    parent_chunks = ListCharField(
        base_field=models.CharField(max_length=2000),
        size=10,
        max_length=(10 * 2001)  # 6 * 10 character nominals, plus commas
    )
    child_chunks = ListCharField(
        base_field=models.CharField(max_length=2000),
        size=10,
        max_length=(10 * 2001)  # 6 * 10 character nominals, plus commas
    )

