def emailTemplate(otp):
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                color: #333333;
                background-color: #f4f4f4;
                padding: 20px;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                background-color: #ffffff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                text-align: center;
            }}
            .header {{
                color: #0056b3;
            }}
            .logo img {{
                width: 80px;
                height: auto;
                margin: 0 auto 20px;
            }}
            .otp-code {{
                font-size: 24px;
                font-weight: bold;
                color: #0056b3;
                margin: 20px 0;
                text-align: center;
            }}
            .footer {{
                margin-top: 30px;
                font-size: 12px;
                text-align: center;
                color: #888888;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo">
                <img src="{image_url}" alt="StudyBuddy Logo">
            </div>
            <h2 class="header">Welcome to StudyBuddy!</h2>
            <p>Dear User,</p>
            <p>Your One-Time Password (OTP) is here! Use the code below to complete your verification and join your friends and community in sharing thoughts and interests:</p>
            <div class="otp-code">{otp}</div>
            <p>This code is unique to you and valid only for a limited time. Keep it private for your security.</p>
            <p>We look forward to connecting with you soon!</p>
            <div class="footer">
                Best regards,<br>
                StudyBuddy Team
            </div>
        </div>
    </body>
    </html>
    """
    return html_template


image_url = "https://res.cloudinary.com/dkn1nxszi/image/upload/v1730020606/logo_hwwo1r.png"
