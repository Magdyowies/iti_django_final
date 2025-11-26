from django.core.management.base import BaseCommand
from users.models import User
from projects.models import Project
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Creates sample users and projects for development'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')

        # Create users
        user1 = User.objects.create_user(email='user1@example.com', password='password123', first_name='John', last_name='Doe', mobile_phone='01001234567')
        user1.is_active = True
        user1.save()
        user2 = User.objects.create_user(email='user2@example.com', password='password123', first_name='Jane', last_name='Smith', mobile_phone='01101234567')
        user2.is_active = True
        user2.save()

        self.stdout.write(self.style.SUCCESS(f'Created users: {user1.email}, {user2.email}'))

        # Create projects
        Project.objects.create(
            owner=user1,
            title='First Project by John',
            details='This is the first project details by John.',
            target_amount=5000,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30),
        )
        Project.objects.create(
            owner=user1,
            title='Second Project by John',
            details='Another project by John, a bit longer.',
            target_amount=10000,
            start_date=date.today() + timedelta(days=5),
            end_date=date.today() + timedelta(days=60),
        )
        Project.objects.create(
            owner=user2,
            title='Project by Jane',
            details='Jane\'s amazing project.',
            target_amount=7500,
            start_date=date.today() - timedelta(days=10),
            end_date=date.today() + timedelta(days=20),
        )

        self.stdout.write(self.style.SUCCESS('Successfully created sample projects.'))
        self.stdout.write(self.style.SUCCESS('Sample data creation complete.'))
