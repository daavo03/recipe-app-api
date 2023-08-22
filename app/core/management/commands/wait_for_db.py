"""
Django command to wait for the DB to be available.
"""

import time
from psycopg2 import OperationalError as Psycopg2OpError
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Django command to wait for database.
    """

    # This is the standard syntax for any command the handle method gets called
    # when you run your django command
    def handle(self, *args, **options):
        """
        Entrypoint for command
        """

        # stdout we can use to log things to the screen as our command is executing
        self.stdout.write('Waiting for database...')

        # Assuming the DB is not up
        db_up = False
        while db_up is False:
            try:
                # If we call this and the DB isn't ready throws an exception
                self.check(databases=["default"])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write("Database unavailable waiting 1 second...")
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS("Database available!"))
