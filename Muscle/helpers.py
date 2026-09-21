import os
import flet as ft
from datetime import datetime

EXTERNAL_DIR = r'/storage/sdcard0/Documents/muscle_app'

def write_log(message: str):
    """Append a timestamped line to log.txt in the external dir.
    Falls back to app-private storage if the external dir isn't writable,
    so a log always exists somewhere."""
    line = f"{datetime.now().isoformat(timespec='seconds')}  {message}\n"
    try:
        os.makedirs(EXTERNAL_DIR, exist_ok=True)
        with open(os.path.join(EXTERNAL_DIR, 'log.txt'), 'a') as f:
            f.write(line)
        return
    except Exception:
        pass
    try:  # fallback: app-private, always writable
        storage = os.getenv('FLET_APP_STORAGE_DATA')
        if storage:
            data_dir = os.path.join(storage, 'data')
            os.makedirs(data_dir, exist_ok=True)
            with open(os.path.join(data_dir, 'log.txt'), 'a') as f:
                f.write(line)
    except Exception:
        pass

def show_popup(page: ft.Page, title: str, message: str):
    """Show a dialog on the phone. Safe to call from anywhere with `page`."""
    if page is None:
        return
    dlg = ft.AlertDialog(
        title=ft.Text(title),
        content=ft.Container(
            content=ft.Column([ft.Text(message, selectable=True, size=12)],
                              scroll=ft.ScrollMode.AUTO, tight=True),
            width=400, height=300,   # scrolls, so long tracebacks stay readable
        ),
        actions=[ft.TextButton("OK", on_click=lambda e: page.close(dlg))],
    )
    page.open(dlg)