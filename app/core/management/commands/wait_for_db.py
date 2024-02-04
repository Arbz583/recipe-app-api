"""
Django command to wait for the database to be available.
"""
import time

from psycopg2 import OperationalError as Psycopg2OpError

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for database."""

    def handle(self, *args, **options):
        """Entrypoint for command."""
        self.stdout.write('Waiting for database...')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))

#  the check method is responsible for performing pre-execution checks (include database availablity), and if any errors are detected during these checks, the handle method will not be called.
# if check method fail then project stops but if handle method fail not!
# in testing we use mocked check method not real one!
# While multiple invocations of the check method are reasonable, it's essential to ensure that these checks do not have side effects that impact the execution of subsequent commands
