"""Utils models"""

from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

from app.config.storage import r2_storage


class FileAsset(models.Model):
    """File model"""

    id = fields.IntField(pk=True)
    key = fields.CharField(max_length=255)  # R2 key/path
    alt_text = fields.CharField(max_length=255, null=True)
    content_type = fields.CharField(max_length=100, null=True)
    file_size = fields.IntField(null=True)

    def get_url(self, expiration: int = 604800) -> str:
        """Generate a presigned URL for the file asset.

        Args:
            expiration (int): Time in seconds until the URL expires. Defaults to 604800 (7 days).

        Returns:
            str: The presigned URL for accessing the file.
        """
        return r2_storage.generate_presigned_url(self.key, expiration)


FileAsset_Pydantic = pydantic_model_creator(FileAsset, name="FileAsset")
