# Deploy Course Hub to Render - Complete Step-by-Step Guide (Free Plan)

## ⚠️ Important Notes About Free Plan
- **Sleep after 15 minutes of inactivity** (auto-wakes on request, takes ~30 seconds)
- **Limited resources**: 0.5 CPU, 512 MB RAM
- **SQLite Database**: Works fine for learning/testing
- **Static files**: Handled by WhiteNoise
- **Outbound bandwidth**: Limited but sufficient for course marketplace
- **No custom domain initially**: You get a Render subdomain

---

## Step 1: Create Render Account

1. Go to **https://render.com**
2. Click **"Sign up"** → Choose **"Sign up with GitHub"**
3. **Authorize** Render to access your GitHub account
4. Click **"Authorize render-examples"** when prompted
5. You're now logged into Render dashboard

---

## Step 2: Create Web Service

1. In Render dashboard, click **"+ New +"** button (top right)
2. Select **"Web Service"**
3. You'll see a list of your GitHub repositories
4. **Find & select**: `muhmmdaman/coursemanager`
5. Click **"Connect"**

---

## Step 3: Configure Web Service Settings

### 3.1 Basic Information

**Fill in these fields:**

| Field | Value |
|-------|-------|
| **Name** | `coursemanager` |
| **Environment** | `Python 3` |
| **Region** | `Oregon` (or closest to you) |
| **Branch** | `master` |

### 3.2 Build & Start Commands

**Build Command:**
```bash
./build.sh
```

**Start Command:**
```bash
gunicorn myproject.wsgi:application --bind 0.0.0.0:$PORT
```

⚠️ **Important**: Make sure `build.sh` exists in your repo (✓ it does)

---

## Step 4: Add Environment Variables

1. Scroll down to **"Advanced"** section
2. Click **"Add Environment Variable"**

### Add these variables one by one:

**Variable 1:**
- **Key:** `DEBUG`
- **Value:** `False`
- Click **"Add"**

**Variable 2:**
- **Key:** `SECRET_KEY`
- **Value:** Go to https://djecrety.ir → Copy the generated key → Paste it
- Click **"Add"**

**Variable 3:**
- **Key:** `ALLOWED_HOSTS`
- **Value:** `*`
- Click **"Add"**

**Variable 4 (Optional for PostgreSQL later):**
- **Key:** `PYTHON_VERSION`
- **Value:** `3.11.7`
- Click **"Add"**

---

## Step 5: Review & Deploy

1. **Scroll to bottom** of the form
2. Verify all settings:
   - ✅ Build Command: `./build.sh`
   - ✅ Start Command: `gunicorn myproject.wsgi:application --bind 0.0.0.0:$PORT`
   - ✅ Environment Variables added
   - ✅ Python 3 selected

3. Click **"Create Web Service"**
4. **Wait 3-5 minutes** for deployment to complete

---

## Step 6: Monitor Deployment

1. You'll see a **"Deploys"** tab showing build progress
2. **Build stages** you'll see:
   - "Building Docker image..."
   - "Building image..."
   - "Pushing image..."
   - "Running migrations..."
   - "Running build script..."

3. **Wait for** "Your service is live!" message

---

## Step 7: Get Your URL

1. Once deployment is complete, look at the top
2. You'll see: `https://coursemanager.onrender.com` (or similar)
3. **Copy this URL** - that's your live app!

---

## Step 8: Test Your Deployment

### First test - Check if app loads:
1. **Open** your Render URL in browser
2. You should see the **Course Hub homepage**

### Test login:
- **Admin:** `admin` / `admin123`
- **Instructor:** `instructor1` / `instructor123`
- **Student:** `student1` / `student123`

### Test core features:
- ✅ Browse courses
- ✅ Login with test account
- ✅ View course details
- ✅ Check admin panel at `/admin`

---

## Step 9: Check Logs for Issues

If something goes wrong:

1. Go to your service on Render
2. Click **"Logs"** tab
3. Look for **error messages**
4. Common issues are listed below

---

## Common Issues & Fixes

### ❌ "502 Bad Gateway"

**Check the Logs:**
```
- Look for: "Address already in use"
- Look for: "ModuleNotFoundError"
- Look for: "ImportError"
```

**Fix:**
- Verify `gunicorn` is in `requirements.txt` ✓
- Check Start Command is correct ✓
- Wait 1-2 minutes and refresh

