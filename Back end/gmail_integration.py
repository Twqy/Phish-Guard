import logging
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os.path
import base64
import email
import requests  # Added import for requests
from dotenv import load_dotenv  # Added import for dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()  # Load environment variables from .env file

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), 'config', 'credentials.json')
TOKEN_PATH = os.path.join(os.path.dirname(__file__), 'token.json')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')  # Load OpenAI API key from environment variable
OPENAI_API_URL = 'https://api.openai.com/v1/chat/completions'  # Added OpenAI API URL

if not OPENAI_API_KEY:
    logger.error("OpenAI API key not found in environment variables")
    raise ValueError("OpenAI API key not configured")

def get_gmail_service():
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, 
                SCOPES
            )
            # Remove explicit redirect_uri and let it handle automatically
            creds = flow.run_local_server(port=0)  # Changed to port=0 for dynamic port
        
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())
    
    logger.info("Gmail service initialized successfully")
    return build('gmail', 'v1', credentials=creds)

def fetch_recent_emails(service, max_emails=3):  # Changed default to 3
    results = service.users().messages().list(userId='me', maxResults=max_emails).execute()
    messages = results.get('messages', [])
    
    logger.info(f"Found {len(messages)} messages to process")
    
    emails = []
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
        email_data = parse_email(msg)
        emails.append(email_data)
        logger.info(f"Processed email: {email_data['subject'][:30]}...")  # Added logging
    
    return emails

def parse_email(msg):
    try:
        payload = msg['payload']
        headers = payload.get('headers', [])
        
        subject = next((header['value'] for header in headers if header['name'].lower() == 'subject'), 'No Subject')
        sender = next((header['value'] for header in headers if header['name'].lower() == 'from'), 'Unknown Sender')
        
        parts = [payload]
        content = ''
        
        while parts:
            part = parts.pop()
            if part.get('parts'):
                parts.extend(part['parts'])
            if part.get('body') and part['body'].get('data'):
                try:
                    decoded = base64.urlsafe_b64decode(part['body']['data'])
                    content += decoded.decode('utf-8', errors='ignore')
                except Exception as e:
                    content += f"[Error decoding content: {str(e)}]"
        
        return {
            'subject': subject,
            'sender': sender,
            'content': content or '[No content found]'
        }
    except Exception as e:
        return {
            'subject': 'Error parsing email',
            'sender': 'Error',
            'content': f'Error parsing email: {str(e)}'
        }

def analyze_email_with_ai(content):
    try:
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "gpt-4o-mini",  # Using the correct model name
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert at detecting phishing attempts in emails."
                },
                {
                    "role": "user",
                    "content": f"Analyze this email for phishing attempts:\n\n{content}"
                }
            ]
        }
        
        response = requests.post(OPENAI_API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            analysis = response.json()
            return {
                "confidence_score": 0.8,  # Example score
                "is_legit": True,
                "analysis": analysis['choices'][0]['message']['content'],
                "suspicious_phrases": []
            }
    except Exception as e:
        logger.error(f"Error in AI analysis: {str(e)}")
        return {
            "confidence_score": 0,
            "is_legit": False,
            "analysis": f"Error analyzing email: {str(e)}",
            "suspicious_phrases": []
        }

def test_email_fetch(service, max_emails=3):  # Changed default to 3
    try:
        emails = fetch_recent_emails(service, max_emails)
        if emails:
            analyzed_emails = []
            for email in emails:
                analysis = analyze_email_with_ai(email['content'])
                analyzed_emails.append({
                    'subject': email['subject'],
                    'sender': email['sender'],
                    'content': email['content'][:200] + '...' if len(email['content']) > 200 else email['content'],
                    'analysis': analysis
                })
            return {
                'status': 'success',
                'count': len(emails),
                'emails': analyzed_emails
            }
        return {'status': 'success', 'count': 0, 'message': 'No emails found'}
    except Exception as e:
        logger.error(f"Error in test_email_fetch: {str(e)}")
        return {'status': 'error', 'message': str(e)}