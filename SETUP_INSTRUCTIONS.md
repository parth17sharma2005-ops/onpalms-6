# PALMS Chatbot Integration Setup Guide

## Overview
This guide will help you:
1. Deploy your Flask backend to Render
2. Set up Google Sheets integration 
3. Update the footer.php with the new API URL

## Step 1: Deploy Backend to Render

1. **Push your code to GitHub:**
   ```bash
   git add .
   git commit -m "Updated chatbot with phone number and fixed OpenAI integration"
   git push origin main
   ```

2. **Deploy on Render:**
   - Go to https://render.com
   - Connect your GitHub repository
   - Create a new Web Service
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `python app.py`
   - Add environment variable: `OPENAI_API_KEY` (your OpenAI API key)
   - Add environment variable: `ALLOW_RESET=TRUE`
   - Deploy the service

3. **Get your Render URL:**
   - After deployment, you'll get a URL like: `https://your-app-name.onrender.com`

## Step 2: Set Up Google Sheets Integration

### A. Create Google Sheet
1. Go to https://sheets.google.com
2. Create a new sheet called "PALMS Demo Requests"
3. Add headers in row 1: `Timestamp | Name | Email | Phone | Source`
4. Copy the Sheet ID from the URL (between `/d/` and `/edit`):
   ```
   https://docs.google.com/spreadsheets/d/SHEET_ID_HERE/edit
   ```

### B. Set Up Google Apps Script
1. Go to https://script.google.com
2. Click "New Project"
3. Delete the default code
4. Copy and paste the code from `google-apps-script.js`
5. Replace `YOUR_GOOGLE_SHEET_ID_HERE` with your actual Sheet ID
6. Save the project (give it a name like "PALMS Demo Form Handler")

### C. Deploy as Web App
1. Click "Deploy" → "New deployment"
2. Choose "Web app" as type
3. Set execute as: "Me"
4. Set access to: "Anyone"
5. Click "Deploy"
6. Copy the Web App URL (looks like: `https://script.google.com/macros/s/SCRIPT_ID/exec`)

## Step 3: Update footer.php

1. **Update API URL:**
   Replace line 437 in footer.php:
   ```javascript
   const API_URL = 'https://YOUR_RENDER_URL_HERE';
   ```

2. **Update Google Script URL:**
   Replace line 847 in footer.php:
   ```javascript
   const GOOGLE_SCRIPT_URL = 'https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec';
   ```

## Step 4: Test the Integration

1. **Test Backend API:**
   - Visit: `https://your-render-url.onrender.com`
   - Chat with the bot
   - Request a demo
   - Check if form appears and submits correctly

2. **Test Google Sheets:**
   - Submit a demo request
   - Check your Google Sheet for the new row
   - Verify all data is captured correctly

## Key Changes Made

### Backend Integration:
- ✅ Fixed demo trigger: `show_demo_form` instead of `show_demo_popup`
- ✅ Updated API endpoints to match your backend (`/chat` and `/submit_demo`)
- ✅ Added proper session handling with `session_id`
- ✅ Added phone number field to demo form (optional)
- ✅ Proper error handling from backend validation

### Google Sheets Integration:
- ✅ Real-time data submission to Google Sheets
- ✅ Automatic timestamp and source tracking
- ✅ Error handling (won't break if Sheets fails)
- ✅ Dual submission (backend + Google Sheets)

### Form Improvements:
- ✅ Inline demo form with phone number
- ✅ Better validation and error display
- ✅ Matches your backend validation logic
- ✅ Professional styling with PALMS branding

## Demo Form Flow:
1. User requests demo in chat
2. Backend sends `show_demo_form: true`
3. Inline form appears with Name, Email, Phone fields
4. User submits form
5. Data sent to both:
   - Your Flask backend (`/submit_demo`)
   - Google Sheets (real-time)
6. Backend validates business email
7. Success/error message shown to user
8. Lead data stored in both systems

## Troubleshooting:

**If demo form doesn't appear:**
- Check browser console for API errors
- Verify your Render URL is correct
- Test your backend API directly

**If Google Sheets isn't updating:**
- Check Google Apps Script logs
- Verify Sheet ID is correct
- Test the script manually in Apps Script editor

**If email validation fails:**
- Check that backend is running
- Verify business email validation logic
- Check Flask logs on Render

Your chatbot now has:
- ✅ Real OpenAI responses (no more fallback messages)
- ✅ Proper demo form with phone number
- ✅ Google Sheets integration for lead tracking  
- ✅ Business email validation
- ✅ Professional floating widget design
