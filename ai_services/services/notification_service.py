"""
Notification service for sending emails, SMS, and other communications
"""

import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, Optional
from core.config import get_settings

logger = logging.getLogger(__name__)


class NotificationService:
    """Service for sending various types of notifications"""

    def __init__(self):
        self.settings = get_settings()

    async def send_email(
        self, to_email: str, subject: str, body: str, is_html: bool = False
    ) -> bool:
        """
        Send an email notification

        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Email body content
            is_html: Whether body is HTML formatted

        Returns:
            bool: True if sent successfully, False otherwise
        """
        try:
            # Create message
            msg = MIMEMultipart()
            msg["From"] = self.settings.FROM_EMAIL
            msg["To"] = to_email
            msg["Subject"] = subject

            # Attach body
            mime_type = "html" if is_html else "plain"
            msg.attach(MIMEText(body, mime_type))

            # Send email
            with smtplib.SMTP(
                self.settings.SMTP_HOST, self.settings.SMTP_PORT
            ) as server:
                server.starttls()
                server.login(self.settings.SMTP_USERNAME, self.settings.SMTP_PASSWORD)
                server.send_message(msg)

            logger.info(f"Email sent successfully to {to_email}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}")
            return False

    async def send_sms(self, to_phone: str, message: str) -> bool:
        """
        Send an SMS notification using Twilio

        Args:
            to_phone: Recipient phone number
            message: SMS message content

        Returns:
            bool: True if sent successfully, False otherwise
        """
        try:
            # Import Twilio here to avoid dependency issues if not configured
            from twilio.rest import Client

            client = Client(
                self.settings.TWILIO_ACCOUNT_SID, self.settings.TWILIO_AUTH_TOKEN
            )

            message = client.messages.create(
                body=message, from_=self.settings.TWILIO_PHONE_NUMBER, to=to_phone
            )

            logger.info(f"SMS sent successfully to {to_phone}, SID: {message.sid}")
            return True

        except Exception as e:
            logger.error(f"Failed to send SMS to {to_phone}: {e}")
            return False

    def format_template(self, template: str, data: Dict[str, Any]) -> str:
        """
        Format a notification template with data

        Args:
            template: Template string with {key} placeholders
            data: Dictionary of values to substitute

        Returns:
            str: Formatted string
        """
        try:
            return template.format(**data)
        except KeyError as e:
            logger.error(f"Missing template key: {e}")
            return template

    async def send_emergency_alert(
        self,
        recipients: list,
        incident_type: str,
        location: str,
        urgency: str,
        instructions: str = "",
    ) -> Dict[str, Any]:
        """
        Send emergency alerts to multiple recipients

        Args:
            recipients: List of recipient contact info
            incident_type: Type of emergency
            location: Location of incident
            urgency: Urgency level
            instructions: Emergency instructions

        Returns:
            Dict containing send results
        """
        results = {"sent": 0, "failed": 0, "errors": []}

        # Create alert message
        subject = f"🚨 {urgency.upper()} EMERGENCY ALERT - {incident_type}"
        message = f"""
EMERGENCY ALERT

Type: {incident_type}
Location: {location}
Urgency: {urgency}

{instructions}

This is an automated alert from the Disaster Response Coordination System.
"""

        for recipient in recipients:
            try:
                contact = recipient.get("contact")
                phone = recipient.get("phone")

                # Send email if available
                if contact and "@" in contact:
                    success = await self.send_email(contact, subject, message)
                    if success:
                        results["sent"] += 1
                    else:
                        results["failed"] += 1
                        results["errors"].append(f"Email failed: {contact}")

                # Send SMS if available and urgent
                if phone and urgency.upper() in ["HIGH", "CRITICAL"]:
                    # Shorter message for SMS
                    sms_message = f"🚨 {urgency} EMERGENCY: {incident_type} at {location}. {instructions[:100]}..."
                    success = await self.send_sms(phone, sms_message)
                    if success:
                        results["sent"] += 1
                    else:
                        results["failed"] += 1
                        results["errors"].append(f"SMS failed: {phone}")

            except Exception as e:
                results["failed"] += 1
                results["errors"].append(f"Error processing recipient {recipient}: {e}")

        logger.info(
            f"Emergency alert sent: {results['sent']} successful, {results['failed']} failed"
        )
        return results

    async def send_status_update(
        self, recipients: list, incident_id: str, status: str, message: str
    ) -> bool:
        """
        Send status update notifications

        Args:
            recipients: List of recipients
            incident_id: Incident ID
            status: New status
            message: Update message

        Returns:
            bool: True if all sent successfully
        """
        subject = f"Incident Update - {incident_id}"
        email_body = f"""
Incident Status Update

Incident ID: {incident_id}
New Status: {status}

{message}

---
Disaster Response Coordination System
"""

        success_count = 0
        for recipient in recipients:
            contact = recipient.get("contact")
            if contact and "@" in contact:
                if await self.send_email(contact, subject, email_body):
                    success_count += 1

        return success_count == len(
            [r for r in recipients if r.get("contact") and "@" in r.get("contact", "")]
        )


# Global notification service instance
_notification_service: Optional[NotificationService] = None


def get_notification_service() -> NotificationService:
    """Get the global notification service instance"""
    global _notification_service
    if _notification_service is None:
        _notification_service = NotificationService()
    return _notification_service
