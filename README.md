# 🤖 PALMS™ RAG Sales Chatbot

A sophisticated RAG (Retrieval-Augmented Generation) chatbot built with Flask, OpenAI GPT-4o-mini, and ChromaDB for intelligent warehouse management solution sales conversations.

## ✨ Features

- **🧠 Two-Layer AI System**: Information retrieval + contextual sales conversation
- **💬 Context-Aware Conversations**: Remembers user preferences and conversation history
- **📊 Lead Scoring & Qualification**: Automatic lead scoring based on user interactions
- **🎯 Smart Demo Management**: Respects user demo preferences and avoids pushy behavior
- **📱 Responsive UI**: Clean, modern chat interface with mobile support
- **💾 Session Management**: Persistent conversation state throughout user session
- **📧 Business Email Validation**: Validates business emails for demo requests
- **🔍 Vector Search**: ChromaDB-powered knowledge base for accurate information retrieval

## 🏗️ Architecture

### Two-Layer AI System:
1. **Information Layer**: Extracts relevant information from knowledge base using RAG
2. **Sales Layer**: Generates contextual, sales-focused responses using OpenAI GPT-4o-mini

### Tech Stack:
- **Backend**: Flask (Python)
- **AI/ML**: OpenAI GPT-4o-mini, Sentence Transformers
- **Vector Database**: ChromaDB
- **Frontend**: HTML, CSS, JavaScript
- **Email Validation**: email-validator library

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Git (for cloning)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/parth17sharma2005-ops/salesbot-testing.git
   cd salesbot-testing
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   
   # Activate virtual environment
   # On macOS/Linux:
   source .venv/bin/activate
   
   # On Windows:
   .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file in root directory
   touch .env
   ```
   
   Add your OpenAI API key to `.env`:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```
   
   > **🔑 Get your OpenAI API key**: Visit [OpenAI API Keys](https://platform.openai.com/api-keys)

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open in browser**
   ```
   http://localhost:5002
   ```

## 📁 Project Structure

```
salesbot-testing/
├── app.py                 # Main Flask application
├── chat.py               # RAG chatbot logic and AI layers  
├── info.txt              # Knowledge base content
├── requirements.txt      # Python dependencies
├── templates/
│   └── index.html       # Chat interface UI
├── .env                 # Environment variables (create this)
└── README.md           # This file
```

## 🔧 Configuration

### Environment Variables (.env file)
```env
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional
FLASK_ENV=development
FLASK_DEBUG=True
```

### Customizing the Knowledge Base

Edit `info.txt` to customize the chatbot's knowledge base with your own product information, features, pricing, etc. The system will automatically process and index this content.

### Customizing Responses

Modify the response templates in `chat.py`:
- `get_enhanced_demo_response()`: Fallback responses when OpenAI API is unavailable
- AI prompts in `get_sales_layer_response()`: Customize the AI behavior and tone

## 🎯 Usage

### Basic Chat
- Ask questions about products, features, pricing
- The bot provides concise, helpful responses
- Automatic lead qualification based on conversation

### Demo Requests
- Users can request demos through conversation
- Smart demo form appears for qualified leads
- Business email validation prevents spam

### Lead Management
- Automatic lead scoring based on user engagement
- Session persistence for continued conversations
- Demo decline tracking (won't keep pushing demos)

## 🔍 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main chat interface |
| `/chat` | POST | Process chat messages |
| `/submit_demo` | POST | Handle demo form submissions |

### Chat API Example
```bash
curl -X POST http://localhost:5002/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is PALMS?", "session_id": "test_session"}'
```

## 🎨 UI Features

- **Responsive Design**: Works on desktop and mobile
- **Real-time Chat**: Instant message delivery with typing indicators
- **Loading States**: Professional loading dots at bottom of chat
- **Demo Modal**: Popup form for demo requests
- **Business Email Validation**: Client-side and server-side validation

## 🛠️ Development

### Adding New Features

1. **Extend Knowledge Base**: Add content to `info.txt`
2. **Modify AI Behavior**: Update prompts in `chat.py`
3. **UI Changes**: Edit `templates/index.html`
4. **New Endpoints**: Add routes in `app.py`

### Running in Development Mode
```bash
export FLASK_ENV=development
export FLASK_DEBUG=True
python app.py
```

## 🔒 Security Notes

- Never commit `.env` file to version control
- Use environment variables for all sensitive data
- Validate all user inputs (already implemented for emails)
- Consider adding rate limiting for production use

## 📦 Dependencies

Key dependencies (see `requirements.txt` for full list):

- **Flask 2.3.3**: Web framework
- **openai**: OpenAI API client  
- **chromadb 0.4.15**: Vector database
- **sentence-transformers**: Text embeddings
- **email-validator**: Email validation
- **flask-cors**: Cross-origin resource sharing

## 🚀 Production Deployment

### Recommended Steps:

1. **Use a production WSGI server**:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5002 app:app
   ```

2. **Set up environment variables**:
   - Use your hosting platform's environment variable system
   - Never hardcode API keys

3. **Database considerations**:
   - For production, consider using Redis for session storage
   - Backup ChromaDB data regularly

4. **Security enhancements**:
   - Add rate limiting
   - Use HTTPS
   - Implement proper logging

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🐛 Troubleshooting

### Common Issues:

**Port already in use:**
```bash
# Kill process on port 5002
lsof -ti:5002 | xargs kill -9
```

**OpenAI API errors:**
- Check your API key in `.env` file
- Ensure you have credits in your OpenAI account
- Verify API key permissions

**ChromaDB issues:**
- Delete `chroma_db/` folder and restart to reset database
- Check disk space and permissions

**Dependencies issues:**
```bash
# Clear pip cache and reinstall
pip cache purge
pip install --no-cache-dir -r requirements.txt
```

## 📞 Support

For issues and questions:
1. Check the troubleshooting section above
2. Open an issue on GitHub
3. Check OpenAI API documentation for API-related issues

---

**Built with ❤️ using Flask, OpenAI, and ChromaDB**
- **Demo Scheduling**: Integrated demo request form with business email validation
- **Pricing Queries**: Handles cost-related questions intelligently
- **FAQ Handling**: Instant answers from the knowledge base
- **Memory**: Maintains conversation context and lead scoring
- **Human Handoff**: Demo form for connecting with sales team

### 🎯 Salesbot Personality
- Professional yet approachable sales representative
- Goal-driven: always steering toward conversion
- Empathetic and reassuring when addressing concerns
- Uses persuasion psychology (urgency, validation, social proof)
- Mirrors visitor's tone (formal for B2B, casual for individuals)

### 🚀 Technical Features
- **RAG Implementation**: ChromaDB + Sentence Transformers for knowledge retrieval
- **Lead Scoring**: Automatic scoring based on user interactions
- **Business Email Validation**: Rejects personal email domains
- **Session Management**: Maintains conversation state
- **Beautiful UI**: Modern, responsive design with animations
- **Mobile Responsive**: Works perfectly on all devices

## Setup Instructions

### 1. Environment Setup
Make sure you have Python 3.8+ installed, then activate your virtual environment:

```bash
# The virtual environment is already configured
source .venv/bin/activate  # On macOS/Linux
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Edit the `.env` file and add your OpenAI API key:
```
OPENAI_API_KEY=your_actual_openai_api_key_here
```

### 4. Run the Application
```bash
python app.py
```

The chatbot will be available at: http://localhost:5000

## Project Structure
```
bot_testing/
├── app.py              # Flask application main file
├── chat.py             # RAG chatbot implementation
├── info.txt            # PALMS™ knowledge base
├── requirements.txt    # Python dependencies
├── .env               # Environment variables
├── templates/
│   └── index.html     # Beautiful chat interface
└── chroma_db/         # ChromaDB vector database (auto-created)
```

## How It Works

1. **Knowledge Base**: The `info.txt` file is processed and stored in ChromaDB for RAG retrieval
2. **User Interaction**: When a user sends a message, relevant context is retrieved from the knowledge base
3. **AI Response**: OpenAI GPT generates responses using the retrieved context and sales personality
4. **Lead Scoring**: Each interaction updates the lead score based on interest indicators
5. **Demo Forms**: High-scoring leads are presented with demo request forms
6. **Email Validation**: Business email domains are validated before accepting demo requests

## Lead Scoring System
- Asks about pricing: +10 points
- Mentions specific challenges: +15 points
- Provides company details: +20 points  
- Requests demo: +30 points
- Discusses timeline: +25 points
- Mentions budget: +20 points

## Business Email Validation
The system rejects personal email domains:
- gmail.com, yahoo.com, hotmail.com, outlook.com
- And other common personal email providers

## Customization
- Modify `info.txt` to update the knowledge base
- Adjust the salesbot personality in `chat.py`
- Customize the UI in `templates/index.html`
- Update lead scoring rules in the `analyze_message_intent` function

## Production Deployment
For production use:
1. Replace in-memory session storage with Redis or database
2. Add proper logging and error handling
3. Implement rate limiting
4. Add CRM integration for lead storage
5. Use production WSGI server (e.g., Gunicorn)

## Support
For questions or issues, contact the development team.
