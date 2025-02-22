# Phish Guard 🛡️

A real-time email phishing detection tool powered by AI. Upload any suspicious email and get instant analysis of its legitimacy, with detailed explanations of potential threats.

## Tech Stack

### Frontend

- React.js
- Lucide React Icons
- JavaScript ES6+
- CSS

### Backend

- Python Flask
- OpenAI gpt-4o-mini API
- Flask-CORS for cross-origin handling
- dotenv for environment management

### Features

- Real-time email analysis
- Confidence scoring system (0-100%)
- Detailed threat analysis
- Suspicious phrase highlighting
- Mobile-responsive design
- Clean, modern UI

## Installation

### Backend Setup

```bash
cd "Back end"
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate

pip install -r requirements.txt

# Create .env file
echo OPENAI_API_KEY=your_api_key_here > .env
```

### Frontend Setup

```bash
cd "Front end"
npm install
```

## Running the Application

1. Start the Flask backend:

```bash
cd "Back end"
python app.py
```

2. Start the React frontend:

```bash
cd "Front end"
npm start
```

Access the application at `http://localhost:3000`

## Prerequisites

- Node.js (v14+)
- Python (v3.8+)
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- npm or yarn package manager

## Security Note

- Never commit your `.env` file
- API keys should be kept secret
- This tool is for educational purposes
- Always verify results with other security measures

## License

MIT License

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open pull request
