#!/usr/bin/env python3
"""
Django-style app generator for FastAPI projects.
Usage: python startapp.py <app_name> [--extended]
"""

import argparse
from pathlib import Path


# Template for services.py
SERVICES_TEMPLATE = '''"""{} services"""

from uuid import UUID
from fastapi import HTTPException, status
from tortoise.transactions import in_transaction

from app.{}.models import *
from app.{}.schemas import *


async def example_service_function(resource_id: UUID) -> dict:
    """
    Example service function.

    Args:
        resource_id: UUID of the resource

    Returns:
        dict containing the result

    Raises:
        HTTPException: If resource is not found
    """
    # TODO: Implement service logic
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Service not implemented."
    )
'''

# Template for models.py
MODELS_TEMPLATE = '''"""{} models"""

import uuid

from tortoise import fields, models


class ExampleModel(models.Model):
    """
    Table: {table_name}
    """

    id = fields.UUIDField(pk=True, default=uuid.uuid4)

    # TODO: Add your model fields here
    name = fields.CharField(max_length=255)
    
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        """Meta class for ExampleModel model"""
        table = "{table_name}"
        indexes = [
            ("name",),
        ]

    def __str__(self):
        return self.name
'''

# Template for schemas.py
SCHEMAS_TEMPLATE = '''"""{} schemas"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel, Field

from app.{}.models import ExampleModel


# Example Model Schemas
ExampleModelFullPydantic = pydantic_model_creator(
    ExampleModel, name="ExampleModelFull"
)
ExampleModelCreatePydantic = pydantic_model_creator(
    ExampleModel,
    name="ExampleModelCreate",
    exclude_readonly=True,
)


class ExampleModelRead(BaseModel):
    """Example model read schema."""
    id: UUID
    name: str
    updated_at: datetime

    class Config:
        """Pydantic model configuration"""
        from_attributes = True


class ExampleModelUpdate(BaseModel):
    """Schema for updating example model."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
'''

# Template for routes.py
ROUTES_TEMPLATE = '''"""{} Routes"""

from uuid import UUID

from fastapi import APIRouter, Depends, status, HTTPException

from app.{}.services import example_service_function
from app.{}.schemas import ExampleModelRead
from app.accounts.models import Account
from app.accounts.auth import get_current_user


router = APIRouter(prefix="/{}", tags=["{}"])


@router.get("/{{resource_id}}", response_model=ExampleModelRead, status_code=status.HTTP_200_OK)
async def get_resource(resource_id: UUID):
    """
    Get resource by ID.

    Args:
        resource_id: UUID of the resource

    Returns:
        Resource details
    """
    # TODO: Implement endpoint logic
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Endpoint not implemented."
    )
'''

# Template for emails.py
EMAILS_TEMPLATE = '''"""{} Email Templates"""

from typing import Dict

from app.base.email_template import base_email_template as base_template


def example_email(context: Dict) -> str:
    """
    Generate HTML email template for example email

    Args:
        context (dict): Contains template variables

    Returns:
        str: HTML formatted email content
    """
    content = f"""
        <h1>Example Email</h1>
        <p>Hello {{context.get('name', 'User')}},</p>
        <p>This is an example email template.</p>
        <p>Please customize this template to fit your needs.</p>
        """
    return base_template("Example Email", content)
'''

# Template for utils.py
UTILS_TEMPLATE = '''"""{} utilities"""

from uuid import UUID

from fastapi import HTTPException, status

from app.accounts.models import Account
from app.{}.models import ExampleModel


def example_utility_function(resource_id: UUID) -> ExampleModel:
    """
    Example utility function.

    Args:
        resource_id: UUID of the resource

    Returns:
        ExampleModel instance

    Raises:
        HTTPException: If resource is not found
    """
    # TODO: Implement utility logic
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Utility not implemented."
    )
'''

# Template for enums.py
ENUMS_TEMPLATE = '''"""{} enums"""

from enum import Enum


class ExampleEnum(str, Enum):
    """Example enum"""
    OPTION_ONE = "option_one"
    OPTION_TWO = "option_two"
'''

# Template for __init__.py (optional, but good practice)
INIT_TEMPLATE = '''"""{} module"""
'''


def generate_app(app_name: str, extended: bool = False):
    """
    Generate a new FastAPI app with boilerplate files.

    Args:
        app_name: Name of the app to create (lowercase, underscore-separated)
        extended: If True, also generate routes.py, emails.py, utils.py, enums.py
    """
    # Validate app name
    if not app_name.islower() or not app_name.replace('_', '').isalnum():
        print(
            f"Error: App name '{app_name}' must be lowercase and contain only letters, numbers, and underscores.")
        return

    # Get the app directory path
    base_dir = Path(__file__).parent
    app_dir = base_dir / "app" / app_name

    # Check if app already exists
    if app_dir.exists():
        print(f"Error: App '{app_name}' already exists at {app_dir}")
        return

    # Create app directory
    app_dir.mkdir(parents=True, exist_ok=False)
    print(f"Created directory: {app_dir}")

    # Generate module name for templates (capitalize first letter of each word)
    module_name = ' '.join(word.capitalize() for word in app_name.split('_'))
    table_name = app_name  # Use app_name as table name (can be customized)

    # Generate required files
    files_to_create = [
        ("services.py", SERVICES_TEMPLATE.format(module_name, app_name, app_name)),
        ("models.py", MODELS_TEMPLATE.format(module_name, table_name=table_name)),
        ("schemas.py", SCHEMAS_TEMPLATE.format(module_name, app_name)),
    ]

    # Add extended files if flag is set
    if extended:
        routes_prefix = app_name.replace('_', '-')
        routes_tag = module_name
        files_to_create.extend([
            ("routes.py", ROUTES_TEMPLATE.format(module_name,
             app_name, app_name, routes_prefix, routes_tag)),
            ("emails.py", EMAILS_TEMPLATE.format(module_name)),
            ("utils.py", UTILS_TEMPLATE.format(module_name, app_name)),
            ("enums.py", ENUMS_TEMPLATE.format(module_name)),
        ])

    # Write files
    for filename, content in files_to_create:
        file_path = app_dir / filename
        file_path.write_text(content, encoding='utf-8')
        print(f"Created file: {file_path}")

    print(f"\nSuccessfully created app '{app_name}'")
    if extended:
        print(
            f"  Created {len(files_to_create)} files (including extended files)")
    else:
        print(f"  Created {len(files_to_create)} files (required files only)")
        print(f"  Run with --extended flag to also create routes.py, emails.py, utils.py, enums.py")


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Generate a new FastAPI app with boilerplate files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python startapp.py my_app
  python startapp.py my_app --extended
  python startapp.py user_profiles -e
        """
    )
    parser.add_argument(
        "app_name",
        help="Name of the app to create (lowercase, underscore-separated)"
    )
    parser.add_argument(
        "-e", "--extended",
        action="store_true",
        help="Also generate routes.py, emails.py, utils.py, and enums.py"
    )

    args = parser.parse_args()
    generate_app(args.app_name, args.extended)


if __name__ == "__main__":
    main()
