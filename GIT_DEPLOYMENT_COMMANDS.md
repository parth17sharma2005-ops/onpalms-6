# 🚀 Deploy to onpalms-6 Repository

## Step 1: Initialize and Connect to GitHub

```bash
cd /Users/musashi/Desktop/bot_testing_v2

# Initialize git if not already done
git init

# Add the onpalms-6 repository as remote
git remote add origin https://github.com/parth17sharma2005-ops/onpalms-6.git

# Or if remote already exists, update it
git remote set-url origin https://github.com/parth17sharma2005-ops/onpalms-6.git
```

## Step 2: Stage and Commit All Files

```bash
# Stage all files
git add .

# Commit with descriptive message
git commit -m "Initial deployment: PALMS chatbot with TOFU sales intelligence"
```

## Step 3: Push to GitHub

```bash
# Push to main branch
git push -u origin main

# Or if you need to force push (only if repository exists)
git push -u origin main --force
```

## Step 4: Verify on GitHub

1. Go to: https://github.com/parth17sharma2005-ops/onpalms-6
2. Verify all files are uploaded:
   - ✅ app.py
   - ✅ chat.py
   - ✅ requirements.txt
   - ✅ Procfile
   - ✅ runtime.txt
   - ✅ info.txt
   - ✅ templates/index.html
   - ✅ google-apps-script.js
   - ✅ README.md
   - ✅ DEPLOYMENT.md

## Step 5: Deploy on Render

1. Go to [Render.com](https://render.com)
2. Click **"New +"** → **"Web Service"**
3. Select repository: `parth17sharma2005-ops/onpalms-6`
4. Configure:
   - Name: `palms-chatbot-tofu`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
5. Add environment variable:
   - `OPENAI_API_KEY`: (your key)
6. Click "Create Web Service"

## Step 6: Get Your API URL

After deployment completes (5-10 minutes), you'll get a URL like:
```
https://palms-chatbot-tofu.onrender.com
```

## Step 7: Update footer.php

In your WordPress/PHP project, update the API URL:

```javascript
// OLD (local development)
const API_URL = 'http://localhost:5002';

// NEW (production on Render)
const API_URL = 'https://palms-chatbot-tofu.onrender.com';
```

## 🎉 Done!

Your chatbot is now live and ready to capture leads with TOFU intelligence!

## 📝 Important Notes

- **Do NOT commit** `.env` file (it's in `.gitignore`)
- **Do commit** all Python files, templates, and config files
- **ChromaDB folder** is ignored - it will be created fresh on Render
- **Environment variables** must be set in Render dashboard

## 🔄 Future Updates

To update your deployed app:

```bash
git add .
git commit -m "Your update description"
git push origin main
```

Render will automatically detect the push and redeploy! ✨
