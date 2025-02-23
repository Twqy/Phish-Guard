import requests
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import json
from werkzeug.utils import secure_filename
import pytesseract
from PIL import Image
import PyPDF2
import io
from flask import send_from_directory
from gmail_integration import get_gmail_service, fetch_recent_emails, test_email_fetch

# Add near the top of your file
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load environment variables and initialize Flask
load_dotenv()
app = Flask(__name__)
CORS(app)

# Constants
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
MODEL_NAME = "gpt-4o-mini"  # Using the most cost-effective model
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return jsonify({"status": "API is running"})

@app.route('/test-api', methods=['GET'])
def test_api():
    try:
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        test_payload = {
            "model": MODEL_NAME,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": "Hello"
                }
            ]
        }
        
        response = requests.post(OPENAI_API_URL, json=test_payload, headers=headers)
        
        if response.status_code == 200:
            return jsonify({"status": "success", "message": "API key is valid"})
        else:
            return jsonify({
                "status": "error",
                "message": f"API key may be invalid. Status code: {response.status_code}"
            }), 400
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

def analyze_email_with_ai(content):
    try:
        headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
        payload = {
            "model": MODEL_NAME,
            "messages": [
                {
                    "role": "system",
                    "content": """You are an expert at detecting phishing attempts in emails and attachments. Analyze the content using these criteria:

                    1. Text Analysis:
                    - Check for suspicious phrases and urgency
                    - Look for grammatical errors
                    - Verify sender information
                    
                    2. URL Analysis:
                    - Check for suspicious or misspelled URLs
                    - Verify HTTPS usage
                    - Look for unusual redirects
                    
                    3. Attachment Analysis:
                    - Check for suspicious file names
                    - Analyze attachment content
                    - Look for embedded links or scripts
                    
                    Provide your analysis as JSON:
                    {
                        "analysis": "Detailed explanation including both email and attachments",
                        "confidence_score": 0.XX (1.0 = legitimate, 0.0 = phishing),
                        "suspicious_phrases": [
                            {
                                "text": "suspicious content found",
                                "reason": "detailed explanation",
                                "source": "email/filename"
                            }
                        ]
                    }"""
                },
                {"role": "user", "content": f"Analyze this content:\n\n{content}"}
            ],
            "response_format": { "type": "json_object" }
        }
        
        response = requests.post(OPENAI_API_URL, json=payload, headers=headers)
        response_json = response.json()
        gpt_analysis = json.loads(response_json["choices"][0]["message"]["content"])
        
        # Normalize confidence score
        confidence_score = float(gpt_analysis.get("confidence_score", 0))
        confidence_score = max(0, min(1, confidence_score))
        
        return {
            "analysis": gpt_analysis.get("analysis", "Analysis not provided"),
            "confidence_score": confidence_score,
            "is_legit": confidence_score > 0.5,
            "suspicious_phrases": gpt_analysis.get("suspicious_phrases", [])
        }
    except Exception as e:
        return {
            "error": str(e),
            "confidence_score": 0,
            "is_legit": False,
            "analysis": "Error processing analysis",
            "suspicious_phrases": []
        }

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_image(image_file):
    try:
        image = Image.open(image_file)
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        return f"Error extracting text from image: {str(e)}"

def extract_text_from_pdf(pdf_file):
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text.strip()
    except Exception as e:
        return f"Error extracting text from PDF: {str(e)}"

@app.route('/analyze-with-files', methods=['POST'])
def analyze_with_files():
    try:
        email_text = request.form.get('email', '')
        files = request.files.getlist('files')
        
        # Process uploaded files
        file_analysis = []
        combined_text = email_text + "\n\n"
        
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_content = ""
                
                # Extract text based on file type
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    file_content = extract_text_from_image(file)
                elif filename.lower().endswith('.pdf'):
                    file_content = extract_text_from_pdf(file)
                elif filename.lower().endswith('.txt'):
                    file_content = file.read().decode('utf-8')
                
                # Add file content to combined text
                combined_text += f"\nContent from {filename}:\n{file_content}\n"
                
                # Add file information to analysis
                file_analysis.append({
                    "filename": filename,
                    "type": file.content_type,
                    "content": file_content[:200] + "..." if len(file_content) > 200 else file_content,
                    "warning": "Caution: Suspicious file attachment detected" if filename.endswith(('.exe', '.bat', '.cmd')) else "File appears legitimate"
                })
        
        # Analyze combined text
        analysis_result = analyze_email_with_ai(combined_text) if combined_text.strip() else {}
        
        return jsonify({
            **analysis_result,
            "file_analysis": file_analysis
        })
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "confidence_score": 0,
            "is_legit": False,
            "analysis": "Error processing analysis",
            "suspicious_phrases": [],
            "file_analysis": []
        }), 500

@app.route('/analyze', methods=['POST'])
def analyze_email():
    email_text = request.json.get('email', '')
    if not email_text:
        return jsonify({
            'error': 'No email text provided',
            'confidence_score': 0,
            'is_legit': False,
            'analysis': 'No email content to analyze',
            'suspicious_phrases': []
        }), 400
    
    result = analyze_email_with_ai(email_text)
    return jsonify(result)

@app.route('/analyze-gmail', methods=['POST'])
def analyze_gmail():
    try:
        service = get_gmail_service()
        emails = fetch_recent_emails(service, max_emails=3)
        
        results = []
        for email in emails:
            analysis = analyze_email_with_ai(email['content'])
            results.append({
                'subject': email['subject'],
                'sender': email['sender'],
                'content': email['content'][:200] + '...' if len(email['content']) > 200 else email['content'],
                'analysis': analysis
            })
        
        return jsonify({
            'status': 'success',
            'count': len(results),
            'emails': results
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/test-ocr', methods=['GET'])
def test_ocr():
    try:
        version = pytesseract.get_tesseract_version()
        return jsonify({
            "status": "success",
            "version": str(version),
            "tesseract_path": pytesseract.pytesseract.tesseract_cmd
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "tesseract_path": pytesseract.pytesseract.tesseract_cmd
        })

@app.route('/test-gmail', methods=['GET'])
def test_gmail():
    try:
        service = get_gmail_service()
        profile = service.users().getProfile(userId='me').execute()
        return jsonify({
            "status": "success",
            "email": profile['emailAddress']
        })
    except Exception as e:
        # Here's where you return 500
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/test-gmail-fetch', methods=['GET'])
def test_gmail_fetch():
    try:
        service = get_gmail_service()
        result = test_email_fetch(service)
        return jsonify(result)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/test-config', methods=['GET'])
def test_config():
    return jsonify({
        "openai_key_configured": bool(OPENAI_API_KEY),
        "model_name": MODEL_NAME
    })

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                             'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.errorhandler(500)
def handle_500_error(e):
    return jsonify({
        'status': 'error',
        'message': str(e),
        'type': type(e).__name__,
        'details': {
            'file': e.__traceback__.tb_frame.f_code.co_filename,
            'line': e.__traceback__.tb_lineno
        }
    }), 500

if __name__ == '__main__':
    app.run(debug=True)