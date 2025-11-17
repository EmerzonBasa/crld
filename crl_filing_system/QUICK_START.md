# CRL Filing System - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Install XAMPP (2 minutes)
1. Download XAMPP: https://www.apachefriends.org/
2. Install and open XAMPP Control Panel
3. Click **Start** for Apache and MySQL

### Step 2: Create Database (1 minute)
1. Open browser: http://localhost/phpmyadmin
2. Click **Import** tab
3. Click **Choose File** → Select `database/schema.sql`
4. Click **Go** button
5. Done! Database created with sample data

### Step 3: Install Python Packages (1 minute)
```bash
cd crl_filing_system
pip install -r requirements.txt
```

### Step 4: Configure Email (1 minute)
Create file `.env` in project folder:

```env
SECRET_KEY=my-secret-key-12345
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=crl_filing_system

# Gmail Configuration for OTP
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-gmail-app-password
MAIL_DEFAULT_SENDER=noreply@crl.com
```

**How to get Gmail App Password:**
1. Go to Google Account → Security
2. Turn on 2-Step Verification
3. Go to App passwords
4. Select Mail → Other → Generate
5. Copy 16-character password to `.env`

### Step 5: Run the System (30 seconds)
```bash
python app.py
```

### Step 6: Login
1. Open browser: http://localhost:5000
2. **Username**: admin
3. **Password**: admin123
4. Enter OTP sent to your email
5. Done! 🎉

---

## 📱 First Steps After Login

### 1. Change Admin Password
- Click your name in top-right
- Update password immediately

### 2. Add Your First Document
- Click **Upload** in sidebar
- Select Company: LOYOLA, CARITAS, PPLIC, or ETERNAL
- Choose Category
- Drop PDF files
- Fill details (optional)
- Click Upload

### 3. Create New Users
- Click **User Settings** in sidebar
- Click **Add New User**
- Fill details and set permissions
- Click Create User

---

## 🎯 Common Tasks

### Upload Multiple PDFs
1. Go to Upload page
2. Select company and category
3. Drag multiple PDF files
4. All files use same metadata
5. Click Upload

### Search Documents
1. Go to Documents page
2. Type in search bar
3. Search by filename, AO name, or description
4. Results appear instantly

### Filter by Company/Year
1. Go to Documents page
2. Use dropdown filters
3. Combine multiple filters
4. Click "Clear Filters" to reset

### View Reports
1. Go to Reports page
2. See all documents with details
3. Click "Export to Excel" for CSV file

### Restore Deleted Document
1. Go to Recycle Bin
2. Find document
3. Click Restore icon
4. Document returns to Documents

---

## ⚡ Keyboard Shortcuts

- **Ctrl + K**: Focus search bar
- **Esc**: Close modal/popup
- **Tab**: Navigate form fields

---

## 🎨 Features Overview

### Dashboard
- View statistics (total documents, storage, pages)
- Quick access to all companies
- Recent uploads list

### Documents
- View all documents
- Filter by company, category, year, month
- Search functionality
- Download/Print/Delete actions

### Upload
- Drag & drop interface
- Multiple file support
- Metadata fields
- Real-time file preview

### Recycle Bin
- Soft delete protection
- Restore capability
- Permanent delete option

### Reports
- Comprehensive document list
- Export to CSV/Excel
- Statistics dashboard

### User Settings (Admin only)
- Create new users
- Manage permissions
- Set roles (Admin, Manager, User, Viewer)

---

## 🔐 User Permissions

**Admin**: Everything
**Manager**: All except user management
**User**: View, Upload, Edit (as permitted)
**Viewer**: View only, Print if permitted

---

## 📁 Document Categories

Pre-configured categories:
- Quarterly Reports
- IC Reply Letters
- Incoming & Outgoing Communications (5 sub-folders)
- Examination & Verification (4 sub-folders)
- Claims (3 sub-folders)
- Bank/Financial Statements (2 sub-folders)
- Division Files (4 sub-folders)

---

## 🆘 Need Help?

### OTP Not Received?
1. Check spam/junk folder
2. Verify email in `.env` file
3. Check Gmail App Password
4. Look at console for errors

### Can't Upload?
1. Check file is PDF
2. File size under 50MB
3. Check upload folder permissions
4. Ensure disk space available

### Database Error?
1. Check MySQL is running in XAMPP
2. Verify database exists in phpMyAdmin
3. Check `.env` credentials

---

## 📞 Quick Reference

**Application URL**: http://localhost:5000
**phpMyAdmin**: http://localhost/phpmyadmin
**Default Admin**: admin / admin123
**Max File Size**: 50MB per file
**Supported Format**: PDF only
**Database**: MySQL (via XAMPP)

---

## ✅ Security Checklist

- [ ] Changed default admin password
- [ ] Created individual user accounts
- [ ] Set appropriate permissions per user
- [ ] Configured email for OTP
- [ ] Backed up database
- [ ] Backed up upload folder
- [ ] Reviewed activity logs

---

**Ready to go! Start managing your documents efficiently! 🚀**

For detailed information, see README.md
