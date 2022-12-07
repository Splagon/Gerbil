from django.core.management.base import BaseCommand, CommandError
from lessons.models import User, Term, Request, Adult


class Command(BaseCommand):
    def handle(self, *args, **options):
        User.objects.all().delete()
        Adult.objects.all().delete()
        Term.objects.all().delete()
        Request.objects.all().delete()
        print("Unseeding complete.")
