"""
Google Drive Sync for Voice AI System
======================================
Syncs local transcripts and insights to Google Drive.

Folder structure on Drive:
/VoiceAI/
  /transcripts/raw/      - Raw daily transcripts
  /transcripts/processed/ - (reserved for future use)
  /insights/daily/       - Daily extracted insights
  /insights/weekly/      - Weekly summaries (future)

Built: December 6th, 2025
"""

import os
import pickle
from pathlib import Path
from datetime import datetime

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


# Scopes needed for Drive access
SCOPES = ['https://www.googleapis.com/auth/drive.file']


class DriveSync:
    """
    Sync local files to Google Drive.
    """
    
    def __init__(self, credentials_path: str = "credentials.json", token_path: str = "token.pickle"):
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.service = None
        self.folder_ids = {}  # Cache folder IDs
    
    def authenticate(self):
        """
        Authenticate with Google Drive API.
        """
        creds = None
        
        # Load existing token
        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token:
                creds = pickle.load(token)
        
        # Refresh or get new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_path):
                    raise FileNotFoundError(
                        f"Missing {self.credentials_path}. "
                        "Download from Google Cloud Console."
                    )
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES
                )
                creds = flow.run_local_server(port=0)
            
            # Save token
            with open(self.token_path, 'wb') as token:
                pickle.dump(creds, token)
        
        self.service = build('drive', 'v3', credentials=creds)
        print("✅ Authenticated with Google Drive")
    
    def get_or_create_folder(self, folder_name: str, parent_id: str = None) -> str:
        """
        Get folder ID, creating if it doesn't exist.
        """
        cache_key = f"{parent_id or 'root'}/{folder_name}"
        
        if cache_key in self.folder_ids:
            return self.folder_ids[cache_key]
        
        # Search for existing folder
        query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        if parent_id:
            query += f" and '{parent_id}' in parents"
        
        results = self.service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name)'
        ).execute()
        
        files = results.get('files', [])
        
        if files:
            folder_id = files[0]['id']
        else:
            # Create folder
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            if parent_id:
                file_metadata['parents'] = [parent_id]
            
            folder = self.service.files().create(
                body=file_metadata,
                fields='id'
            ).execute()
            folder_id = folder['id']
            print(f"📁 Created folder: {folder_name}")
        
        self.folder_ids[cache_key] = folder_id
        return folder_id
    
    def ensure_folder_structure(self) -> dict:
        """
        Create the full folder structure if needed.
        Returns dict of folder paths to IDs.
        """
        # Root folder
        voice_ai = self.get_or_create_folder("VoiceAI")
        
        # Transcripts
        transcripts = self.get_or_create_folder("transcripts", voice_ai)
        transcripts_raw = self.get_or_create_folder("raw", transcripts)
        transcripts_processed = self.get_or_create_folder("processed", transcripts)
        
        # Insights
        insights = self.get_or_create_folder("insights", voice_ai)
        insights_daily = self.get_or_create_folder("daily", insights)
        insights_weekly = self.get_or_create_folder("weekly", insights)
        
        return {
            "root": voice_ai,
            "transcripts/raw": transcripts_raw,
            "transcripts/processed": transcripts_processed,
            "insights/daily": insights_daily,
            "insights/weekly": insights_weekly
        }
    
    def upload_file(self, local_path: Path, drive_folder_id: str, update_existing: bool = True) -> str:
        """
        Upload a file to Drive folder.
        Returns file ID.
        """
        file_name = local_path.name
        
        # Check if file exists
        if update_existing:
            query = f"name='{file_name}' and '{drive_folder_id}' in parents and trashed=false"
            results = self.service.files().list(
                q=query,
                spaces='drive',
                fields='files(id)'
            ).execute()
            
            existing = results.get('files', [])
            
            if existing:
                # Update existing file
                media = MediaFileUpload(str(local_path), resumable=True)
                file = self.service.files().update(
                    fileId=existing[0]['id'],
                    media_body=media
                ).execute()
                print(f"📝 Updated: {file_name}")
                return file['id']
        
        # Upload new file
        file_metadata = {
            'name': file_name,
            'parents': [drive_folder_id]
        }
        media = MediaFileUpload(str(local_path), resumable=True)
        file = self.service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        print(f"📤 Uploaded: {file_name}")
        return file['id']
    
    def sync_directory(self, local_dir: Path, drive_folder_id: str):
        """
        Sync all files in local directory to Drive folder.
        """
        if not local_dir.exists():
            print(f"⚠️ Local directory doesn't exist: {local_dir}")
            return
        
        for file_path in local_dir.glob("*.md"):
            self.upload_file(file_path, drive_folder_id)
    
    def sync_all(self, local_base: str = "."):
        """
        Sync all transcripts and insights to Drive.
        """
        local_base = Path(local_base)
        
        print("\n🔄 Syncing to Google Drive...")
        
        # Ensure structure
        folders = self.ensure_folder_structure()
        
        # Sync transcripts
        self.sync_directory(
            local_base / "transcripts" / "raw",
            folders["transcripts/raw"]
        )
        
        # Sync insights
        self.sync_directory(
            local_base / "insights" / "daily",
            folders["insights/daily"]
        )
        
        print("✅ Sync complete\n")


def main():
    """
    Run sync to Google Drive.
    """
    sync = DriveSync()
    sync.authenticate()
    sync.sync_all()


if __name__ == "__main__":
    main()
