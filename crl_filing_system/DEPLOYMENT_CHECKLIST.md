# CRL Filing System - Deployment Checklist

## Pre-Deployment Checklist

### 1. Environment Setup
- [ ] XAMPP installed and configured
- [ ] Python 3.7+ installed
- [ ] All Python dependencies installed (`pip install -r requirements.txt`)
- [ ] MySQL/MariaDB server running
- [ ] Apache server running (for production)

### 2. Database Configuration
- [ ] Database `crl_filing_system` created
- [ ] Schema imported successfully from `database/schema.sql`
- [ ] All tables created (9 tables total)
- [ ] Default data inserted (companies, categories, admin user)
- [ ] Database indexes created properly
- [ ] MySQL root password set (production only)
- [ ] Dedicated database user created (production only)

### 3. Application Configuration
- [ ] `.env` file created from `.env.example`
- [ ] `SECRET_KEY` set to random, secure value
- [ ] `DB_HOST` configured correctly
- [ ] `DB_USER` configured correctly
- [ ] `DB_PASSWORD` configured (if set)
- [ ] `DB_NAME` set to `crl_filing_system`
- [ ] Email settings configured (MAIL_SERVER, MAIL_PORT, etc.)
- [ ] Email credentials verified and working

### 4. Directory Structure
- [ ] `static/uploads/` directory exists
- [ ] `static/uploads/` has write permissions
- [ ] `static/css/` contains style.css
- [ ] `static/js/` contains main.js
- [ ] All template files present in `templates/`
- [ ] Database directory contains schema.sql

### 5. File Permissions (Linux/Mac)
```bash
# Application files
chmod 755 app.py
chmod 644 requirements.txt
chmod 644 .env

# Static files
chmod 755 static/
chmod 755 static/css/
chmod 755 static/js/
chmod 755 static/uploads/
chmod 644 static/css/*
chmod 644 static/js/*

# Templates
chmod 755 templates/
chmod 644 templates/*

# Documentation
chmod 644 *.md
```

### 6. Security Configuration
- [ ] Change default admin password from `admin123`
- [ ] Generate strong `SECRET_KEY` (minimum 32 characters)
- [ ] Use app-specific password for email (not regular password)
- [ ] Disable debug mode in production (`FLASK_ENV=production`)
- [ ] Set up HTTPS/SSL certificate (production)
- [ ] Configure firewall rules
- [ ] Set up regular database backups
- [ ] Configure log rotation

### 7. Testing Before Go-Live
- [ ] Login page loads correctly
- [ ] Can login with admin credentials
- [ ] OTP email received successfully
- [ ] OTP verification works
- [ ] Dashboard displays correctly
- [ ] Can view all companies
- [ ] Can upload a test PDF document
- [ ] Document appears in Documents page
- [ ] Search functionality works
- [ ] Filter functionality works
- [ ] Can view Reports page
- [ ] Can access User Settings (admin only)
- [ ] Can create a new user
- [ ] New user can login successfully
- [ ] Can delete a document (moves to recycle bin)
- [ ] Can restore from recycle bin
- [ ] Can permanently delete from recycle bin
- [ ] All permissions working correctly
- [ ] CSS loads correctly (3D design visible)
- [ ] JavaScript functionality works
- [ ] Responsive design works on mobile

### 8. Email Configuration Verification
```python
# Test email sending
from flask_mail import Mail, Message
from flask import Flask

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-app-password'

mail = Mail(app)

with app.app_context():
    msg = Message('Test Email', recipients=['test@example.com'])
    msg.body = 'If you receive this, email is configured correctly!'
    mail.send(msg)
    print("Test email sent successfully!")
```

### 9. Performance Optimization
- [ ] Database queries optimized
- [ ] Static files minified (production)
- [ ] Images optimized
- [ ] Browser caching configured
- [ ] Gzip compression enabled (production)
- [ ] CDN configured for static assets (optional)

### 10. Backup Configuration
- [ ] Database backup script created
- [ ] Automated daily backups scheduled
- [ ] Upload folder backup scheduled
- [ ] Backup storage location configured
- [ ] Backup restoration tested

---

## Deployment Steps

### Step 1: Install Dependencies
```bash
cd /path/to/crl_filing_system
pip install -r requirements.txt
```

### Step 2: Configure Environment
```bash
cp .env.example .env
nano .env  # Edit configuration
```

### Step 3: Setup Database
```bash
mysql -u root -p
CREATE DATABASE crl_filing_system CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE crl_filing_system;
SOURCE database/schema.sql;
EXIT;
```

### Step 4: Test Application
```bash
python app.py
# Visit http://localhost:5000
```

### Step 5: Production Deployment (Optional)
```bash
# Install production WSGI server
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Or use Apache mod_wsgi
# Configure Apache virtual host
```

---

## Post-Deployment Checklist

### 1. Initial Setup
- [ ] Login as admin
- [ ] Change admin password immediately
- [ ] Update admin email address
- [ ] Create user accounts for team members
- [ ] Assign appropriate roles and permissions
- [ ] Test each user account

