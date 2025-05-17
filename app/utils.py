import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timezone
from app.models import RefreshToken, TokenBlocklist
from app import db
from app.models import PasswordResetToken

def send_password_reset_email(email, token):
    """
    Send password reset email with token
    
    NOTE: In a production environment, you would use a proper email service
    like SendGrid, Mailgun, AWS SES, etc. This is a simplified version
    for demonstration purposes.
    """
    # In development, just print the reset link
    reset_link = f"http://localhost:5011/reset-password?token={token}"
    print(f"Password reset link for {email}: {reset_link}")
    
    # Uncomment and configure for actual email sending
    """
    msg = MIMEMultipart()
    msg['From'] = 'noreply@yourapp.com'
    msg['To'] = email
    msg['Subject'] = 'Password Reset Request'
    
    body = f'''
    Hello,
    
    You have requested to reset your password. Please click the link below to reset your password:
    
    {reset_link}
    
    This link will expire in 24 hours.
    
    If you did not request a password reset, please ignore this email.
    
    Best regards,
    Your App Team
    '''
    
    msg.attach(MIMEText(body, 'plain'))
    
    # Configure your SMTP server
    server = smtplib.SMTP('smtp.yourprovider.com', 587)
    server.starttls()
    server.login('your_email@yourprovider.com', 'your_password')
    server.send_message(msg)
    server.quit()
    """


def cleanup_expired_tokens():
    """
    Clean up expired refresh tokens and reset tokens.
    This should be run periodically via a scheduler.
    """
    now = datetime.now(timezone.utc)
    
    # Delete expired refresh tokens
    expired_refresh = RefreshToken.query.filter(RefreshToken.expires_at < now).all()
    for token in expired_refresh:
        # Add to blocklist
        revoked = TokenBlocklist(
            jti=token.token,
            type='refresh',
            user_id=token.user_id
        )
        db.session.add(revoked)
        db.session.delete(token)
    
    # Delete expired password reset tokens
    expired_reset = PasswordResetToken.query.filter(
        PasswordResetToken.expires_at < now,
        PasswordResetToken.is_used == False
    ).all()
    for token in expired_reset:
        db.session.delete(token)
    
    db.session.commit()