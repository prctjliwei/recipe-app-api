"""
Django command to wait for the databae to be acailable
"""
    
from typing import Any
import time
from django.core.management.base import BaseCommand
from pyscopg2 import OperationalError as Pyscopg2OpError
from django.db.utils import OperationalError

class Command(BaseCommand):
    """Django command to wait for database."""
    def handle(self, *args, **options):
        """Enterypoint for commands"""
        self.stdout.write('Waiting for database...')
        db_up = False
        while db_up is False:
            try:
                self.check(dataases=["dafault"])
                db_up = True
            except (Pyscopg2OpError, OperationalError):
                self.stdout.write("Database unavailable, waiting 1 sec...")
                time.sleep(1)
                
        self.stdout.write(self.style.SUCCESS("Database available!"))