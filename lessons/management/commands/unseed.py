from django.core.management.base import BaseCommand, CommandError
from lessons.models import User, Term


class Command(BaseCommand):
    def handle(self, *args, **options):
        User.objects.filter(is_staff=False, is_superuser=False).delete()
        Term.objects.all().delete()
        print("Unseeding complete.")
