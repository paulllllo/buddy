import os
import shutil
from typing import Optional, BinaryIO
from pathlib import Path
from app.config import settings
from app.storage.base import StorageInterface


class LocalStorage(StorageInterface):
    """Local file storage implementation"""
    
    def __init__(self):
        self.base_path = Path(settings.local_storage_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    async def upload_file(self, file_data: BinaryIO, filename: str, folder: str = "") -> str:
        """Upload a file to local storage"""
        # Create folder path
        folder_path = self.base_path / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        
        # Create full file path
        file_path = folder_path / filename
        
        # Save file
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file_data, f)
        
        # Return relative path
        return str(file_path.relative_to(self.base_path))
    
    async def download_file(self, file_path: str) -> Optional[BinaryIO]:
        """Download a file from local storage"""
        full_path = self.base_path / file_path
        
        if not full_path.exists():
            return None
        
        return open(full_path, "rb")
    
    async def delete_file(self, file_path: str) -> bool:
        """Delete a file from local storage"""
        full_path = self.base_path / file_path
        
        if full_path.exists():
            full_path.unlink()
            return True
        return False
    
    async def file_exists(self, file_path: str) -> bool:
        """Check if a file exists in local storage"""
        full_path = self.base_path / file_path
        return full_path.exists()
    
    def get_file_url(self, file_path: str) -> str:
        """Get the local file URL (for development)"""
        # In production, this would be a CDN or static file server URL
        return f"/files/{file_path}" 