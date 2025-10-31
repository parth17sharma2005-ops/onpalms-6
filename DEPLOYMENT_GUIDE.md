# PALMS™ Chatbot Deployment Guide

## 🎯 Overview
This guide covers deploying the PALMS™ AI Sales Assistant with backend on Render and frontend on WordPress.

---

## 📦 Architecture

```
┌─────────────────────────────────────────────────┐
│           WordPress Website                      │
│         (smartwms.onpalms.com)                  │
│                                                  │
│  ┌────────────────────────────────┐            │
│  │  footer.php (Chatbot Widget)   │            │
│  │  - JavaScript Frontend         │            │
│  │  - Auto-greeting               │            │
│  │  - Demo forms                  │            │
│  └────────────┬───────────────────┘            │
│               │ API Calls                       │
│               │ (HTTPS)                         │
└───────────────┼─────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────┐
│        Render.com (Backend API)                  │
│     https://onpalms-6.onrender.com              │
│                                                  │
│  ┌────────────────────────────────┐            │
│  │  Flask App (app.py)            │            │
│  │  - /chat endpoint              │            │
│  │  - /submit_demo endpoint       │            │
│  │  - /submit_info endpoint       │            │
│  └────────┬───────────────────────┘            │
│           │                                     │
│  ┌────────▼───────────────────────┐            │
│  │  chat.py (AI Logic)            │            │
│  │  - RAG with ChromaDB           │            │
│  │  - TOFU lead scoring           │            │
│  │  - GPT-4o-mini responses       │            │
│  └────────┬───────────────────────┘            │
│           │                                     │
│  ┌────────▼───────────────────────┐            │
│  │  info.txt (Knowledge Base)     │            │
│  │  - 9 PALMS products            │            │
│  │  - 14,817 characters           │            │
│  │  - 35 chunks in ChromaDB       │            │
│  └────────────────────────────────┘            │
└─────────────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────┐
│      Google Sheets (Lead Storage)                │
│  https://script.google.com/macros/s/...         │
└─────────────────────────────────────────────────┘
```

---

## 🚀 Backend Deployment (Render)

### **Required Files** ✅
All files are ready in the repository:

1. **app.py** - Flask server with endpoints:
   - `/chat` - Main conversation endpoint
   - `/submit_demo` - Demo request submission
   - `/submit_info` - User info collection
   
2. **chat.py** - AI chatbot logic:
   - RAG with ChromaDB
   - OpenAI GPT-4o-mini
   - TOFU lead qualification
   - Automatic knowledge base refresh
   
3. **info.txt** - Knowledge base:
   - 9 PALMS products
   - Complete feature descriptions
   - FAQs and pricing info
   
4. **requirements.txt** - Python dependencies
5. **Procfile** - Gunicorn configuration
6. **runtime.txt** - Python 3.11.9
7. **render.yaml** - Render deployment config

### **Deployment Steps**

#### 1️⃣ **Push to GitHub**
```bash
# Stage all files
git add app.py chat.py info.txt requirements.txt Procfile runtime.txt render.yaml footer.php templates/index.html refresh_database.py

# Commit changes
git commit -m "Production-ready backend with footer.php compatibility"

# Push to main branch
git push origin main
```

#### 2️⃣ **Deploy on Render**
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository: `onpalms-6`
4. Configure:
   - **Name**: `palms-chatbot` (or `onpalms-6`)
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT app:app`
   - **Plan**: Free (or paid for better performance)

#### 3️⃣ **Set Environment Variables**
In Render dashboard, add:
```
OPENAI_API_KEY = sk-proj-your-actual-key-here
FLASK_DEBUG = False
ALLOW_RESET = TRUE
```

#### 4️⃣ **Deploy!**
- Click **"Create Web Service"**
- Wait 5-10 minutes for deployment
- Your API will be live at: `https://onpalms-6.onrender.com`

---

## 🌐 Frontend Deployment (WordPress)

### **File: footer.php**

Already configured with correct API URL:
```javascript
const API_URL = 'https://onpalms-6.onrender.com';
```

### **Deployment Steps**

#### 1️⃣ **Access WordPress**
1. Log in to WordPress admin
2. Go to: **Appearance** → **Theme File Editor**
3. Select your active theme (e.g., "Hello Elementor")

#### 2️⃣ **Upload footer.php**
1. Find `footer.php` in the theme files list (or create it)
2. Copy entire content from `/Users/musashi/Desktop/bot_testing_v3/footer.php`
3. Paste into WordPress editor
4. Click **"Update File"**

#### 3️⃣ **Verify**
- Visit your website: `https://smartwms.onpalms.com`
- Chatbot should appear in bottom-right corner
- Click to open and test greeting message

