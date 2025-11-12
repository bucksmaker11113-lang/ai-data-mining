import smtplib, os
from email.mime.text import MIMEText

class ReportMailer:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", 465))
        self.smtp_user = os.getenv("SMTP_USER")
        self.smtp_pass = os.getenv("SMTP_PASS")
        self.to_email = os.getenv("REPORT_EMAIL", "bucksmaker11111@gmail.com")

    def send_report(self, subject, text):
        if not self.smtp_user or not self.smtp_pass:
            print("[Mailer WARNING] Nincs SMTP konfigurálva, e-mail nem küldve.")
            return False
        msg = MIMEText(text, "plain", "utf-8")
        msg["Subject"] = subject
        msg["From"] = f"AI Data Mining <{self.smtp_user}>"
        msg["To"] = self.to_email
        try:
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                server.login(self.smtp_user, self.smtp_pass)
                server.send_message(msg)
            print(f"[Mailer] Riport elküldve → {self.to_email}")
            return True
        except Exception as e:
            print("[Mailer ERROR]", e)
            return False
