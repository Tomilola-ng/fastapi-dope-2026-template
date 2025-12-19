"""R2 Storage Module"""

import os
import uuid
from typing import Optional

import boto3
from botocore.exceptions import ClientError
from fastapi import UploadFile

from app.config.settings import settings


class R2Storage:
    """Cloudflare R2 Storage Client"""

    def __init__(self):
        """Initialize R2 client"""
        self.s3_client = boto3.client(
            "s3",
            endpoint_url=settings.R2_ENDPOINT_URL,
            aws_access_key_id=settings.R2_ACCESS_KEY_ID,
            aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
            region_name="auto",  # R2 doesn't use regions but boto3 requires this
        )
        self.bucket_name = settings.R2_BUCKET_NAME
        self.public_url = settings.R2_PUBLIC_URL

    async def upload_file(
        self, file: UploadFile, folder: str = "uploads", filename: Optional[str] = None
    ) -> str:
        """Upload file to R2 storage

        Args:
            file: The file to upload
            folder: The folder to upload to (default: uploads)
            filename: Optional custom filename, if not provided a UUID will be generated

        Returns:
            The key/path of the uploaded file (NOT the full URL)
        """
        # Generate a unique filename if not provided
        if not filename:
            ext = os.path.splitext(file.filename)[1] if file.filename else ""
            filename = f"{uuid.uuid4()}{ext}"

        # Create the full path
        key = f"{folder}/{filename}"

        # Read file content
        content = await file.read()

        try:
            # Upload to R2
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=content,
                ContentType=file.content_type,
            )

            # Reset file cursor for potential further use
            await file.seek(0)

            # Return only the key, not the full URL
            return key

        except ClientError as e:
            raise Exception(f"Failed to upload file to R2: {str(e)}")

    def generate_presigned_url(self, key: str, expiration: int = 604800) -> str:
        """Generate a presigned URL for a file

        Args:
            key: The key/path of the file in R2
            expiration: URL expiration time in seconds (default: 7 days)

        Returns:
            Presigned URL string
        """
        try:
            response = self.s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket_name, "Key": key},
                ExpiresIn=expiration,
            )
            return response
        except ClientError as e:
            raise Exception(f"Failed to generate presigned URL: {str(e)}")

    def generate_presigned_urls(
        self, keys: list[str], expiration: int = 604800
    ) -> dict[str, str]:
        """Generate presigned URLs for multiple files

        Args:
            keys: List of keys/paths of files in R2
            expiration: URL expiration time in seconds (default: 7 days)

        Returns:
            Dictionary mapping keys to presigned URLs
        """
        urls = {}
        for key in keys:
            try:
                urls[key] = self.generate_presigned_url(key, expiration)
            except Exception:
                # If URL generation fails, skip this key
                continue
        return urls

    def delete_file(self, key: str) -> bool:
        """Delete file from R2 storage

        Args:
            key: The key/path of the file to delete

        Returns:
            True if deletion was successful, False otherwise
        """
        try:
            # Delete from R2
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=key)
            return True
        except ClientError:
            return False

    def file_exists(self, key: str) -> bool:
        """Check if file exists in R2

        Args:
            key: The key/path of the file to check

        Returns:
            True if file exists, False otherwise
        """
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=key)
            return True
        except ClientError:
            return False


# Create a singleton instance
r2_storage = R2Storage()
