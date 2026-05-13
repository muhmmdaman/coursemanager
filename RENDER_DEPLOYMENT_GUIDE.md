# Deploying Course Hub to Render - Complete Guide

## Step 1: Prepare Your Project

### 1.1 Update requirements.txt
Your project needs a proper `requirements.txt` with all dependencies:

```bash
Django==4.2.11
Pillow==11.0.0
gunicorn==21.2.0
python-decouple==3.8
```

### 1.2 Create a runtime.txt
Tell Render which Python version to use:

```
python-3.11.7
```

Save as `runtime.txt` in your project root.

### 1.3 Update settings.py for Production

Add/modify these in `myproject/settings.py`:

```python
import os
from pathlib import Path

# ... existing code ...

# Allow Render domain
ALLOWED_HOSTS = ['*']  # Or specify: ['coursemanager.onrender.com']

# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Database (SQLite will work for now, upgrade to PostgreSQL later)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Security
DEBUG = os.getenv('DEBUG', 'False') == 'True'
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here-change-in-production')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### 1.4 Create build.sh

Create `build.sh` in your project root:

```bash
#!/bin/bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
```

Make it executable:
```bash
chmod +x build.sh
```

### 1.5 Update wsgi.py

Make sure `myproject/wsgi.py` looks like this:

```python
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

application = get_wsgi_application()
```

## Step 2: Push to GitHub

Commit and push these changes:

```bash
git add build.sh runtime.txt RENDER_DEPLOYMENT_GUIDE.md
git commit -m "Add Render deployment configuration"
git push origin master
```

## Step 3: Create Render Account & Deploy

### 3.1 Go to Render
Visit https://render.com and sign up with your GitHub account.

### 3.2 Create New Web Service
1. Click **"+ New"** → **"Web Service"**
2. Select your GitHub repository `muhmmdaman/coursemanager`
3. Choose a name (e.g., `coursemanager`)
4. Select **Python 3** as the environment

### 3.3 Configure Build & Start Commands

**Build Command:**
```bash
./build.sh
```

**Start Command:**
```bash
gunicorn myproject.wsgi:application --bind 0.0.0.0:$PORT
```

### 3.4 Add Environment Variables

Click **"Advanced"** → **"Add Environment Variable"**

Add these:

| Key | Value |
|-----|-------|
| `PYTHON_VERSION` | `3.11.7` |
| `DEBUG` | `False` |
| `SECRET_KEY` | (Generate one: https://djecrety.ir) |

## Step 4: Deploy

1. Click **"Create Web Service"**
2. Render will automatically deploy your app
3. Wait for the build to complete (3-5 minutes)
4. Your app will be live at: `https://coursemanager.onrender.com`

## Step 5: Verify Deployment

1. Visit your Render URL
2. Check the logs if there are issues: **Logs** tab in Render dashboard
3. Test key features:
   - View homepage
   - Try login
   - Browse courses

## Step 6: Set Up Database (PostgreSQL - Optional but Recommended)

For production, use PostgreSQL instead of SQLite:

### 6.1 Create PostgreSQL Database on Render

1. In Render dashboard, click **"+ New"** → **"PostgreSQL"**
2. Enter name and region
3. Copy the **Internal Database URL**

### 6.2 Update settings.py

```python
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600
    )
}
```

### 6.3 Install dj-database-url

Add to `requirements.txt`:
```
dj-database-url==2.1.0
```

### 6.4 Add Environment Variable in Render

1. In Web Service settings → **Environment**
2. Add `DATABASE_URL` = (paste the PostgreSQL internal URL from Step 6.1)
3. Click **"Save"** and Render will redeploy

## Troubleshooting

### Build Failed
- Check the **Build Logs** in Render
- Common issues:
  - Missing `requirements.txt`
  - Python version mismatch
  - Syntax errors in settings.py

### Static Files Not Loading
- Run: `python manage.py collectstatic --no-input`
- Check `STATIC_ROOT` and `STATIC_URL` in settings.py

### 502 Bad Gateway
- Check **Logs** tab
- Verify `gunicorn` start command
- Check environment variables

### Database Issues
- If using SQLite, make sure migrations are run via `build.sh`
- For PostgreSQL, verify `DATABASE_URL` format

## Next Steps

1. ✅ Deploy to Render
2. Set up custom domain (optional)
3. Enable HTTPS (automatic on Render)
4. Monitor logs regularly
5. Plan upgrades (PostgreSQL, static storage service)

---

**Need help?**
- Render Docs: https://render.com/docs
- Django Deployment: https://docs.djangoproject.com/en/4.2/howto/deployment/