### ❌ "Build failed"

**In Logs, look for:**
- `pip install` errors → Missing package
- `python` errors → Syntax issue
- `migrate` errors → Database issue

**Fix:**
1. Check `build.sh` is executable
2. Verify `requirements.txt` has all packages
3. Try redeploying: Go to **Deploys** → click **"Redeploy"**

### ❌ "Static files not loading" (CSS/images look broken)

**Fix:**
- This is normal on free plan first load
- Refresh the page (Ctrl+F5)
- Wait 10 seconds and refresh again

### ❌ "App goes to sleep"

**Expected behavior on free plan:**
- Service sleeps after 15 minutes of no requests
- When you visit, it wakes up automatically (~30 seconds)
- This is normal and not an error

---

## Step 10: Setup Auto-Wakeup (Optional)

To prevent sleep, use a free pinging service:

1. Go to **https://uptimerobot.com** or **https://www.pingdom.com**
2. Create a monitor pointing to your Render URL
3. Set it to ping every 5 minutes
4. Your app won't sleep

---

## What to Do If Deployment Fails

### Option A: Check Logs (Recommended)
1. Go to your service on Render
2. Click **"Logs"** tab
3. **Read the error message carefully**
4. Search for the error below or in the guide

### Option B: Manual Redeploy
1. Go to **"Deploys"** tab
2. Click **"Redeploy"** button
3. Wait for new deployment

### Option C: Check GitHub Push
1. Verify your code was pushed to GitHub
2. Check: https://github.com/muhmmdaman/coursemanager
3. You should see all your files there

---

## Free Plan Limitations & Solutions

| Limitation | Impact | Solution |
|-----------|--------|----------|
| 15 min sleep | App takes 30s to wake | Use uptimerobot to ping |
| 512 MB RAM | May run slow | Optimize later |
| SQLite DB | Data lost on redeploy | Upgrade to PostgreSQL later |
| No custom domain | Long URL | Add domain later ($12/month) |
| Limited bandwidth | Not an issue for testing | Fine for free plan |

---

## Upgrade to PostgreSQL (When Ready)

When you want persistent data:

1. In Render dashboard, click **"+ New +"**
2. Select **"PostgreSQL"**
3. Name: `coursemanager-db`
4. Copy the connection string
5. Add to Web Service environment:
   - **Key:** `DATABASE_URL`
   - **Value:** (paste connection string)
6. Render will auto-redeploy

---

## Success Checklist

- ✅ Render account created
- ✅ GitHub connected
- ✅ Web Service created
- ✅ All environment variables added
- ✅ Build & start commands correct
- ✅ Deployment completed successfully
- ✅ URL works in browser
- ✅ Can login with test credentials
- ✅ Courses display properly
- ✅ Admin panel accessible

---

## Next Steps After Deployment

1. **Test thoroughly** on live URL
2. **Create real accounts** (delete test data later)
3. **Add courses** using instructor dashboard
4. **Monitor logs** for any errors
5. **Plan upgrades** when outgrowing free tier

---

## Troubleshooting Flowchart

```
App won't deploy?
├─ Check Logs → Find error message
├─ Verify build.sh exists
├─ Check requirements.txt complete
└─ Redeploy

App shows 502 error?
├─ Check Logs for errors
├─ Verify Start Command
├─ Wait 2 minutes and refresh
└─ Redeploy if needed

Static files broken?
├─ Refresh page (Ctrl+F5)
├─ Wait 10 seconds
└─ It's WhiteNoise catching up

Can't login?
├─ Check migrations ran (see logs)
├─ Try admin account: admin/admin123
└─ Check database exists
```

---

## Support Resources

- **Render Docs:** https://render.com/docs
- **Django Deployment:** https://docs.djangoproject.com/en/4.2/howto/deployment/
- **GitHub Issues:** Check your repo for errors
- **Render Support:** render.com/support

---

## Important Commands (Reference)

If you need to make changes:

```bash
# Make changes locally
# Commit to GitHub
git add .
git commit -m "Your changes"
git push origin master

# Render automatically detects and redeploys
# Watch Logs tab to see deployment progress
```

---

**You're ready to deploy! 🚀 Follow the steps above and your Course Hub will be live in minutes!**
