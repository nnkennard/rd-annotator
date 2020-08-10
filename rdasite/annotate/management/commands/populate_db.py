from django.core.management.base import BaseCommand
from annotate.models import *

class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _create_tags(self):
        print("Hi")

    def handle(self, *args, **options):
        self._create_tags()
