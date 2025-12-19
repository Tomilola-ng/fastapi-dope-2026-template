"""Utils schemas"""

from typing import Optional

from pydantic import BaseModel, validator

from app.config.storage import r2_storage


class FileOut(BaseModel):
    """Public file metadata."""
    id: int
    key: str
    alt_text: Optional[str] = None
    url: Optional[str] = None

    class Config:
        """ORM config."""
        from_attributes = True

    @validator("url", pre=True, always=True)
    def generate_url(cls, v, values):
        """Generate URL from the key if not already provided"""
        if v is not None:
            return v

        # Get the key from values or from the original object
        key = values.get("key")
        if key:
            try:
                return r2_storage.generate_presigned_url(key, 604800)
            except Exception:
                return None
        return None
