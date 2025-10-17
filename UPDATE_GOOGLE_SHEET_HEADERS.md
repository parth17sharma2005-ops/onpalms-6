# Update Google Sheet Headers for TOFU Data

## Current Issue
Your Google Sheet doesn't have the TOFU enhancement columns (Lead Score, Stage, Signals, Touches).

## Solution Options

### Option 1: Manual Update (Quick - 2 minutes)
1. Open your Google Sheet: https://docs.google.com/spreadsheets/d/1kxAbogmt-khwhUzoJI14uKhgANFLP_EuHYQtNKHmVYc
2. In Row 1, make sure you have these **9 columns in order**:

```
A1: Timestamp
B1: Name  
C1: Email
D1: Phone
E1: Source
F1: Lead Score
G1: Stage
H1: Signals
I1: Touches
```

3. Format Row 1:
   - Make text **bold**
   - Add light gray background (#f0f0f0)

4. Save and test!

---

### Option 2: Create New Sheet Tab (Fresh Start - 3 minutes)
1. Open your Google Sheet
2. Create a new tab called "Leads_TOFU"
3. Add headers manually as shown above
4. Update Google Apps Script:
   - Change: `const SHEET_NAME = 'Sheet1';`
   - To: `const SHEET_NAME = 'Leads_TOFU';`

---

### Option 3: Run This Google Apps Script Function (Advanced - 5 minutes)
Add this function to your Google Apps Script and run it once:

```javascript
function updateSheetHeaders() {
  const SHEET_ID = '1kxAbogmt-khwhUzoJI14uKhgANFLP_EuHYQtNKHmVYc';
  const SHEET_NAME = 'Sheet1';
  
  const sheet = SpreadsheetApp.openById(SHEET_ID).getSheetByName(SHEET_NAME);
  
  // Update headers
  sheet.getRange(1, 1, 1, 9).setValues([
    ['Timestamp', 'Name', 'Email', 'Phone', 'Source', 'Lead Score', 'Stage', 'Signals', 'Touches']
  ]);
  
  // Format headers
  sheet.getRange(1, 1, 1, 9).setFontWeight('bold');
  sheet.getRange(1, 1, 1, 9).setBackground('#f0f0f0');
  sheet.autoResizeColumns(1, 9);
  
  Logger.log('Headers updated successfully!');
}
```

Then:
1. Go to https://script.google.com
2. Open your PALMS Demo Form script
3. Add the function above
4. Click the function dropdown and select `updateSheetHeaders`
5. Click Run (play button)
6. Authorize if needed
7. Check the sheet - headers should be updated!

---

## What Each Column Captures

| Column | Description | Example |
|--------|-------------|---------|
| **Timestamp** | When form was submitted | 2025-10-15 21:38:08 |
| **Name** | Lead's full name | John Smith |
| **Email** | Business email | john@acme.com |
| **Phone** | Phone number | +1 (555) 123-4567 |
| **Source** | Form origin | Localhost Demo Form |
| **Lead Score** | TOFU score (0-100) | 75 |
| **Stage** | Lead temperature | direct_sales |
| **Signals** | Qualification flags | authority_high, timeline_urgent |
| **Touches** | Conversation depth | 5 |

---

## After Updating Headers

Test it by:
1. Going to http://127.0.0.1:5002
2. Chatting with the bot
3. Clicking "Book a call" or "Schedule a demo"
4. Filling out the form
5. Checking your Google Sheet - you should see all 9 columns populated!

---

## Verification
Once you've updated the headers, new submissions will include:
- ✅ Lead Score showing buying intent (0-100)
- ✅ Stage showing lead temperature
- ✅ Qualification signals (authority, budget, timeline indicators)
- ✅ Touch count showing conversation engagement

This rich data helps you prioritize which leads to follow up with first! 🎯
