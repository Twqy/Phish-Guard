# 🛡️ Phish Guard

Phish Guard is an AI-powered email security tool that helps detect phishing attempts using advanced machine learning. It analyzes email content, attachments, and can integrate directly with Gmail to scan your inbox.


## 🚀 Features

- 📧 Real-time email content analysis
- 📎 Image and PDF attachment scanning
- 🔍 Gmail inbox integration
- 🤖 AI-powered phishing detection
- 📊 Confidence scoring system
- 🎯 Suspicious phrase identification

https://github.com/Twqy/Phish-Guard/issues/2#issue-2873022745
https://github.com/Twqy/Phish-Guard/issues/1#issue-2873022581

## 🛠️ Technology Stack

### Frontend

- React.js
- Modern CSS
- Lucide React Icons

### Backend

- Python Flask
- OpenAI GPT-4o-mini
- Gmail API
- Tesseract OCR
- PyPDF2

## ⚙️ Prerequisites

- Node.js (v16+)
- Python (v3.8+)
- Tesseract OCR
- Google Cloud Platform account
- OpenAI API key

## 📥 Installation

### Backend Setup

```bash
# Navigate to backend directory
cd "Back end"

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo OPENAI_API_KEY=your_api_key_here > .env

# Install Tesseract OCR
winget install UB-Mannheim.TesseractOCR
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd "Front end"

# Install dependencies
npm install

# Start development server
npm start
```

### Gmail API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project
3. Enable Gmail API
4. Create OAuth 2.0 credentials
5. Download credentials.json to `/Back end/config/`

## 🚦 Running the Application

1. Start the backend server:

```bash
cd "Back end"
python app.py
```

2. Start the frontend (in a new terminal):

```bash
cd "Front end"
npm start
```

3. Access the application at `http://localhost:3000`

## 🔒 Security Notes

- Never commit `.env` files
- Keep your API keys private
- Store credentials.json securely
- Review file uploads carefully
- Monitor API usage and costs

## 💡 Usage

1. **Text Analysis**: Paste suspicious email content
2. **File Analysis**: Upload email screenshots or PDFs
3. **Gmail Integration**: Analyze recent emails directly
4. **Review Results**: Check confidence scores and suspicious elements

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for GPT-4o-mini
- Google Cloud Platform
- Tesseract OCR
