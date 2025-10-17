/**
 * Google Apps Script for PALMS Demo Form Integration with TOFU Enhancement
 * 
 * DEPLOYMENT INFO:
 * Deployment ID: AKfycbwtkTDW3CjoKgSJrDgj2dWn6oU-ZXYncoGuu6h7zeB5lT14xe_8Q-yjtlwYxHZ61H77
 * Web App URL: https://script.google.com/macros/s/AKfycbwtkTDW3CjoKgSJrDgj2dWn6oU-ZXYncoGuu6h7zeB5lT14xe_8Q-yjtlwYxHZ61H77/exec
 * 
 * SETUP INSTRUCTIONS:
 * 1. Go to https://script.google.com
 * 2. Create a new project
 * 3. Replace the default code with this script
 * 4. Create a Google Sheet with headers: Timestamp, Name, Email, Phone, Source, Lead Score, Stage, Signals, Touches
 * 5. Replace SHEET_ID with your Google Sheet ID
 * 6. Deploy as Web App with execute permissions for "Anyone"
 * 7. Copy the Web App URL and update GOOGLE_SCRIPT_URL in app.py
 */

// Replace this with your Google Sheet ID (found in the sheet URL)
const SHEET_ID = '1kxAbogmt-khwhUzoJI14uKhgANFLP_EuHYQtNKHmVYc';
const SHEET_NAME = 'Sheet1'; // Name of the sheet tab (change to your actual tab name)

function doPost(e) {
  try {
    // Parse the request data
    const data = JSON.parse(e.postData.contents);
    
    // Open the Google Sheet
    const sheet = SpreadsheetApp.openById(SHEET_ID).getSheetByName(SHEET_NAME);
    
    // If sheet doesn't exist, create it with headers
    if (!sheet) {
      const newSheet = SpreadsheetApp.openById(SHEET_ID).insertSheet(SHEET_NAME);
      newSheet.getRange(1, 1, 1, 9).setValues([
        ['Timestamp', 'Name', 'Email', 'Phone', 'Source', 'Lead Score', 'Stage', 'Signals', 'Touches']
      ]);
      
      // Format header row - all 9 columns
      newSheet.getRange(1, 1, 1, 9).setFontWeight('bold');
      newSheet.getRange(1, 1, 1, 9).setBackground('#f0f0f0');
    }
    
    // Get the sheet (after potential creation)
    const targetSheet = SpreadsheetApp.openById(SHEET_ID).getSheetByName(SHEET_NAME);
    
    // Prepare the row data with enhanced TOFU fields
    const rowData = [
      data.timestamp || new Date().toLocaleString(),
      data.name || '',
      data.email || '',
      data.phone || '',
      data.source || 'Website',
      data.lead_score || 0,
      data.stage || 'unknown',
      data.qualification_signals || '',
      data.touch_count || 0
    ];
    
    // Append the data to the sheet
    targetSheet.appendRow(rowData);
    
    // Auto-resize columns for better readability
    targetSheet.autoResizeColumns(1, 9);
    
    // Return success response
    return ContentService
      .createTextOutput(JSON.stringify({
        success: true,
        message: 'Data successfully added to Google Sheet'
      }))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (error) {
    // Return error response
    return ContentService
      .createTextOutput(JSON.stringify({
        success: false,
        message: 'Error: ' + error.toString()
      }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet(e) {
  // Handle GET requests (optional, for testing)
  return ContentService
    .createTextOutput(JSON.stringify({
      message: 'PALMS Demo Form Google Apps Script is running',
      timestamp: new Date().toLocaleString()
    }))
    .setMimeType(ContentService.MimeType.JSON);
}

// Test function to verify the script works
function testScript() {
  const testData = {
    postData: {
      contents: JSON.stringify({
        timestamp: new Date().toLocaleString(),
        name: 'Test User',
        email: 'test@example.com',
        phone: '+1234567890',
        source: 'Test'
      })
    }
  };
  
  const result = doPost(testData);
  Logger.log(result.getContent());
}
