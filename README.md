# 🛡️ Phish Guard

AI-powered email phishing detection tool that analyzes emails and attachments for potential security threats.

## 🚀 Features

- Real-time email analysis with GPT-4o-mini
- Image and PDF text extraction
- Suspicious phrase detection
- Confidence scoring system
- File attachment analysis
- Modern, responsive UI

## 🛠️ Tech Stack

### Frontend

- React.js
- Custom CSS
- Lucide React Icons

### Backend

- Python Flask
- OpenAI GPT-4o-mini
- Tesseract OCR
- PyPDF2
- Flask-CORS

## 📋 Prerequisites

- Node.js (v14+)
- Python (v3.8+)
- OpenAI API key
- Tesseract OCR

## ⚙️ Installation

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

## 🚦 Running the Application

1. Start the backend server:

```bash
cd "Back end"
python app.py
```

2. In a new terminal, start the frontend:

```bash
cd "Front end"
npm start
```

3. Access the application at `http://localhost:3000`

## 🔒 Security Notes

- Never commit `.env` files
- Keep your API keys private
- Review file uploads carefully
- Monitor usage and costs

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open pull request

## 📜 License

MIT License
