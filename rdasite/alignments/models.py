from django.db import models

# Create your models here.

#{'forum_id': 'ryl8-3AcFX', 'split': 'train', 'parent_supernote': 'SkluH4n6nX', 'comment_supernote': 'SklMCmJ-aX', 'parent_author': 'AnonReviewer1', 'title': 'Environment Probing Interaction Policies'}

class AlignmentAnnotation(models.Model):
    class Meta:
        app_label = "alignments"
    review_supernote = models.CharField(max_length=30)
    rebuttal_supernote = models.CharField(max_length=30)
    rebuttal_chunk = models.IntegerField()
    label = models.CharField(max_length=30)
    comment = models.CharField(max_length=50)
   
class AnnotatedPair(models.Model):
    class Meta:
        app_label = "alignments"
    review_supernote = models.CharField(max_length=30)
    rebuttal_supernote = models.CharField(max_length=30)
    annotator = models.CharField(max_length=30)
    status = models.IntegerField()

class Text(models.Model):
    class Meta:
        app_label = "alignments"
    comment_supernote = models.CharField(max_length=30)
    chunk_idx = models.IntegerField()
    sentence_idx = models.IntegerField()
    token_idx = models.IntegerField()
    token = models.CharField(max_length=30)
    
