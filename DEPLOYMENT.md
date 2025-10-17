# PALMS Chatbot Deployment Guide - Render

## 🚀 Quick Deploy to Render

### Step 1: Push to GitHub Repository
1. Make sure all your changes are committed to `onpalms-6` repository
2. Push to GitHub:
   ```bash
   cd /Users/musashi/Desktop/bot_testing_v2
   git add .
   git commit -m "Prepare for Render deployment with TOFU enhancements"
   git push origin main
   ```

### Step 2: Deploy on Render
1. Go to [Render.com](https://render.com) and sign in
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account (if not already connected)
4. Select the repository: **`parth17sharma2005-ops/onpalms-6`**
5. Configure the deployment settings:
   - **Name**: `palms-chatbot-tofu` (or your preferred name)
   - **Environment**: `Python 3`
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

### Step 3: Add Environment Variables
In the Render dashboard, add these environment variables:
- **`OPENAI_API_KEY`**: Your OpenAI API key (from https://platform.openai.com)
- **`FLASK_DEBUG`**: `False`
- **`PORT`**: `10000` (Render default, optional)

### Step 4: Deploy
1. Click **"Create Web Service"**
2. Wait for the build to complete (usually 5-10 minutes)
3. Your app will be live at: `https://palms-chatbot-tofu.onrender.com`

---

## 📝 After Deployment - Update footer.php

Once your Render deployment is live, update the API URL in your `footer.php` file:

```javascript
// Replace this line in footer.php:
const API_URL = 'http://localhost:5002'; // OLD

// With your new Render URL:
const API_URL = 'https://palms-chatbot-tofu.onrender.com'; // NEW
```

Or use your actual Render URL if you named it differently.

---

## 🧪 Testing the Deployment

1. **Test the API endpoint**: 
   - Visit `https://your-app-name.onrender.com/` - should show the chat interface
   
2. **Test chat functionality**:
   - Send a message and verify bot responses
   - Check that TOFU lead scoring is working
   
3. **Test demo form submission**:
   - Request a demo through the chat
   - Fill out the form with a business email
   - Verify data appears in your Google Sheet with all 9 columns:
     - Timestamp, Name, Email, Phone, Source
     - Lead Score, Stage, Signals, Touches

---

## 🔧 Environment Variables Explained

| Variable | Value | Purpose |
|----------|-------|---------|
| `OPENAI_API_KEY` | Your API key | Enables AI chatbot responses with GPT-4o-mini |
| `FLASK_DEBUG` | `False` | Disables debug mode for production security |
| `PORT` | `10000` | Port Render uses (auto-configured) |

---

## 📦 What's Included in This Deployment

### Core Files:
- ✅ `app.py` - Main Flask application with TOFU enhancements
- ✅ `chat.py` - AI chatbot with lead qualification system
- ✅ `requirements.txt` - Production dependencies (optimized)
- ✅ `Procfile` - Tells Render how to start the app
- ✅ `runtime.txt` - Specifies Python version
- ✅ `templates/index.html` - Chat interface
- ✅ `info.txt` - PALMS™ knowledge base

### TOFU Features:
- ✅ 4-tier lead scoring (0-100 points)
- ✅ Smart qualification signals (authority, budget, timeline)
- ✅ Progressive conversation flows
- ✅ Enhanced Google Sheets integration
- ✅ Multi-touch tracking

---

## 🐛 Troubleshooting

### Issue: Build Fails
- **Check logs** in Render dashboard for specific errors
- **Verify** `requirements.txt` has no syntax errors
- **Ensure** all files are pushed to GitHub

### Issue: OpenAI API Not Working
- **Verify** your `OPENAI_API_KEY` is correct
- **Check** you have credits in your OpenAI account
- **Look** at Render logs for specific OpenAI errors

### Issue: ChromaDB Fails to Initialize
- This is normal on first deployment - it will create the database
- Check Render logs to ensure `info.txt` was loaded properly

### Issue: Google Sheets Not Receiving Data
- **Verify** your Google Apps Script URL in `app.py` is correct
- **Check** the script deployment is set to "Anyone" access
- **Test** the script URL directly in a browser

### Issue: Slow Cold Start
- Render free tier has ~1 minute cold start after inactivity
- Consider upgrading to paid tier for instant availability

---

## 📊 Monitoring Your Deployment

### Render Dashboard:
- **Logs**: View real-time application logs
- **Metrics**: Monitor CPU, memory usage
- **Events**: See deployment history

### Google Sheets:
- Track all leads with rich TOFU data
- Filter by lead score to prioritize follow-ups
- Analyze qualification signals

---

## 🔄 Updating Your Deployment

When you make changes to your code:

```bash
# Commit and push changes
git add .
git commit -m "Your update description"
git push origin main
```

Render will automatically detect the push and redeploy! ✨

---

## 💡 Pro Tips

1. **Use environment variables** for all sensitive data (API keys, URLs)
2. **Monitor Render logs** regularly for errors
3. **Test locally first** before pushing to production
4. **Keep your OpenAI key secure** - never commit it to GitHub
5. **Check Google Sheets** regularly to ensure data is flowing

---

## 📞 Support

If you encounter issues:
1. Check Render logs first
2. Verify all environment variables are set
3. Test your Google Apps Script independently
4. Ensure your OpenAI account has available credits

---

**Your deployment is ready! 🎉**

After deploying, your chatbot will be available at your Render URL, and you can update `footer.php` with the new API endpoint.

## Environment Variables Required
- `OPENAI_API_KEY`: Your OpenAI API key (get from https://platform.openai.com)
- `ALLOW_RESET`: Set to `TRUE` (allows ChromaDB to reset if needed)
- `FLASK_DEBUG`: Set to `False` for production

## After Deployment
1. Your app will be available at: `https://your-app-name.onrender.com`
2. Update `footer.php` with the new URL:
   ```javascript
   const API_URL = 'https://your-app-name.onrender.com';
   ```

## Testing the Deployment
1. Visit `https://your-app-name.onrender.com` (should show the chat interface)
2. Test the chat functionality
3. Test the demo form submission

## Troubleshooting
- If ChromaDB fails to initialize, check that `ALLOW_RESET=TRUE` is set
- If OpenAI fails, verify your `OPENAI_API_KEY` is correct and has credits
- Check Render logs for any deployment errors

## Files Modified for Deployment
- `app.py`: Updated to use environment PORT variable
- `Procfile`: Added for deployment process
- `render.yaml`: Added for easy Render deployment
- This deployment guide created
