import smtplib
from email.message import EmailMessage
import os

def notify_error(agent_type: str, client_id: str, error: str):
    msg = EmailMessage()
    msg['Subject'] = f'[Hummus Brain] Error en {agent_type}'
    msg['From'] = 'brain@agenciahummus.com.ar'
    msg['To'] = os.getenv('ERROR_NOTIFY_EMAIL', 'mateo@ejemplo.com')
    msg.set_content(f'Agente: {agent_type}\nCliente: {client_id}\nError: {error}')
    
    gmail_user = os.getenv('GMAIL_USER')
    gmail_app_pwd = os.getenv('GMAIL_APP_PASSWORD')
    
    if not gmail_user or not gmail_app_pwd:
        print("No SMTP credentials configured. Error details:", error)
        return

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:
            s.login(gmail_user, gmail_app_pwd)
            s.send_message(msg)
    except Exception as e:
        print(f"Failed to send email notification: {e}")
