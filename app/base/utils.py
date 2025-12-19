"""Utility Code"""

# pylint: disable=broad-exception-caught, missing-timeout

import re
import json
import secrets
import requests

from app.config.settings import settings


ZEPTO_URL = "https://api.zeptomail.com/v1.1/email"


def send_email(subject: str, address: str, body: str):
    """Send an email and handle errors."""
    try:
        payload = json.dumps(
            {
                "from": {"address": "noreply@fast_template.com"},
                "to": [
                    {
                        "email_address": {
                            "address": address,
                            "name": address.split("@")[0],
                        }
                    }
                ],
                "subject": subject,
                "htmlbody": body,
            }
        )

        print("Body", body)

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": settings.ZEPTO_API_KEY,
        }

        dre = requests.request(
            "POST", ZEPTO_URL, headers=headers, data=payload)
        print("Email response :", dre)
    except Exception as e:
        print(f"Error sending email: {e}")
        return None


def generate_otp(length: int = 6) -> str:
    """
    Generate a random OTP of the specified length.

    Args:
        length (int): The length of the OTP. Defaults to 6.

    Returns:
        str: The generated OTP.
    """
    return "".join(secrets.choice("0123456789") for _ in range(length))


def generate_slug(text: str) -> str:
    """
    Generate a URL-friendly slug from the provided text.

    Args:
        text (str): The text to generate the slug from.

    Returns:
        str: The generated slug.
    """
    slug = text.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = slug.strip("-")
    # Ensure uniqueness or further processing if needed
    return slug
