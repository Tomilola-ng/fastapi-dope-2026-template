"""Base Email Template"""

# pylint: disable=line-too-long

import datetime


def base_email_template(title: str, body: str) -> str:
    """
    Generate base HTML email template with common header, footer, and styling

    Args:
        body (str): The main content of the email
        title (str): The title of the email

    Returns:
        str: HTML formatted email content
    """
    year = datetime.datetime.now().year
    return f"""
    <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title> {title} | Fast_Template</title>
        <style>
            /* Reset styles for email clients */
            body, table, td, a, p, h1, h2, h3, h4, h5, h6 {{
            margin: 0;
            padding: 0;
            font-family: Arial, Helvetica, sans-serif;
            }}
            body {{
            background-color: #f4f4f4;
            padding: 20px;
            }}
            .email-container {{
            max-width: 600px;
            margin: 0 auto;
            background-color: #ffffff;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }}
            .header {{
            text-align: center;
            padding: 20px;
            background-color: #F9F9FB; /* Fast_Template brand color */
            color: #ffffff;
            }}
            .header img {{
            width: 203px; /* Scaled logo width (4060/20) */
            height: 59px; /* Scaled logo height (1180/20) */
            display: block;
            margin: 0 auto;
            }}
            .content {{
            padding: 20px;
            }}
            .footer {{
            text-align: center;
            padding: 20px;
            background-color: #f4f4f4;
            color: #666666;
            font-size: 12px;
            }}
            .footer a {{
            color: #1F0F70;
            text-decoration: none;
            }}
            h1, h2, h3 {{
            color: #333333;
            margin-bottom: 10px;
            }}
            p {{
            color: #333333;
            font-size: 16px;
            line-height: 1.5;
            margin-bottom: 15px;
            }}
            .muted {{
            color: #999999;
            font-size: 14px;
            }}
            .error {{
            background-color: #ffe6e6;
            border-left: 4px solid #d32f2f;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 4px;
            }}
            .success {{
            background-color: #e6ffed;
            border-left: 4px solid #2e7d32;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 4px;
            }}
            .notification {{
            background-color: #e3f2fd;
            border-left: 4px solid #1e88e5;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 4px;
            }}
            .warning {{
            background-color: #fff3e0;
            border-left: 4px solid #f57c00;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 4px;
            }}
            a {{
            color: #1F0F70;
            text-decoration: none;
            }}
            a:hover {{
            text-decoration: underline;
            }}
            @media only screen and (max-width: 600px) {{
            .email-container {{
                width: 100%;
                margin: 0;
            }}
            .header img {{
                width: 150px; /* Smaller logo for mobile */
                height: 44px;
            }}
            }}
        </style>
        </head>
        <body>
        <div class="email-container">
            <div class="header">
            <img src="https://public_image.com/Fast_Template-logo.png" alt="Fast_Template Logo">
            </div>
            <div class="content">
                {body}
            <p class="muted">If you have any questions, feel free to reach out to our support team at support@fast_template.com.</p>
            </div>
            <div class="footer">
            <p>&copy; {year} Fast_Template. All rights reserved.</p>
            <p><a href="https://fast_template.com">fast_template.com</a> | <a href="https://fast_template.com/privacy">Privacy Policy</a></p>
            </div>
        </div>
        </body>
        </html>
    """