### 2. Data Migration (if applicable)
- [ ] Export existing documents from old system
- [ ] Import documents into new system
- [ ] Verify all documents uploaded correctly
- [ ] Check document metadata
- [ ] Verify file integrity

### 3. User Training
- [ ] Provide Quick Start Guide to all users
- [ ] Conduct training session
- [ ] Demonstrate upload process
- [ ] Show search and filter features
- [ ] Explain document categories
- [ ] Review security best practices

### 4. Documentation
- [ ] README.md available to team
- [ ] QUICK_START.md distributed
- [ ] INSTALLATION.md for IT staff
- [ ] Admin guide prepared
- [ ] User manual created
- [ ] FAQ document prepared

### 5. Monitoring Setup
- [ ] Monitor application logs
- [ ] Track error rates
- [ ] Monitor database performance
- [ ] Check disk space usage
- [ ] Review user activity logs
- [ ] Set up alerts for critical issues

### 6. Backup Verification
- [ ] Initial database backup created
- [ ] Initial file backup created
- [ ] Backup restoration tested
- [ ] Backup schedule verified
- [ ] Offsite backup configured (optional)

---

## Production Configuration

### Apache Virtual Host (Optional)
```apache
<VirtualHost *:80>
    ServerName crl-filing.yourdomain.com

    WSGIDaemonProcess crl_filing python-path=/path/to/crl_filing_system
    WSGIScriptAlias / /path/to/crl_filing_system/app.wsgi

    <Directory /path/to/crl_filing_system>
        WSGIProcessGroup crl_filing
        WSGIApplicationGroup %{GLOBAL}
        Require all granted
    </Directory>

    Alias /static /path/to/crl_filing_system/static
    <Directory /path/to/crl_filing_system/static>
        Require all granted
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/crl_filing_error.log
    CustomLog ${APACHE_LOG_DIR}/crl_filing_access.log combined
</VirtualHost>
```

### Gunicorn Service (Linux)
```ini
# /etc/systemd/system/crl-filing.service
[Unit]
Description=CRL Filing System
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/crl_filing_system
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app

[Install]
WantedBy=multi-user.target
```

### Nginx Reverse Proxy (Optional)
```nginx
server {
    listen 80;
    server_name crl-filing.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        alias /path/to/crl_filing_system/static;
        expires 30d;
    }
}
```

---

## Maintenance Schedule

### Daily
- [ ] Check application logs for errors
- [ ] Monitor disk space usage
- [ ] Verify backup completion
- [ ] Review recent uploads

### Weekly
- [ ] Review user activity logs
- [ ] Check for failed login attempts
- [ ] Analyze system performance
- [ ] Update documentation if needed

### Monthly
- [ ] Review user accounts
- [ ] Clean up deleted files (if needed)
- [ ] Update Python dependencies
- [ ] Test backup restoration
- [ ] Review and optimize database

### Quarterly
- [ ] Security audit
- [ ] Performance optimization
- [ ] User feedback review
- [ ] System updates
- [ ] Capacity planning

---

## Troubleshooting Reference

### Common Issues and Solutions

**Issue**: Application won't start
```bash
# Check Python version
python --version

# Check dependencies
pip list | grep Flask

# Check logs
python app.py 2>&1 | tee error.log
```

**Issue**: Database connection failed
```bash
# Test MySQL connection
mysql -u root -p crl_filing_system -e "SHOW TABLES;"

# Check .env configuration
cat .env | grep DB_
```

**Issue**: Email not sending
```bash
# Test SMTP connection
python -c "import smtplib; smtplib.SMTP('smtp.gmail.com', 587).starttls()"

# Check email settings
cat .env | grep MAIL_
```

**Issue**: Upload fails
```bash
# Check directory permissions
ls -la static/uploads/

# Check disk space
df -h

# Check file size limit in app.py
grep MAX_CONTENT_LENGTH app.py
```

---

## Rollback Plan

### If Deployment Fails

1. **Stop Application**
   ```bash
   # Stop Flask/Gunicorn
   pkill -f "python app.py"
   ```

2. **Restore Previous Version**
   ```bash
   # Restore from backup
   cp -r /backup/crl_filing_system /path/to/
   ```

3. **Restore Database**
   ```bash
   mysql -u root -p crl_filing_system < backup.sql
   ```

4. **Restart Services**
   ```bash
   python app.py
   ```

---

## Success Criteria

### Deployment Successful When:
- ✅ Application accessible via browser
- ✅ All users can login
- ✅ OTP emails delivered within 1 minute
- ✅ Documents can be uploaded
- ✅ Search returns results in < 2 seconds
- ✅ All permissions enforced correctly
- ✅ No error messages in logs
- ✅ UI displays correctly on all browsers
- ✅ Backup system operational

---

## Contact Information

**System Administrator**: ___________________

**Email**: ___________________

**Phone**: ___________________

**Emergency Contact**: ___________________

---

## Sign-off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| System Administrator | | | |
| IT Manager | | | |
| Project Sponsor | | | |

---

**Deployment Date**: ___________________

**Go-Live Date**: ___________________

**Version**: 1.0.0

---

**All checks completed ✅ - Ready for production!**
