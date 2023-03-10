from students.models import Student
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    def add_arguments(self, parser) -> None:
        parser.add_argument("-u", "--username", type=str, default="userBanned")
        parser.add_argument("-p", "--password", type=str, default="userBanned123")
        parser.add_argument("-e", "--email", type=str)
        parser.add_argument("-i", "--is_banned", type=bool, default=True)

    def handle(self, *args, **kwargs):
        username = kwargs["username"]
        password = kwargs["password"]
        email = kwargs["email"]
        is_banned = kwargs["is_banned"]

        if email:
            email = email
        else:
            email = f"{username}@example.com"

        if Student.objects.filter(username=username):
            raise CommandError(f"Username `{username}` already taken.")
        if Student.objects.filter(email=email):
            raise CommandError(f"Email `{email}` already taken.")

        Student.objects.create_superuser(
            username=username, email=email, password=password, is_banned=is_banned
        )

        self.stdout.write(
            self.style.SUCCESS(f"Banned User `{username}` successfully created!")
        )
