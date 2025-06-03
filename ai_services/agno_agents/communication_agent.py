# ai_services/agno_agents/communication_agent.py
import os
import logging
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from typing import Dict, List, Optional
from datetime import datetime
from core.database import supabase
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)


class CommunicationAgent(Agent):
    """AGNO Agent for managing notifications and communications"""

    def __init__(self):
        # Initialize AGNO Agent with OpenAI only
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError(
                "OPENAI_API_KEY environment variable is required for CommunicationAgent"
            )

        model = OpenAIChat(id="gpt-4o-mini", temperature=0.4, max_tokens=800)

        super().__init__(
            name="DisasterCommunicationAgent",
            model=model,
            description="AI agent for managing disaster response communications and notifications",
            instructions="""
You are a disaster response communication agent. Your job is to:
1. Generate appropriate messages for different stakeholders
2. Send notifications about task assignments and updates
3. Craft clear, empathetic, and actionable communications
4. Notify affected individuals about help status
5. Alert administrators about resource needs and system issues

Communication principles:
- Be clear, concise, and actionable
- Show empathy for those affected by disasters
- Provide specific next steps and contact information
- Include relevant details (location, time, resources)
- Maintain professional but caring tone
- Prioritize urgent communications

Message types:
- Task assignments to volunteers/responders
- Status updates to affected individuals
- Resource alerts to administrators
- System notifications for coordination
""",
            add_history_to_messages=True,
            num_history_responses=3,
            markdown=False,
        )
        self.version = "1.0.0"

        # Email configuration
        self.smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")

    def get_pending_notifications(self) -> List[Dict]:
        """Get pending notifications from database"""
        try:
            response = (
                supabase.table("notifications")
                .select("*")
                .eq("status", "pending")
                .order("created_at", desc=False)
                .execute()
            )
            return response.data if response.data else []
        except Exception as e:
            logger.error(f"Failed to fetch pending notifications: {e}")
            return []

    def get_new_assignments(self) -> List[Dict]:
        """Get newly assigned tasks that need notification"""
        try:
            response = (
                supabase.table("tasks")
                .select("*, requests(*), users(*)")
                .eq("status", "assigned")
                .is_("notification_sent", "null")
                .execute()
            )
            return response.data if response.data else []
        except Exception as e:
            logger.error(f"Failed to fetch new assignments: {e}")
            return []

    def get_status_updates(self) -> List[Dict]:
        """Get requests with status updates that need communication"""
        try:
            response = (
                supabase.table("requests")
                .select("*, users(*)")
                .in_("status", ["assigned", "in_progress", "completed"])
                .eq("status_notification_sent", False)
                .execute()
            )
            return response.data if response.data else []
        except Exception as e:
            logger.error(f"Failed to fetch status updates: {e}")
            return []

    def generate_message(self, message_type: str, context: Dict) -> Dict:
        """Generate appropriate message using AI"""
        try:
            ai_prompt = f"""
Generate a professional, empathetic communication message for disaster response.

MESSAGE TYPE: {message_type}
CONTEXT: {context}

Requirements:
- Clear and actionable language
- Empathetic tone appropriate for disaster response
- Include all relevant details (time, location, contact info)
- Professional but caring approach
- Specific next steps for recipient

Generate a JSON response:
{{
    "subject": "Email subject line",
    "message": "Full message content",
    "urgency": "high/medium/low",
    "call_to_action": "specific action needed from recipient",
    "contact_info": "relevant contact information"
}}

Message types and guidelines:
- task_assignment: Clear instructions, timeline, resources, contact info
- status_update: Current status, next steps, estimated timeline
- resource_alert: Current situation, immediate needs, action required
- completion_notice: What was accomplished, next steps if any
"""

            # Get AI response
            response = self.run(ai_prompt)
            ai_result = (
                response.content if hasattr(response, "content") else str(response)
            )

            # Parse AI response
            import json

            try:
                message_data = json.loads(ai_result)
                return message_data
            except json.JSONDecodeError:
                # Fallback to basic message
                return {
                    "subject": f"Disaster Response: {message_type.replace('_', ' ').title()}",
                    "message": f"Update regarding your disaster response {message_type.replace('_', ' ')}.",
                    "urgency": "medium",
                    "call_to_action": "Please check your dashboard for details.",
                    "contact_info": "Contact support if you need assistance.",
                }

        except Exception as e:
            logger.error(f"Failed to generate message: {e}")
            return {
                "subject": "Disaster Response Update",
                "message": "Please check your dashboard for the latest updates.",
                "urgency": "medium",
                "call_to_action": "Check dashboard",
                "contact_info": "Contact support for assistance.",
            }

    def send_email(self, to_email: str, subject: str, message: str) -> bool:
        """Send email notification"""
        try:
            if not self.smtp_user or not self.smtp_password:
                logger.warning("SMTP credentials not configured, skipping email")
                return False

            # Create message
            msg = MIMEMultipart()
            msg["From"] = self.smtp_user
            msg["To"] = to_email
            msg["Subject"] = subject

            # Add body
            msg.attach(MIMEText(message, "plain"))

            # Send email
            server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            server.starttls()
            server.login(self.smtp_user, self.smtp_password)

            text = msg.as_string()
            server.sendmail(self.smtp_user, to_email, text)
            server.quit()

            logger.info(f"Email sent successfully to {to_email}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}")
            return False

    def process_task_assignments(self, assignments: List[Dict]) -> List[Dict]:
        """Process new task assignment notifications"""
        notifications = []

        for assignment in assignments:
            try:
                # Get assignee email
                assignee_email = assignment.get("users", {}).get("email", "")
                if not assignee_email:
                    continue

                # Prepare context
                context = {
                    "assignee_name": assignment.get("users", {}).get(
                        "name", "Volunteer"
                    ),
                    "task_title": assignment.get("title", ""),
                    "task_description": assignment.get("description", ""),
                    "priority": assignment.get("priority", "medium"),
                    "location": assignment.get("location", ""),
                    "special_instructions": assignment.get("special_instructions", ""),
                    "request_description": assignment.get("requests", {}).get(
                        "description", ""
                    ),
                    "estimated_duration": assignment.get("estimated_duration", ""),
                }

                # Generate message
                message_data = self.generate_message("task_assignment", context)

                # Send email
                email_sent = self.send_email(
                    assignee_email,
                    message_data.get("subject", "Task Assignment"),
                    message_data.get("message", "You have been assigned a new task."),
                )

                # Create notification record
                notification = {
                    "id": f"notif_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{assignment.get('id')}",
                    "type": "task_assignment",
                    "recipient_email": assignee_email,
                    "recipient_id": assignment.get("assignee_id"),
                    "task_id": assignment.get("id"),
                    "subject": message_data.get("subject"),
                    "message": message_data.get("message"),
                    "urgency": message_data.get("urgency", "medium"),
                    "status": "sent" if email_sent else "failed",
                    "sent_at": datetime.utcnow().isoformat() if email_sent else None,
                    "created_at": datetime.utcnow().isoformat(),
                }

                notifications.append(notification)

                # Update task to mark notification as sent
                if email_sent:
                    supabase.table("tasks").update(
                        {
                            "notification_sent": True,
                            "notification_sent_at": datetime.utcnow().isoformat(),
                        }
                    ).eq("id", assignment.get("id")).execute()

            except Exception as e:
                logger.error(f"Failed to process assignment notification: {e}")

        return notifications

    def process_status_updates(self, updates: List[Dict]) -> List[Dict]:
        """Process status update notifications"""
        notifications = []

        for update in updates:
            try:
                # Get requester email
                requester_email = update.get("users", {}).get("email", "")
                if not requester_email:
                    continue

                # Prepare context
                context = {
                    "requester_name": update.get("users", {}).get("name", ""),
                    "request_title": update.get("title", ""),
                    "current_status": update.get("status", ""),
                    "priority": update.get("priority", "medium"),
                    "location": update.get("location", ""),
                    "assigned_at": update.get("assigned_at", ""),
                    "description": update.get("description", ""),
                }

                # Generate message
                message_data = self.generate_message("status_update", context)

                # Send email
                email_sent = self.send_email(
                    requester_email,
                    message_data.get("subject", "Request Status Update"),
                    message_data.get(
                        "message", "Your request status has been updated."
                    ),
                )

                # Create notification record
                notification = {
                    "id": f"notif_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{update.get('id')}",
                    "type": "status_update",
                    "recipient_email": requester_email,
                    "recipient_id": update.get("reporter_id"),
                    "request_id": update.get("id"),
                    "subject": message_data.get("subject"),
                    "message": message_data.get("message"),
                    "urgency": message_data.get("urgency", "medium"),
                    "status": "sent" if email_sent else "failed",
                    "sent_at": datetime.utcnow().isoformat() if email_sent else None,
                    "created_at": datetime.utcnow().isoformat(),
                }

                notifications.append(notification)

                # Update request to mark notification as sent
                if email_sent:
                    supabase.table("requests").update(
                        {
                            "status_notification_sent": True,
                            "status_notification_sent_at": datetime.utcnow().isoformat(),
                        }
                    ).eq("id", update.get("id")).execute()

            except Exception as e:
                logger.error(f"Failed to process status update notification: {e}")

        return notifications

    def save_notifications_to_db(self, notifications: List[Dict]) -> bool:
        """Save notification records to database"""
        try:
            if notifications:
                response = (
                    supabase.table("notifications").insert(notifications).execute()
                )

                if response.data:
                    logger.info(f"Saved {len(notifications)} notifications to database")
                    return True
                else:
                    logger.error("Failed to save notifications to database")
                    return False
            return True

        except Exception as e:
            logger.error(f"Failed to save notifications: {e}")
            return False

    def run_communication_cycle(self) -> Dict:
        """Run a complete communication cycle"""
        try:
            # Get new assignments
            new_assignments = self.get_new_assignments()
            assignment_notifications = self.process_task_assignments(new_assignments)

            # Get status updates
            status_updates = self.get_status_updates()
            status_notifications = self.process_status_updates(status_updates)

            # Combine all notifications
            all_notifications = assignment_notifications + status_notifications

            # Save to database
            saved = self.save_notifications_to_db(all_notifications)

            result = {
                "status": "completed",
                "assignment_notifications": len(assignment_notifications),
                "status_notifications": len(status_notifications),
                "total_notifications": len(all_notifications),
                "notifications_saved": saved,
                "timestamp": datetime.utcnow().isoformat(),
            }

            logger.info(f"Communication cycle completed: {result}")
            return result

        except Exception as e:
            logger.error(f"Communication cycle failed: {e}")
            return {"status": "failed", "error": str(e)}

    def send_resource_alert(
        self, resource_type: str, current_stock: int, threshold: int, location: str
    ) -> bool:
        """Send resource shortage alert to administrators"""
        try:
            # Get admin users
            response = (
                supabase.table("users")
                .select("email, name")
                .eq("role", "admin")
                .execute()
            )

            admins = response.data if response.data else []

            if not admins:
                logger.warning("No admin users found for resource alert")
                return False

            # Generate alert message
            context = {
                "resource_type": resource_type,
                "current_stock": current_stock,
                "threshold": threshold,
                "location": location,
                "shortage_amount": threshold - current_stock,
            }

            message_data = self.generate_message("resource_alert", context)

            # Send to all admins
            notifications_sent = 0
            for admin in admins:
                admin_email = admin.get("email", "")
                if admin_email:
                    email_sent = self.send_email(
                        admin_email,
                        f"URGENT: Low Resource Alert - {resource_type}",
                        message_data.get(
                            "message",
                            f"Low stock alert for {resource_type} at {location}",
                        ),
                    )
                    if email_sent:
                        notifications_sent += 1

            logger.info(f"Resource alert sent to {notifications_sent} administrators")
            return notifications_sent > 0

        except Exception as e:
            logger.error(f"Failed to send resource alert: {e}")
            return False


# Standalone functions for backward compatibility
def send_communications() -> Dict:
    """Run communication cycle for all pending notifications"""
    agent = CommunicationAgent()
    return agent.run_communication_cycle()


def send_custom_notification(recipient_email: str, subject: str, message: str) -> bool:
    """Send a custom notification"""
    try:
        agent = CommunicationAgent()
        return agent.send_email(recipient_email, subject, message)
    except Exception as e:
        logger.error(f"Failed to send custom notification: {e}")
        return False


def alert_low_resources(
    resource_type: str, current_stock: int, threshold: int, location: str
) -> bool:
    """Send low resource alert to administrators"""
    try:
        agent = CommunicationAgent()
        return agent.send_resource_alert(
            resource_type, current_stock, threshold, location
        )
    except Exception as e:
        logger.error(f"Failed to send resource alert: {e}")
        return False
