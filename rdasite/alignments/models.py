from django.db import models

# Create your models here.

class AlignmentAnnotation(models.Model):
    class Meta:
        app_label = "alignments"
    review_supernote = models.CharField(max_length=30)
    rebuttal_supernote = models.CharField(max_length=30)
    rebuttal_chunk = models.IntegerField()
    label = models.CharField(max_length=30)
    comment = models.CharField(max_length=200)
    annotator = models.CharField(max_length=30)
    review_chunking_error = models.BooleanField(default=False)
    rebuttal_chunking_error = models.BooleanField(default=False)
   
class AnnotatedPair(models.Model):
    class Meta:
        app_label = "alignments"
    review_supernote = models.CharField(max_length=30)
    rebuttal_supernote = models.CharField(max_length=30)
    status = models.IntegerField()
    title = models.CharField(max_length=300)
    reviewer = models.CharField(max_length=30)

class Text(models.Model):
    class Meta:
        app_label = "alignments"
    comment_supernote = models.CharField(max_length=30)
    chunk_idx = models.IntegerField()
    sentence_idx = models.IntegerField()
    token_idx = models.IntegerField()
    token = models.CharField(max_length=30)
    

class Statuses(models.Model):
    class Meta:
        app_label = "alignments"
    UNANNOTATED = 0
    PARTIALLY_ANNOTATED = 1
    COMPLETE = 2
    ERROR = 3
