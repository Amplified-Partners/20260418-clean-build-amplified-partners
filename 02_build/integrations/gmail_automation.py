#!/usr/bin/env python3
"""
Gmail Automation - Clawd
Triages inbox, drafts responses, extracts action items
"""

import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Scopes: read, send, modify
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def get_gmail_service():
    """Authenticate and return Gmail API service"""
    creds = None
    token_path = os.path.expanduser('~/.openclaw/credentials/gmail_token.pickle')
    creds_path = os.path.expanduser('~/.openclaw/credentials/gmail_credentials.json')
    
    # Load existing token
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    
    # If no valid creds, refresh or get new
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # First time: needs credentials.json from Google Cloud Console
            if not os.path.exists(creds_path):
                print(f"ERROR: Missing {creds_path}")
                print("Download from: https://console.cloud.google.com/apis/credentials")
                return None
            
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save token for next time
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
    
    return build('gmail', 'v1', credentials=creds)

def list_unread_messages(service, max_results=50):
    """Get unread messages"""
    try:
        results = service.users().messages().list(
            userId='me',
            q='is:unread',
            maxResults=max_results
        ).execute()
        
        messages = results.get('messages', [])
        return messages
    except HttpError as error:
        print(f'Error: {error}')
        return []

def get_message_detail(service, msg_id):
    """Get full message details"""
    try:
        message = service.users().messages().get(
            userId='me',
            id=msg_id,
            format='full'
        ).execute()
        return message
    except HttpError as error:
        print(f'Error: {error}')
        return None

def triage_message(message):
    """
    Categorize message priority
    Returns: 'client', 'urgent', 'low', or 'spam'
    """
    headers = message['payload']['headers']
    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '')
    from_email = next((h['value'] for h in headers if h['name'] == 'From'), '')
    
    # Priority logic (customize based on patterns)
    if 'URGENT' in subject.upper() or 'ASAP' in subject.upper():
        return 'urgent'
    
    # Check for client domains (customize)
    client_domains = ['jesmondplumbing.co.uk']  # Add real client domains
    if any(domain in from_email for domain in client_domains):
        return 'client'
    
    # Spam indicators
    spam_keywords = ['unsubscribe', 'click here', 'limited time']
    if any(kw in subject.lower() for kw in spam_keywords):
        return 'spam'
    
    return 'low'

def main():
    """Run email triage"""
    service = get_gmail_service()
    if not service:
        return
    
    print("Fetching unread messages...")
    messages = list_unread_messages(service)
    
    if not messages:
        print("No unread messages.")
        return
    
    print(f"Found {len(messages)} unread messages")
    
    # Triage each message
    for msg in messages[:10]:  # Process first 10
        detail = get_message_detail(service, msg['id'])
        if detail:
            category = triage_message(detail)
            headers = detail['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            from_email = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
            
            print(f"\n[{category.upper()}] {subject}")
            print(f"From: {from_email}")

if __name__ == '__main__':
    main()
