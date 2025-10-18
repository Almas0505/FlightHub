"""
Seed test users for FlightHub demo
Usage: python manage.py seed_users
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import UserProfile

User = get_user_model()


class Command(BaseCommand):
    help = 'Create test users with different loyalty tiers for demo'

    def handle(self, *args, **options):
        test_users = [
            {
                'email': 'demo@flighthub.com',
                'password': 'Demo123!',
                'first_name': 'Demo',
                'last_name': 'User',
                'phone': '+77001234567',
                'loyalty_tier': 'GOLD',
                'loyalty_points': 15000,
            },
            {
                'email': 'john.doe@example.com',
                'password': 'Test123!',
                'first_name': 'John',
                'last_name': 'Doe',
                'phone': '+77001234568',
                'loyalty_tier': 'PLATINUM',
                'loyalty_points': 50000,
            },
            {
                'email': 'jane.smith@example.com',
                'password': 'Test123!',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'phone': '+77001234569',
                'loyalty_tier': 'SILVER',
                'loyalty_points': 5000,
            },
            {
                'email': 'alex.brown@example.com',
                'password': 'Test123!',
                'first_name': 'Alex',
                'last_name': 'Brown',
                'phone': '+77001234570',
                'loyalty_tier': 'BRONZE',
                'loyalty_points': 500,
            },
            {
                'email': 'sarah.wilson@example.com',
                'password': 'Test123!',
                'first_name': 'Sarah',
                'last_name': 'Wilson',
                'phone': '+77001234571',
                'loyalty_tier': 'GOLD',
                'loyalty_points': 12000,
            },
        ]

        created_count = 0
        skipped_count = 0

        for user_data in test_users:
            email = user_data['email']
            
            if User.objects.filter(email=email).exists():
                self.stdout.write(
                    self.style.WARNING(f'User {email} already exists. Skipping.')
                )
                skipped_count += 1
                continue

            # Create user
            username = email.split('@')[0]  # Use email prefix as username
            user = User.objects.create_user(
                username=username,
                email=email,
                password=user_data['password'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                phone=user_data['phone'],
            )

            # Update user with loyalty data
            user.tier = user_data['loyalty_tier']
            user.loyalty_points = user_data['loyalty_points']
            user.email_notifications = True
            user.sms_notifications = True
            user.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Created user: {email} (Tier: {user_data["loyalty_tier"]}, Points: {user_data["loyalty_points"]})'
                )
            )
            created_count += 1

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(self.style.SUCCESS(f'Seed completed! Created: {created_count}, Skipped: {skipped_count}'))
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write('')
        self.stdout.write(self.style.WARNING('Test credentials for demo:'))
        self.stdout.write('  Email: demo@flighthub.com')
        self.stdout.write('  Password: Demo123!')
        self.stdout.write('')
