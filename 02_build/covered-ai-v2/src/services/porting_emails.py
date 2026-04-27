"""
Porting Email Templates and Notifications

Sends email notifications for the porting workflow using Resend.
"""

import os
from typing import Optional
from datetime import datetime

# Try to import resend, fail gracefully if not installed
try:
    import resend
    RESEND_AVAILABLE = True
except ImportError:
    RESEND_AVAILABLE = False


RESEND_API_KEY = os.getenv("RESEND_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL", "Covered AI <hello@covered.ai>")


def _send_email(to: str, subject: str, html: str) -> bool:
    """Send email via Resend."""
    if not RESEND_AVAILABLE or not RESEND_API_KEY:
        print(f"[EMAIL MOCK] To: {to}, Subject: {subject}")
        return True
    
    try:
        resend.api_key = RESEND_API_KEY
        resend.Emails.send({
            "from": FROM_EMAIL,
            "to": to,
            "subject": subject,
            "html": html,
        })
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False


def send_porting_confirmation(
    to_email: str,
    account_holder_name: str,
    number_to_port: str,
    request_id: str,
    estimated_completion: str,
) -> bool:
    """Send porting request confirmation email."""
    
    subject = f"Porting Request Received - {number_to_port}"
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: #2563eb; color: white; padding: 30px; text-align: center; border-radius: 8px 8px 0 0; }}
            .content {{ background: #f9fafb; padding: 30px; border-radius: 0 0 8px 8px; }}
            .info-box {{ background: white; border: 1px solid #e5e7eb; border-radius: 8px; padding: 20px; margin: 20px 0; }}
            .step {{ display: flex; align-items: flex-start; margin: 15px 0; }}
            .step-number {{ background: #2563eb; color: white; width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: bold; margin-right: 12px; flex-shrink: 0; }}
            .step-text {{ flex: 1; }}
            .footer {{ text-align: center; margin-top: 30px; color: #6b7280; font-size: 14px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1 style="margin: 0;">Porting Request Received</h1>
            </div>
            <div class="content">
                <p>Hi {account_holder_name},</p>
                
                <p>We've received your request to transfer your phone number to Covered AI. Here's what you need to know:</p>
                
                <div class="info-box">
                    <p style="margin: 0;"><strong>Number:</strong> {number_to_port}</p>
                    <p style="margin: 10px 0 0 0;"><strong>Reference:</strong> {request_id}</p>
                    <p style="margin: 10px 0 0 0;"><strong>Estimated completion:</strong> {estimated_completion}</p>
                </div>
                
                <h3>What happens next</h3>
                
                <div class="step">
                    <div class="step-number">1</div>
                    <div class="step-text">We've generated your Letter of Authorization (LOA) and will submit it to your current provider.</div>
                </div>
                
                <div class="step">
                    <div class="step-number">2</div>
                    <div class="step-text">We'll set up temporary call forwarding so you don't miss any calls during the transfer.</div>
                </div>
                
                <div class="step">
                    <div class="step-number">3</div>
                    <div class="step-text">The transfer typically takes 5-10 business days. We'll email you with updates.</div>
                </div>
                
                <div class="step">
                    <div class="step-number">4</div>
                    <div class="step-text">Once complete, Gemma will start answering calls to your number automatically.</div>
                </div>
                
                <p style="margin-top: 30px;">If you have any questions, just reply to this email.</p>
                
                <p>Cheers,<br>The Covered AI Team</p>
            </div>
            <div class="footer">
                <p>Covered AI Limited<br>
                0800 COVERED | hello@covered.ai</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return _send_email(to_email, subject, html)


def send_porting_update(
    to_email: str,
    account_holder_name: str,
    number_to_port: str,
    request_id: str,
    status: str,
    message: str,
) -> bool:
    """Send porting status update email."""
    
    status_emoji = {
        "submitted": "📤",
        "in_progress": "⏳",
        "scheduled": "📅",
        "completed": "✅",
        "failed": "❌",
    }.get(status, "📋")
    
    subject = f"{status_emoji} Porting Update - {number_to_port}"
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: #2563eb; color: white; padding: 30px; text-align: center; border-radius: 8px 8px 0 0; }}
            .content {{ background: #f9fafb; padding: 30px; border-radius: 0 0 8px 8px; }}
            .status-box {{ background: white; border: 1px solid #e5e7eb; border-radius: 8px; padding: 20px; margin: 20px 0; text-align: center; }}
            .footer {{ text-align: center; margin-top: 30px; color: #6b7280; font-size: 14px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1 style="margin: 0;">Porting Update</h1>
            </div>
            <div class="content">
                <p>Hi {account_holder_name},</p>
                
                <p>Here's an update on your number transfer:</p>
                
                <div class="status-box">
                    <p style="font-size: 32px; margin: 0;">{status_emoji}</p>
                    <p style="font-size: 18px; font-weight: bold; margin: 10px 0;">{status.replace('_', ' ').title()}</p>
                    <p style="margin: 0; color: #6b7280;">{message}</p>
                </div>
                
                <p><strong>Number:</strong> {number_to_port}<br>
                <strong>Reference:</strong> {request_id}</p>
                
                <p>If you have any questions, just reply to this email.</p>
                
                <p>Cheers,<br>The Covered AI Team</p>
            </div>
            <div class="footer">
                <p>Covered AI Limited<br>
                0800 COVERED | hello@covered.ai</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return _send_email(to_email, subject, html)


def send_porting_complete(
    to_email: str,
    account_holder_name: str,
    number_to_port: str,
    request_id: str,
    dashboard_url: str = "https://app.covered.ai/dashboard",
) -> bool:
    """Send porting completion email."""
    
    subject = f"✅ Your number is now live! - {number_to_port}"
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: #059669; color: white; padding: 30px; text-align: center; border-radius: 8px 8px 0 0; }}
            .content {{ background: #f9fafb; padding: 30px; border-radius: 0 0 8px 8px; }}
            .success-box {{ background: #ecfdf5; border: 1px solid #a7f3d0; border-radius: 8px; padding: 20px; margin: 20px 0; text-align: center; }}
            .cta-button {{ display: inline-block; background: #2563eb; color: white; padding: 12px 24px; border-radius: 6px; text-decoration: none; font-weight: bold; margin-top: 20px; }}
            .footer {{ text-align: center; margin-top: 30px; color: #6b7280; font-size: 14px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1 style="margin: 0;">🎉 You're Live!</h1>
            </div>
            <div class="content">
                <p>Hi {account_holder_name},</p>
                
                <p>Great news! Your number has been successfully transferred to Covered AI.</p>
                
                <div class="success-box">
                    <p style="font-size: 24px; margin: 0;">📞 {number_to_port}</p>
                    <p style="margin: 10px 0 0 0; color: #059669; font-weight: bold;">Gemma is now answering your calls</p>
                </div>
                
                <p>From now on, every call to {number_to_port} will be answered by Gemma, your AI receptionist. She'll:</p>
                
                <ul>
                    <li>Answer calls 24/7</li>
                    <li>Capture caller details</li>
                    <li>Triage emergencies</li>
                    <li>Send you notifications</li>
                </ul>
                
                <p>You can view all your calls and manage your settings in your dashboard:</p>
                
                <p style="text-align: center;">
                    <a href="{dashboard_url}" class="cta-button">Open Dashboard</a>
                </p>
                
                <p style="margin-top: 30px;">Thanks for choosing Covered AI. We're excited to help your business grow!</p>
                
                <p>Cheers,<br>The Covered AI Team</p>
            </div>
            <div class="footer">
                <p>Covered AI Limited<br>
                0800 COVERED | hello@covered.ai</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return _send_email(to_email, subject, html)
