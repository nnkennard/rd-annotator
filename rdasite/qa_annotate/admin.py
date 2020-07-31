from django.contrib import admin

from .models import Example, Chunk, Annotation

admin.site.register(Chunk)
admin.site.register(Example)
admin.site.register(Annotation)
