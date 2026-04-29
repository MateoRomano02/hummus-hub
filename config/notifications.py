import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from config.settings import settings

logger = logging.getLogger(__name__)

def notify_error(agent_type: str, client_id: str, error_msg: str):
    """
    Sends an error notification email using Gmail SMTP.
    """
    if not all([settings.gmail_user, settings.gmail_app_password, settings.error_notify_email]):
        logger.warning("Notification skipped: SMTP configuration missing in .env")
        return False

    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = settings.gmail_user
        msg['To'] = settings.error_notify_email
        msg['Subject'] = f"🚨 ERROR CRÍTICO: {agent_type} - Hummus Hub"

        body = f"""
        <html>
        <body style="font-family: sans-serif;">
            <h2 style="color: #d32f2f;">Falla en Agente: {agent_type}</h2>
            <p>Se ha detectado un error crítico que requiere atención inmediata.</p>
            <hr>
            <p><strong>Cliente ID:</strong> {client_id}</p>
            <p><strong>Error:</strong> {error_msg}</p>
            <hr>
            <p style="font-size: 0.8em; color: #666;">Este es un mensaje automático de Hummus Hub Observability.</p>
        </body>
        </html>
        """
        msg.attach(MIMEText(body, 'html'))

        # Send email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(settings.gmail_user, settings.gmail_app_password)
            server.send_message(msg)
        
        logger.info(f"Notification sent successfully for {agent_type}")
        return True

    except Exception as e:
        logger.error(f"Failed to send notification: {str(e)}")
        return False
