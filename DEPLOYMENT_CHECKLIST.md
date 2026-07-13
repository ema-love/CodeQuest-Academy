# CodeQuest Academy - Deployment Checklist

## Pre-Deployment Checklist

- [x] Flask app configured for production
- [x] Requirements.txt includes all dependencies
- [x] WSGI entry point created (wsgi.py)
- [x] Environment variables documented (.env.example)
- [x] Database migrations prepared (SQLite)
- [x] Static files properly configured
- [x] Removed emojis (Font Awesome icons used instead)
- [x] Authentication configured (email whitelist + password)
- [x] Admin/mentor account setup

## Deployment Steps Summary

### Quick Start (PythonAnywhere)

1. **Sign up**: https://www.pythonanywhere.com/
2. **Clone or upload** your project
3. **Create virtualenv**: Python 3.9
4. **Install requirements**: `pip install -r requirements.txt`
5. **Create web app** and point WSGI to `/path/to/wsgi.py`
6. **Set environment variables**:
   - `SECRET_KEY` (generate random string)
   - `MENTOR_EMAIL` 
   - `MENTOR_PASSWORD`
7. **Reload web app**
8. **Visit** `https://YOUR_USERNAME.pythonanywhere.com`

## Configuration Reference

### Allowed Student Emails
- arinola.olayiwola@gmail.com
- niniolayiwola12@gmail.com

### Student Registration Password
- quest1234

### Max Students
- 2 concurrent students

### File Structure
```
codequest-academy/
├── app/
│   ├── __init__.py
│   ├── auth.py
│   ├── main.py
│   ├── mentor.py
│   ├── models.py
│   ├── seed.py
│   ├── extensions.py
│   ├── static/
│   │   ├── css/style.css
│   │   ├── js/app.js
│   │   └── uploads/  (user uploads)
│   └── templates/
│       ├── base.html
│       ├── login.html
│       ├── dashboard.html
│       ├── mission.html
│       ├── missions.html
│       ├── bonus.html
│       ├── graduation.html
│       ├── portfolio.html
│       ├── mentor.html
│       └── mentee.html
├── instance/
│   └── codequest.db (auto-created)
├── migrations/
├── wsgi.py (entry point)
├── run.py (local development)
├── requirements.txt
└── README.md
```

## Post-Deployment

1. Initialize database (first time):
   ```bash
   python -m flask --app=app seed
   ```

2. Test with allowed email:
   - Email: arinola.olayiwola@gmail.com
   - Password: quest1234

3. Mentor login:
   - Email: (from MENTOR_EMAIL env var)
   - Password: (from MENTOR_PASSWORD env var)

## Monitoring

- Check PythonAnywhere **Error log** if issues occur
- Free account: limited bandwidth, must stay active monthly
- Paid account: unlimited bandwidth, better for production

## Support

See DEPLOYMENT.md for detailed instructions
