"""
Email Notifier for Thesis Generation
Sends email notifications with chapter content and review reports
"""
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os


class EmailNotifier:
    def __init__(self, sender_email, sender_password, recipient_email):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.recipient_email = recipient_email
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
    
    
    def send_chapter_notification(self, chapter_name, md_file, docx_file=None, review_file=None):
        """Send email notification when a chapter is completed"""
        subject = f"✅ Thesis Chapter Complete: {chapter_name}"
        
        # Build email body
        body = f"""
Dear Researcher,

Your thesis chapter has been successfully generated!

Chapter: {chapter_name}
Generated at: {self._get_timestamp()}

The chapter is attached in both Markdown (.md) and DOCX (.docx) formats.
"""
        
        if review_file and os.path.exists(review_file):
            body += """
PEER REVIEW REPORT:
The consolidated peer review report for all sections in this chapter is also attached.
Please review the feedback from all three reviewers.
"""
        
        body += """
Best regards,
PhD Thesis Generator
"""
        
        attachments = [md_file]
        if docx_file and os.path.exists(docx_file):
            attachments.append(docx_file)
        if review_file and os.path.exists(review_file):
            attachments.append(review_file)
        
        return self._send_email(subject, body, attachments)
    
    def send_review_notification(self, section_name, review_file):
        """Send email notification with peer review report"""
        subject = f"📋 Peer Review Complete: {section_name}"
        
        body = f"""
Dear Researcher,

The peer review for your thesis section has been completed!

Section: {section_name}
Reviewed at: {self._get_timestamp()}

The review report is attached. Please review the feedback from all three reviewers.

Best regards,
PhD Thesis Generator
"""
        
        return self._send_email(subject, body, [review_file])
    
    def _send_email(self, subject, body, attachments=None):
        """Send email with attachments"""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.recipient_email
            msg['Subject'] = subject
            
            # Add body
            msg.attach(MIMEText(body, 'plain'))
            
            # Add attachments
            if attachments:
                for file_path in attachments:
                    if os.path.exists(file_path):
                        with open(file_path, 'rb') as f:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(f.read())
                            encoders.encode_base64(part)
                            part.add_header(
                                'Content-Disposition',
                                f'attachment; filename={os.path.basename(file_path)}'
                            )
                            msg.attach(part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            print(f"📧 Email sent: {subject}")
            return True
        
        except Exception as e:
            print(f"❌ Email failed: {e}")
            return False
    
    def _get_timestamp(self):
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
