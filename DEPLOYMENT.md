# Course Hub - Deployment & Installation Guide

## Installation

### 1. Clone/Setup Repository
```bash
cd archit
source venv/Scripts/activate
```

### 2. Install Dependencies
```bash
pip install django pillow  # Already done
```

### 3. Apply Migrations
```bash
python manage.py migrate
```

### 4. Create Superuser
```bash
python manage.py createsuperuser
```

### 5. Run Server
```bash
python manage.py runserver
```

## Production Deployment

### Settings Changes Required
Edit `myproject/settings.py`:

```python
# Production settings
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
SECRET_KEY = 'your-secret-key'  # Change this!

# Use production database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'coursehub',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Static files
STATIC_ROOT = '/path/to/static'
MEDIA_ROOT = '/path/to/media'
```

### Deploy with Gunicorn
```bash
pip install gunicorn
gunicorn myproject.wsgi:application --bind 0.0.0.0:8000
```

### Use with Nginx
Configure Nginx to proxy requests to Gunicorn.

## Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.13
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
RUN python manage.py migrate
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]
```

Build and run:
```bash
docker build -t coursehub .
docker run -p 8000:8000 coursehub
```

## Security Checklist

- [ ] Change SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Use HTTPS/SSL
- [ ] Set secure cookies: SESSION_COOKIE_SECURE = True
- [ ] Configure CSRF_COOKIE_SECURE = True
- [ ] Setup proper database backups
- [ ] Use environment variables for secrets

## Features Checklist

- [x] User authentication with roles
- [x] Course creation & management
- [x] Student enrollments
- [x] Review system
- [x] Search & filters
- [x] Bootstrap UI
- [x] Admin panel
- [x] Form validation
- [x] Error handling

## Testing

```bash
python manage.py test

# Or test specific app
python manage.py test users
python manage.py test courses
```

## Troubleshooting

###404 Templates
- Ensure templates/ directory exists in project root
- Check TEMPLATES[DIRS] in settings.py

### Image Uploads Not Working
- Create media/ directory
- Check MEDIA_URL and MEDIA_ROOT in settings.py

### Database Errors
- Run migrations: `python manage.py migrate`
- Check database connection

### User Model Errors
- Ensure AUTH_USER_MODEL = 'users.User' in settings.py
- Clear migrations if custom User model not recognized

## Performance Optimization

1. **Database Queries:**
```python
# Use select_related for ForeignKeys
Course.objects.select_related('instructor', 'category').all()

# Use prefetch_related for reverse relations
User.objects.prefetch_related('courses').all()
```

2. **Caching:**
```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 5)  # Cache for 5 minutes
def course_list(request):
    ...
```

3. **Static Files:**
```bash
python manage.py collectstatic
```

## Backup & Recovery

```bash
# Export database
python manage.py dumpdata > backup.json

# Restore database
python manage.py loaddata backup.json

# Backup media files
tar -czf media_backup.tar.gz media/
```

## Support & Documentation

- Django: https://docs.djangoproject.com/
- Bootstrap: https://getbootstrap.com/
- Pillow (Images): https://pillow.readthedocs.io/
