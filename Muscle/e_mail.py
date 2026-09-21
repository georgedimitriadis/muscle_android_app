
import os
import smtplib
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import flet as ft
import traceback
from helpers import write_log, show_popup

class EMail:
    def __init__(self, page: ft.Page, attachment):

        self.sender_email = 'george.dimitriadis.android@gmail.com'
        self.password ='jcmt tuxe wykt ytuk'
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = '587'
        self.receiver_email = self.sender_email

        self.subject = f'Muscle schedule completed on {str(datetime.now().date())}'
        self.body = ''

        self.page = page

    def send_email(self):
        try:
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = self.receiver_email
            message["Subject"] = self.subject
            message.attach(MIMEText(self.body, "plain"))

            storage_dir = os.getenv('FLET_APP_STORAGE_DATA')
            filename = os.path.join(storage_dir, 'data', 'schedule.json')
            with open(filename, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition",
                                f"attachment; filename={os.path.basename(filename)}")
                message.attach(part)

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.password)
                server.sendmail(self.sender_email, self.receiver_email,
                                message.as_string())

            write_log('[email] sent OK')
            #show_popup(self.page, 'Email sent', 'Schedule emailed successfully.')
            return True, 'Schedule emailed successfully.'
        except Exception:
            err = traceback.format_exc()
            write_log('[email] FAILED\n' + err)
            #show_popup(self.page, 'Email failed', err)
            return False, err

    def send_and_notify(self):
        body = ft.Text("Sending email…")
        close_btn = ft.TextButton("Close", disabled=True)
        dlg = ft.AlertDialog(
            title=ft.Text("Email"),
            content=ft.Container(
                content=ft.Column([body], scroll=ft.ScrollMode.AUTO, tight=True),
                width=400, height=200,
            ),
            actions=[close_btn],
        )
        close_btn.on_click = lambda _: self.page.close(dlg)
        self.page.open(dlg)  # "Sending email…" shows immediately

        def worker():
            ok, detail = self.send_email()
            body.value = "Schedule emailed successfully." if ok else detail
            dlg.title.value = "Email sent" if ok else "Email failed"
            close_btn.disabled = False
            self.page.update()

        threading.Thread(target=worker, daemon=True).start()