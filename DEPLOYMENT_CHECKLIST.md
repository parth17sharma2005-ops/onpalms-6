# ✅ Pre-Deployment Checklist

## Before Pushing to GitHub

- [ ] **requirements.txt** - Contains only necessary packages with gunicorn
- [ ] **Procfile** - Exists with correct start command
- [ ] **runtime.txt** - Specifies Python 3.11.9
- [ ] **.gitignore** - Prevents sensitive files from being committed
- [ ] **.env file** - NOT committed (should be in .gitignore)
- [ ] **Google Apps Script URL** - Updated in app.py
- [ ] **info.txt** - Contains PALMS™ knowledge base
- [ ] **templates/index.html** - Chat interface exists

## Files to Push to onpalms-6

### Essential Backend Files
- [x] `app.py` - Main Flask application
- [x] `chat.py` - AI chatbot with TOFU logic
- [x] `requirements.txt` - Production dependencies
- [x] `Procfile` - Gunicorn start command
- [x] `runtime.txt` - Python version
- [x] `.gitignore` - Exclude sensitive files

### Knowledge & Templates
- [x] `info.txt` - PALMS™ knowledge base
- [x] `templates/index.html` - Chat interface

### Integration Files
- [x] `google-apps-script.js` - For Google Sheets setup

### Documentation
- [x] `README.md` - Project overview
- [x] `DEPLOYMENT.md` - Deployment instructions
- [x] `GIT_DEPLOYMENT_COMMANDS.md` - Git commands
- [x] `UPDATE_GOOGLE_SHEET_HEADERS.md` - Google Sheets setup

## DO NOT Push (Auto-excluded by .gitignore)

- [ ] **.env** - Contains API keys
- [ ] **__pycache__/** - Python cache
- [ ] **venv/** - Virtual environment
- [ ] **chroma_db/** - Will be created fresh on Render
- [ ] **.DS_Store** - Mac OS files

## After Deployment on Render

- [ ] Set `OPENAI_API_KEY` environment variable
- [ ] Set `FLASK_DEBUG=False`
- [ ] Wait for build to complete (~5-10 minutes)
- [ ] Test the deployed URL
- [ ] Verify chat functionality
- [ ] Test demo form submission
- [ ] Check Google Sheets receives data with all 9 columns

## Update footer.php

- [ ] Replace `http://localhost:5002` with your Render URL
- [ ] Test from your WordPress/PHP site
- [ ] Verify CORS is working
- [ ] Confirm leads are being captured

## Post-Deployment Verification

- [ ] Visit `https://your-app.onrender.com/` - Shows chat interface
- [ ] Send test message - Bot responds correctly
- [ ] Trigger demo form - Form appears
- [ ] Submit form with business email - Success message
- [ ] Check Google Sheet - New row with all 9 columns:
  - [ ] Timestamp
  - [ ] Name
  - [ ] Email
  - [ ] Phone
  - [ ] Source
  - [ ] Lead Score
  - [ ] Stage
  - [ ] Signals
  - [ ] Touches

## Google Sheets Verification

- [ ] Headers match expected format (9 columns)
- [ ] Lead Score shows numerical value (0-100)
- [ ] Stage shows one of: awareness/nurture_cold/nurture_warm/direct_sales
- [ ] Signals show qualification data
- [ ] Touch Count shows conversation depth

---

**Once all checkboxes are complete, your deployment is successful! 🎉**
