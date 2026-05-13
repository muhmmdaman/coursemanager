#!/bin/bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Load sample data if not already loaded
python manage.py shell << EOF
from django.contrib.auth import get_user_model
from courses.models import Category

User = get_user_model()

# Only seed if database is empty
if User.objects.filter(username='admin').exists():
    print("✓ Database already seeded, skipping...")
else:
    print("🌱 Loading sample data...")
    exec(open('seed_data.py').read())
    print("✓ Sample data loaded!")
EOF
