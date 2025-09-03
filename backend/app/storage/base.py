from abc import ABC, abstractmethod
from typing import Optional, BinaryIO
from pathlib import Path


class StorageInterface(ABC):
    """Abstract base class for file storage implementations"""
    
    @abstractmethod
    async def upload_file(self, file_data: BinaryIO, filename: str, folder: str = "") -> str:
        """Upload a file and return the URL/path"""
        pass
    
    @abstractmethod
    async def download_file(self, file_path: str) -> Optional[BinaryIO]:
        """Download a file and return file-like object"""
        pass
    
    @abstractmethod
    async def delete_file(self, file_path: str) -> bool:
        """Delete a file and return success status"""
        pass
    
    @abstractmethod
    async def file_exists(self, file_path: str) -> bool:
        """Check if a file exists"""
        pass
    
    @abstractmethod
    def get_file_url(self, file_path: str) -> str:
        """Get the public URL for a file"""
        pass 