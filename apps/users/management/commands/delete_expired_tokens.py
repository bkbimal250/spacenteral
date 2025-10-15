"""
Management command to delete expired authentication tokens
Run this as a cron job to clean up old tokens
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from rest_framework.authtoken.models import Token


class Command(BaseCommand):
    help = 'Delete authentication tokens older than specified days'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=7,
            help='Delete tokens older than this many days (default: 7)',
        )

    def handle(self, *args, **options):
        days = options['days']
        cutoff_date = timezone.now() - timedelta(days=days)
        
        # Delete tokens older than cutoff date
        deleted_count, _ = Token.objects.filter(created__lt=cutoff_date).delete()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully deleted {deleted_count} tokens older than {days} days'
            )
        )

