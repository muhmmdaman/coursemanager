# Render Deployment - Quick Reference Card

## 🚀 TL;DR - Just Do This:

1. Go to https://render.com → Sign up with GitHub
2. Click **+ New → Web Service**
3. Select `muhmmdaman/coursemanager` repo
4. **Build Command:** `./build.sh`
5. **Start Command:** `gunicorn myproject.wsgi:application --bind 0.0.0.0:$PORT`
6. **Add Environment Variables:**
   - `DEBUG` = `False`
   - `SECRET_KEY` = (from https://djecrety.ir)
   - `ALLOWED_HOSTS` = `*`
7. Click **Create Web Service**
8. Wait 3-5 minutes
9. Open your URL → Login with `admin` / `admin123`

---

## 📋 Exact Settings to Enter

### Build Command (Copy-Paste):
```
./build.sh
```

### Start Command (Copy-Paste):
```
gunicorn myproject.wsgi:application --bind 0.0.0.0:$PORT
```

### Environment Variables:

| Key | Value |
|-----|-------|
| DEBUG | False |
| SECRET_KEY | [Generate here](https://djecrety.ir) |
| ALLOWED_HOSTS | * |

---

## 🔑 Test Credentials

| User | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |
| Instructor | instructor1 | instructor123 |
| Student | student1 | student123 |

---

## ⚠️ Free Plan Notes

- ⏰ **Sleeps after 15 min** of inactivity (wakes in ~30 sec)
- 💾 **SQLite database** (data resets on redeploy, OK for now)
- 🖥️ **512 MB RAM** (sufficient for testing)
- 📊 **No custom domain** (you get render subdomain)

---

## 🐛 If Something Goes Wrong

1. **Go to Logs tab** on your Render service
2. **Look for red error messages**
3. **Common fixes:**
   - `502 error` → Wait 2 min, refresh
   - `Build failed` → Check requirements.txt
   - `Static files broken` → Refresh page (Ctrl+F5)

---

## ✅ Verification Checklist

After deployment completes:

- [ ] Visit your Render URL (looks like: `https://coursemanager.onrender.com`)
- [ ] Homepage loads
- [ ] Click "Login"
- [ ] Enter: `admin` / `admin123`
- [ ] Dashboard appears
- [ ] Browse courses
- [ ] View a course detail
- [ ] Visit `/admin` - Admin panel works

---

## 📝 Notes

- Render auto-redeploys when you push to GitHub
- Changes take 2-3 minutes to appear
- Free plan is perfect for learning and testing
- Upgrade to paid if you need: custom domain, persistent DB, more resources
