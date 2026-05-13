import os
import sys
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
sys.path.insert(0, "/c/Users/DELL/Downloads/archit")
django.setup()

# Run migrations
from django.core.management import call_command

call_command("makemigrations")
call_command("migrate")

print("\n✅ Migrations completed successfully!")
