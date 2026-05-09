# Production Deployment

## 1. Environment

Copy `.env.example` to `.env` and set real values:

- `SECRET_KEY`: long random value
- `SESSION_COOKIE_SECURE=true` behind HTTPS
- `ENABLE_HSTS=true` behind HTTPS
- database credentials with a limited MySQL user

Do not use Flask `debug=True` in production.

## 2. Install

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 3. Run on Windows

```powershell
waitress-serve --host=0.0.0.0 --port=5000 wsgi:app
```

Place IIS, Nginx, Apache, or a load balancer in front of Waitress for HTTPS termination.

## 4. Run on Linux

```bash
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
```

If using Linux, add `gunicorn` to requirements.

## 5. Security Checklist

- Use HTTPS only.
- Set `SESSION_COOKIE_SECURE=true`.
- Rotate `SECRET_KEY` if leaked.
- Use strong passwords for superadmin, tenant admins, customer portal accounts, and MySQL.
- Restrict `/gps/webhook/<api_key>` keys per device and rotate if exposed.
- Back up MySQL and the `uploads/` directory.
- Keep `.env`, database dumps, and uploaded documents out of source control.
- Run behind a reverse proxy with request body limits for uploads.
