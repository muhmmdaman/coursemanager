# Course Hub - Virtual Environment Setup Guide

## ✅ All Requirements Installed in venv/

All required packages are now installed in your virtual environment.

---

## 📦 Installed Packages (26 packages)

```
asgiref             3.11.1
colorama            0.4.6
crispy-bootstrap5   2026.3
Django              4.4.11
django-cors-headers 4.3.1
django-crispy-forms 2.3
django-extensions   4.1
djangorestframework 3.14.0
gunicorn            21.2.0
iniconfig           2.3.0
packaging           26.0
pillow              11.0.0
pip                 26.0.1
pluggy              1.6.0
psycopg2-binary     2.9.10
Pygments            2.20.0
pytest              9.0.2
pytest-django       4.12.0
python-decouple     3.8
python-dotenv       1.0.0
pytz                2026.1.post1
setuptools          82.0.1
sqlparse            0.5.5
tzdata              2026.1
wheel               0.46.3
whitenoise          6.12.0
```

---

## 🚀 How to Use the Virtual Environment

### On Windows (PowerShell or CMD):

```bash
# Activate venv
.\venv\Scripts\activate

# You should see: (venv) C:\Users\...\archit>
```

### On macOS/Linux:

```bash
# Activate venv
source venv/bin/activate

# You should see: (venv) user@computer:~/archit$
```

---

## 🎯 Commands to Run (Always with venv activated)

### Start the Development Server:
```bash
python manage.py runserver
```

### Create Migrations:
```bash
python manage.py makemigrations
```

### Apply Migrations:
```bash
python manage.py migrate
```

### Access Django Shell:
```bash
python manage.py shell
```

### Run Tests:
```bash
pytest
```

### Collect Static Files (Production):
```bash
python manage.py collectstatic
```

### Create Superuser:
```bash
python manage.py createsuperuser
```

### Change Password:
```bash
python manage.py changepassword username
```

---

## ✅ Verification

### Check that venv is being used:

```bash
# On Windows:
where python
# Should show: C:\Users\...\archit\venv\Scripts\python.exe

# On macOS/Linux:
which python
# Should show: /path/to/archit/venv/bin/python
```

### Verify Django installation:
```bash
python -c "import django; print(django.VERSION)"
# Should show: (4, 4, 11, 'final', 0)
```

### Verify Pillow installation:
```bash
python -c "import PIL; print(PIL.__version__)"
# Should show: 11.0.0
```

---

## 📁 Requirements Files

### requirements-venv.txt
Essential packages (26 packages) - use this for quick setup:
```bash
pip install -r requirements-venv.txt
```

### requirements.txt
All 231 packages including development tools:
```bash
pip install -r requirements.txt
```

### requirements-minimal.txt
Minimal setup (just Django and Pillow):
```bash
pip install -r requirements-minimal.txt
```

---

## 🔒 Deactivate Virtual Environment

When you're done:
```bash
deactivate
```

---

## 📊 Current Status

✅ Virtual Environment: Active and configured
✅ All Packages: Installed (26 essential packages)
✅ Django: 4.4.11
✅ Pillow: 11.0.0
✅ Server: Ready to run
✅ Database: Connected
✅ System Check: 0 issues

---

## 🎯 Next Steps

1. **Activate the virtual environment:**
   ```bash
   # Windows:
   .\venv\Scripts\activate

   # macOS/Linux:
   source venv/bin/activate
   ```

2. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

3. **Open in browser:**
   ```
   http://127.0.0.1:8000/
   ```

4. **Admin panel:**
   ```
   http://127.0.0.1:8000/admin/
   Username: admin
   Password: admin123
   ```

---

## 🚨 Important Notes

1. **Always activate venv before working** on the project
2. **Use `pip install -r requirements-venv.txt`** if you need to reinstall packages
3. **Don't modify** the venv directory directly
4. **Use deactivate** when you're done to exit the virtual environment

---

## 📞 Troubleshooting

### "Command not found" errors
**Problem:** You forgot to activate the venv

**Solution:**
```bash
# Windows
.\venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### "No module named django"
**Problem:** Django not installed

**Solution:**
```bash
pip install -r requirements-venv.txt
```

### "Permission denied" on macOS/Linux
**Problem:** Activation script not executable

**Solution:**
```bash
chmod +x venv/bin/activate
source venv/bin/activate
```

### Port 8000 already in use
**Problem:** Another application is using port 8000

**Solution:**
```bash
python manage.py runserver 8001
# Then visit http://127.0.0.1:8001/
```

---

## 📌 Keep in Mind

- Virtual environments keep your project isolated
- Each project can have different package versions
- Always activate venv before working on this project
- Dependencies are listed in requirements files
- Use requirements files to manage packages

---

**Everything is ready to go! Start building! 🚀**