---

## 🔧 Configuration Details

### **Endpoints Compatibility** ✅

| Endpoint | footer.php Calls | app.py Provides | Status |
|----------|------------------|-----------------|--------|
| `/chat` | ✅ Yes | ✅ Yes | ✅ Compatible |
| `/submit_demo` | ✅ Yes | ✅ Yes | ✅ Compatible |
| `/submit_info` | ✅ Yes | ✅ Yes | ✅ **FIXED** |

### **Google Sheets Integration** ✅

**Backend (app.py):**
```python
GOOGLE_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbwtkTDW3CjoKgSJrDgj2dWn6oU-ZXYncoGuu6h7zeB5lT14xe_8Q-yjtlwYxHZ61H77/exec'
```

**Frontend (footer.php):**
```javascript
const GOOGLE_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbwtkTDW3CjoKgSJrDgj2dWn6oU-ZXYncoGuu6h7zeB5lT14xe_8Q-yjtlwYxHZ61H77/exec';
```
✅ **SYNCED** - Both use same URL

### **Greeting Messages** ✅

**index.html (Local Testing):**
```
Hello! I'm your PALMS™ Sales Assistant. 👋
How can I assist you today?
```

**footer.php (Production):**
```
Hello! I'm your PALMS™ Sales Assistant. 👋
How can I assist you today?
```
✅ **SYNCED** - Same greeting

---

## 📝 Response Formatting

The bot now uses:
- **Bullet points (•)** for product lists and features
- **4-5 line descriptions** for specific products
- **Concise responses** to avoid overwhelming users

Example:
```
User: "Tell me about the products"
Bot: Here are our PALMS™ products:
     • PALMS™ WMS - Core warehouse management
     • PALMS™ 3PL - Multi-client operations
     • PALMS™ Cross Dock - Real-time transfers
     [etc...]
```

---

## 🧪 Testing Checklist

### **Local Testing (Before Deploy)**
- [x] Run `python app.py` successfully
- [x] Test `/chat` endpoint with products query
- [x] Test demo form submission
- [x] Verify bullet points in responses
- [x] Check greeting message displays

### **Production Testing (After Deploy)**
- [ ] Visit WordPress site
- [ ] Chatbot widget appears in bottom-right
- [ ] Greeting displays on open
- [ ] Ask "tell me about the products" - should show bullet list
- [ ] Ask "tell me about PALMS WMS" - should show 4-5 line description
- [ ] Test demo form - should validate business email
- [ ] Verify Google Sheets receives data

---

## 🔐 Security Notes

1. **API Keys**: Never commit `.env` file (already in `.gitignore`)
2. **CORS**: Enabled for WordPress origin
3. **Business Email Validation**: Blocks Gmail, Yahoo, etc. for demos
4. **Session Management**: Uses in-memory sessions (consider Redis for production scale)

---

## 📊 Knowledge Base

**Current Stats:**
- Total characters: 14,817
- Products: 9 (WMS, 3PL, Cross Dock, Portals, WCS, Mobile, Analytics, Light, Enterprise)
- Chunks in ChromaDB: 35
- Chunk size: 2000 words with 200-word overlap

**To Update Knowledge Base:**
1. Edit `info.txt`
2. Run `python refresh_database.py` (local testing)
3. Push to GitHub
4. Render will auto-rebuild ChromaDB on next deploy

---

## 🐛 Troubleshooting

### **Issue: "Connection error" in chatbot**
- Check Render logs: `https://dashboard.render.com`
- Verify OPENAI_API_KEY is set
- Check Render service is running (not sleeping)

### **Issue: Demo form not submitting**
- Check browser console for errors
- Verify business email validation message
- Check Google Sheets URL is correct

### **Issue: Bot gives generic responses**
- Check ChromaDB initialized: logs should show "35 chunks"
- Verify `info.txt` is in repository
- Restart Render service

---

## 📈 Monitoring

**Render Dashboard:**
- View deployment logs
- Monitor API requests
- Check memory/CPU usage

**Google Sheets:**
- Track demo requests
- View lead scores
- Monitor conversion funnel

---

## 🎉 Success Criteria

✅ Backend deployed on Render
✅ Frontend integrated in WordPress
✅ Chatbot appears on website
✅ Greeting displays automatically
✅ Products listed with bullet points
✅ Demo form validates business emails
✅ Google Sheets receives submissions
✅ Responses are concise and accurate

---

## 📞 Support

**Repository:** `parth17sharma2005-ops/onpalms-6`
**Backend URL:** `https://onpalms-6.onrender.com`
**Frontend:** `https://smartwms.onpalms.com`

---

Last Updated: October 31, 2025
