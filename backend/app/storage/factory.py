from app.config import settings
from app.storage.local import LocalStorage
from app.storage.base import StorageInterface


def get_storage() -> StorageInterface:
    """Get the appropriate storage backend based on configuration"""
    if settings.file_storage_type == "local":
        return LocalStorage()
    elif settings.file_storage_type == "s3":
        # TODO: Implement S3 storage
        # from app.storage.s3 import S3Storage
        # return S3Storage()
        raise NotImplementedError("S3 storage not yet implemented")
    else:
        raise ValueError(f"Unsupported storage type: {settings.file_storage_type}") 