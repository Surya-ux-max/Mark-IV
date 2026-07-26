import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_smtp_email(to_email: str, subject: str, body_text: str) -> str:
    """
    Sends an email using Python's built-in smtplib and email packages.
    Sends from: suryapr.exe14@gmail.com
    If SMTP credentials are not found in .env, it runs in simulation mode,
    logging the payload to ensure complete testability.
    """
    from_email = "suryapr.exe14@gmail.com"
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER", "")
    smtp_pass = os.getenv("SMTP_PASS", "")

    # Create message container
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body_text, 'plain'))

    # If credentials are not present, log email details and simulate send
    if not smtp_user or not smtp_pass:
        sim_msg = (
            f"Email Tool [SIMULATION MODE]:\n"
            f"- From: {from_email}\n"
            f"- To: {to_email}\n"
            f"- Subject: {subject}\n"
            f"- Content: {body_text}\n"
            f"Note: Configure SMTP_USER and SMTP_PASS in .env to execute live sends."
        )
        print(sim_msg)
        return f"Email simulated successfully to {to_email}."

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        return f"Email sent successfully to {to_email}."
    except Exception as e:
        # Fallback explanation
        return (
            f"Email Tool Error: SMTP send failed ({e}).\n"
            f"Email content was: Subject: '{subject}' to {to_email}."
        )
