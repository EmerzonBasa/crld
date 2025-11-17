# CRL Filing System - Complete Installation Guide

## 📋 Table of Contents
1. [System Requirements](#system-requirements)
2. [Installation Steps](#installation-steps)
3. [Configuration](#configuration)
4. [Email Setup](#email-setup)
5. [Testing](#testing)
6. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, Linux, macOS
- **RAM**: 4GB (8GB recommended)
- **Storage**: 500MB for application + space for documents
- **Python**: 3.7 or higher
- **MySQL**: 5.7 or higher (included in XAMPP)
- **Browser**: Chrome 90+, Firefox 88+, Edge 90+, Safari 14+

### Required Software
1. XAMPP (includes Apache, MySQL, PHP)
2. Python 3.7+
3. pip (Python package manager)
4. Web browser

---

## Installation Steps

### Step 1: Install XAMPP

#### Windows
1. Download XAMPP from: https://www.apachefriends.org/download.html
2. Run the installer (xampp-windows-x64-installer.exe)
3. Choose installation directory (default: C:\xampp)
4. Select components: Apache, MySQL, PHP, phpMyAdmin
5. Complete installation
6. Open XAMPP Control Panel
7. Click **Start** buttons for Apache and MySQL

#### Linux
```bash
# Download and install
wget https://www.apachefriends.org/xampp-files/8.2.12/xampp-linux-x64-8.2.12-0-installer.run
chmod +x xampp-linux-x64-8.2.12-0-installer.run
sudo ./xampp-linux-x64-8.2.12-0-installer.run

# Start services
sudo /opt/lampp/lampp start
```

#### macOS
1. Download XAMPP for macOS
2. Open the .dmg file
3. Drag XAMPP to Applications
4. Open XAMPP Manager
5. Start Apache and MySQL

**Verify Installation:**
- Open browser: http://localhost/
- You should see XAMPP welcome page
- Open: http://localhost/phpmyadmin
- You should see phpMyAdmin interface

---

### Step 2: Setup Database

#### Method 1: Using phpMyAdmin (Recommended)
1. Open http://localhost/phpmyadmin
2. Click **New** in left sidebar
3. Database name: `crl_filing_system`
4. Collation: `utf8mb4_general_ci`
5. Click **Create**
6. Click on `crl_filing_system` database
7. Click **Import** tab
8. Click **Choose File**
9. Navigate to `crl_filing_system/database/schema.sql`
10. Click **Go** button at bottom
11. Wait for "Import has been successfully finished"

#### Method 2: Using MySQL Command Line
```bash
# Windows (in XAMPP installation directory)
cd C:\xampp\mysql\bin
mysql -u root -p

# Linux/Mac
mysql -u root -p

# Then in MySQL prompt:
CREATE DATABASE crl_filing_system CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE crl_filing_system;
SOURCE /path/to/crl_filing_system/database/schema.sql;
EXIT;
```

**Verify Database:**
1. In phpMyAdmin, select `crl_filing_system` database
2. Check tables exist: users, companies, documents, etc.
3. Check companies table has 4 rows (LOYOLA, CARITAS, PPLIC, ETERNAL)
4. Check users table has 1 row (admin user)

---

### Step 3: Install Python

#### Windows
1. Download Python from: https://www.python.org/downloads/
2. Run installer
3. ✅ **IMPORTANT**: Check "Add Python to PATH"
4. Click "Install Now"
5. Wait for completion

**Verify:**
```cmd
python --version
pip --version
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip
python3 --version
pip3 --version
```

#### macOS
```bash
# Using Homebrew
brew install python3
python3 --version
pip3 --version
```

---

### Step 4: Install CRL Filing System

#### Extract Files
1. Extract `crl_filing_system.zip` to desired location
2. Example: `C:\Projects\crl_filing_system` (Windows)
3. Example: `/home/user/crl_filing_system` (Linux)
4. Example: `/Users/user/crl_filing_system` (macOS)

#### Install Python Dependencies
```bash
# Navigate to project directory
cd crl_filing_system

# Windows
pip install -r requirements.txt

# Linux/Mac
pip3 install -r requirements.txt
```

**Expected Output:**
```
Successfully installed Flask-3.0.0 Flask-Login-0.6.3 Flask-Mail-0.9.1
PyMySQL-1.1.0 Werkzeug-3.0.1 python-dotenv-1.0.0 itsdangerous-2.1.2 PyPDF2-3.0.1
```

---

### Step 5: Configure Application

#### Create .env File
1. Copy `.env.example` to `.env`
2. Edit `.env` with text editor

**Windows:**
```cmd
copy .env.example .env
notepad .env
```

**Linux/Mac:**
```bash
cp .env.example .env
nano .env
```

#### Edit Configuration
```env
# Generate a random secret key (important for security)
SECRET_KEY=your-random-secret-key-here-make-it-long-and-complex

# Database settings (XAMPP defaults)
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=crl_filing_system

# Email settings (see next section)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password-here
MAIL_DEFAULT_SENDER=noreply@crl.com
```

**Generate Secret Key:**
```python
# Run in Python console
import secrets
print(secrets.token_hex(32))
```

---

## Email Setup

### Gmail Configuration (Recommended)

#### Step 1: Enable 2-Factor Authentication
1. Go to https://myaccount.google.com/security
2. Click "2-Step Verification"
3. Follow steps to enable 2FA

#### Step 2: Generate App Password
1. Go to https://myaccount.google.com/apppasswords
2. Select "Mail" for app
3. Select "Other" for device
4. Enter name: "CRL Filing System"
5. Click "Generate"
6. **Copy the 16-character password** (no spaces)
7. Paste into `.env` file as MAIL_PASSWORD

#### Step 3: Update .env
```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=youremail@gmail.com
MAIL_PASSWORD=abcd efgh ijkl mnop  # Your 16-char app password
MAIL_DEFAULT_SENDER=noreply@crl.com
```

### Alternative Email Providers

#### Outlook/Office 365
```env
MAIL_SERVER=smtp.office365.com
MAIL_PORT=587
MAIL_USERNAME=youremail@outlook.com
MAIL_PASSWORD=your-password
```

#### Yahoo Mail
```env
MAIL_SERVER=smtp.mail.yahoo.com
MAIL_PORT=587
MAIL_USERNAME=youremail@yahoo.com
MAIL_PASSWORD=your-app-password
```

#### Custom SMTP Server
```env
MAIL_SERVER=mail.yourdomain.com
MAIL_PORT=587
MAIL_USERNAME=admin@yourdomain.com
MAIL_PASSWORD=your-password
```

---

## Testing

### Step 1: Start the Application

#### Windows
```cmd
cd C:\Projects\crl_filing_system
python app.py
```

#### Linux/Mac
```bash
cd /path/to/crl_filing_system
python3 app.py
```

**Expected Output:**
```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server.
 * Running on http://127.0.0.1:5000
 * Running on http://YOUR-IP:5000
Press CTRL+C to quit
```

### Step 2: Access Application
1. Open browser
2. Navigate to: http://localhost:5000
3. You should see the login page with 3D design

### Step 3: Test Login
1. Username: `admin`
2. Password: `admin123`
3. Click "Login"
4. Check email for OTP (6-digit code)
5. Enter OTP in verification page
6. Click "Verify OTP"
7. You should see the dashboard

### Step 4: Test Upload
1. Click "Upload" in sidebar
2. Select Company: LOYOLA
3. Select Category: Any category
4. Drag a PDF file
5. Click "Upload Documents"
6. Check Documents page to verify upload

### Step 5: Test Search & Filter
1. Go to Documents page
2. Try searching by filename
3. Try filtering by company
4. Try filtering by year/month

---

## Troubleshooting

### Issue: Python not found
**Error:** `'python' is not recognized as an internal or external command`

**Solution:**
- Reinstall Python with "Add to PATH" checked
- Or use full path: `C:\Python311\python.exe app.py`

### Issue: MySQL connection failed
**Error:** `Can't connect to MySQL server on 'localhost'`

**Solution:**
1. Check XAMPP Control Panel
2. Ensure MySQL is running (green highlight)
3. Click "Admin" button → should open phpMyAdmin
4. Verify database exists

### Issue: OTP email not received
**Error:** No OTP email in inbox

**Solution:**
1. Check spam/junk folder
2. Verify MAIL_USERNAME and MAIL_PASSWORD in `.env`
3. Test email configuration:
```python
from flask_mail import Mail, Message
from flask import Flask
import os

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-app-password'

mail = Mail(app)

with app.app_context():
    msg = Message('Test', recipients=['test@example.com'])
    msg.body = 'Test email'
    mail.send(msg)
    print("Email sent!")
```

### Issue: Upload fails
**Error:** File upload doesn't work

**Solution:**
1. Check file is PDF format
2. Check file size (max 50MB)
3. Verify upload folder exists:
```bash
# Windows
mkdir static\uploads

# Linux/Mac
mkdir -p static/uploads
chmod 777 static/uploads
```

### Issue: Import error for modules
**Error:** `ModuleNotFoundError: No module named 'flask'`

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Issue: Database import fails
**Error:** Error during SQL import

**Solution:**
1. Drop existing database in phpMyAdmin
2. Create new database manually
3. Re-import schema.sql
4. Check for MySQL version compatibility

### Issue: Port 5000 already in use
**Error:** `Address already in use`

**Solution:**
```python
# Edit app.py, change port at bottom:
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)  # Changed to 5001
```

Then access at: http://localhost:5001

### Issue: Permission denied on uploads
**Error:** `PermissionError: [Errno 13] Permission denied`

**Solution:**
```bash
# Linux/Mac
chmod -R 777 static/uploads

# Windows - Run as Administrator or check folder permissions
```

---

## Post-Installation Checklist

- [ ] XAMPP Apache running
- [ ] XAMPP MySQL running
- [ ] Database created and imported
- [ ] Python dependencies installed
- [ ] .env file configured
- [ ] Email sending works (OTP received)
- [ ] Application starts without errors
- [ ] Can login with admin/admin123
- [ ] Can upload a test document
- [ ] Can search and filter documents
- [ ] Admin password changed from default

---

## Security Recommendations

1. **Change Default Admin Password**
   - Login as admin
   - Go to Settings → Profile
   - Change password immediately

2. **Secure Secret Key**
   - Use a long, random string
   - Never commit to version control
   - Regenerate periodically

3. **Database Security**
   - Set MySQL root password in XAMPP
   - Use non-root database user
   - Restrict database access to localhost

4. **File Permissions**
   - Uploads folder: 755 or 700
   - Config files: 600
   - Never 777 in production

5. **HTTPS in Production**
   - Use SSL certificate
   - Enable HTTPS redirect
   - Use secure cookies

---

## Next Steps

1. Read QUICK_START.md for usage guide
2. Read README.md for complete documentation
3. Create user accounts for team members
4. Customize document categories if needed
5. Setup automated backups
6. Configure regular database maintenance

---

## Support Resources

- **Documentation**: README.md
- **Quick Start**: QUICK_START.md
- **Database Schema**: database/schema.sql
- **Configuration Template**: .env.example

---

**Installation Complete! Your CRL Filing System is ready to use! 🎉**
