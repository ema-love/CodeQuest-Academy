# PythonAnywhere Deployment Guide for CodeQuest Academy

## Steps to Deploy:

### 1. Create a PythonAnywhere Account
- Go to https://www.pythonanywhere.com/
- Sign up for a free account (or paid if needed)
- Verify your email

### 2. Upload Your Code
Option A: Using Git (Recommended)
```bash
# SSH into PythonAnywhere console and:
cd /home/YOUR_USERNAME
git clone https://github.com/YOUR_USERNAME/codequest-academy.git
cd codequest-academy
```

Option B: Upload Files Directly
- Use PythonAnywhere's file browser to upload your project files

### 3. Set Up Virtual Environment
In PythonAnywhere Web Console:
```bash
mkvirtualenv --python=/usr/bin/python3.9 codequest
pip install -r requirements.txt
```

### 4. Configure Web App
1. Go to **Web tab** → **Add a new web app**
2. Choose **Manual configuration**
3. Select **Python 3.9**
4. For **WSGI configuration file**, point to:
   `/home/YOUR_USERNAME/codequest-academy/wsgi.py`

### 5. Configure WSGI File
Edit the WSGI config file that PythonAnywhere creates and replace with your path to wsgi.py

### 6. Set Environment Variables
In **Web tab** → **Your Web App** → scroll down to "Virtualenv":
```
/home/YOUR_USERNAME/.virtualenvs/codequest
```

Add these environment variables in the PythonAnywhere dashboard:
- **SECRET_KEY**: Generate a random secret key
- **MENTOR_EMAIL**: mentor@codequest.local (or your email)
- **MENTOR_PASSWORD**: Your secure password

### 7. Database Setup
- SQLite database will be created automatically on first run
- File location: `/home/YOUR_USERNAME/codequest-academy/instance/codequest.db`

### 8. Reload Your Web App
- Go to **Web tab** and click the **Reload** button

### 9. Access Your App
Your app will be available at: `https://YOUR_USERNAME.pythonanywhere.com`

## Important Notes:

- For free accounts, your account must be active (visit the site at least once monthly)
- Free tier includes 100MB of storage and bandwidth limits
- Paid accounts have no bandwidth restrictions
- Static files (CSS, JS) are served separately - PythonAnywhere will auto-configure this
- Keep your SECRET_KEY safe and unique

## Troubleshooting:

1. **App not loading?** Check error log: **Web tab** → **Error log**
2. **Module import errors?** Verify virtualenv is active: `pip list`
3. **Database errors?** Check file permissions on `/instance/` directory
4. **Static files missing?** PythonAnywhere auto-detects them, but you may need to reload

## After Deployment:

1. Run seed command to populate initial data:
   ```bash
   python -m flask --app=app seed
   ```

2. Test login with allowed emails:
   - arinola.olayiwola@gmail.com
   - niniolayiwola12@gmail.com
   - Password: quest1234

3. Mentor account uses MENTOR_EMAIL and MENTOR_PASSWORD from environment variables

Good luck! 🚀
