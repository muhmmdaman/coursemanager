# VENV INSTALLATION - QUICK REFERENCE

## ✅ Installation Complete!

All 28 packages are now installed in your virtual environment.

---

## 🚀 To Start Using the Application

### Step 1: Activate Virtual Environment
```bash
.\venv\Scripts\activate
```
You should see `(venv)` at the start of your command prompt.

### Step 2: Run the Server
```bash
python manage.py runserver
```

### Step 3: Open in Browser
```
http://127.0.0.1:8000/
```

### Step 4: Login
- **Admin:** admin / admin123
- **Instructor:** instructor1 / instructor123
- **Student:** student1 / student123

---

## 📦 What's Installed (28 packages)

| Package | Version | Purpose |
|---------|---------|---------|
| Django | 4.2.11 | Web framework |
| Pillow | 11.0.0 | Image processing |
| gunicorn | 21.2.0 | Production server |
| whitenoise | 6.12.0 | Static files |
| django-crispy-forms | 2.3 | Forms |
| crispy-bootstrap5 | 2026.3 | Bootstrap UI |
| djangorestframework | 3.14.0 | REST API |
| pytest | 9.0.2 | Testing |
| pytest-django | 4.12.0 | Django testing |
| django-extensions | 4.1 | Admin tools |
| psycopg2-binary | 2.9.10 | PostgreSQL |
| + 16 more dependencies | - | Support packages |

---

## 🛠️ Useful Commands

```bash
# Verify venv is active
where python  (Windows)
which python  (macOS/Linux)

# Check Django
python -c "import django; print(django.VERSION)"

# See all packages
pip list

# Reinstall packages
pip install -r requirements-venv.txt

# Run tests
pytest

# Collect static files
python manage.py collectstatic

# Access Django shell
python manage.py shell

# Create new admin
python manage.py createsuperuser

# Deactivate venv (when done)
deactivate
```

---

## ✅ Verification

All systems are verified and working:
- ✅ Virtual environment active
- ✅ 28 packages installed
- ✅ Django 4.2.11 verified
- ✅ Database connected
- ✅ Server tested
- ✅ Admin accessible
- ✅ 0 system issues

---

## 📁 Requirements Files

**requirements-venv.txt** - Use this one!
- 26 essential packages for Course Hub
- Install with: `pip install -r requirements-venv.txt`

**requirements.txt** - Comprehensive
- 231+ packages including all development tools
- Install with: `pip install -r requirements.txt`

**requirements-minimal.txt** - Minimal
- Just Django and Pillow
- Install with: `pip install -r requirements-minimal.txt`

---

## ⚠️ Important

1. **Always activate venv** before working: `.\venv\Scripts\activate`
2. **Don't move the venv folder** - it's location-dependent
3. **Use `deactivate`** when you're finished working
4. **Use the venv's pip** - only install while venv is active

---

## 📊 Quick Status

```
Virtual Environment: ✅ READY
Packages: ✅ INSTALLED (28)
Django: ✅ 4.2.11
Server: ✅ WORKING
Database: ✅ CONNECTED
Tests: ✅ READY
Admin: ✅ ACCESSIBLE
```

---

**Everything is ready! You can start building now! 🚀**
