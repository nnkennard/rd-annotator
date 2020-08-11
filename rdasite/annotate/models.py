from django.db import models
from django_mysql.models import ListCharField

class SuperNode(models.Model):
    class Meta:
        app_label = "annotate"
    comment_id = models.CharField(max_length=30)
    tokens = ListCharField(
        base_field=models.CharField(max_length=25),
        size=1000,
        max_length=1000 * 26)  # 6 * 10 character nominals, plus commas

class Span(models.Model):
    class Meta:
        app_label = "annotate"
    super_node = models.ForeignKey(SuperNode, on_delete=models.CASCADE)
    span_start = models.IntegerField()
    span_exclusive_end = models.IntegerField()

class Annotation(models.Model):
    class Meta:
        app_label = "annotate"
    error_code = models.IntegerField()
    comment = models.CharField(max_length=400)

class Question(models.Model):
    class Meta:
        app_label = "annotate"
    span = models.ForeignKey(Span, on_delete=models.CASCADE)
    annotation = Annotation()

class Answer(models.Model):
    class Meta:
        app_label = "annotate"
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    span = models.ForeignKey(Span, on_delete=models.CASCADE)
    annotation = Annotation()

class QAPair(models.Model):
    class Meta:
        app_label = "annotate"
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

