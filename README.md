# Prime (Ecomm)

Simple Django e-commerce sample project containing a `prime_accessories` app.

## Quickstart

Prerequisites:
- Python 3.11+ (project uses Django 6.x in the venv)
- A virtual environment (recommended)

Setup (Windows PowerShell):

```powershell
cd "C:\Users\ADMIN\Desktop\Prime\Ecomm"
python -m venv myvenv
.\n+myvenv\Scripts\Activate.ps1
pip install -r requirements.txt  # if you maintain one; otherwise install Django
python manage.py migrate
python manage.py runserver
```

Media and static files:
- `media/` contains uploaded assets. Ensure `MEDIA_ROOT` is configured in settings.

Repository:
- Remote: https://github.com/banaye/Prime.git


License: MIT (change if needed)
