import os
import secrets
import pymysql
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_file
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
import PyPDF2
from functools import wraps

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'crl-filing-system-secret-key-2024')
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'static/uploads')
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Email configuration (Configure with your SMTP settings)
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'your-email@gmail.com')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'your-password')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@crl.com')

mail = Mail(app)

# Database configuration
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', ''),
    'database': os.environ.get('DB_NAME', 'crl_filing_system'),
    'cursorclass': pymysql.cursors.DictCursor
}

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Database connection helper
def get_db():
    return pymysql.connect(**DB_CONFIG)

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, user_data):
        self.id = user_data['user_id']
        self.username = user_data['username']
        self.email = user_data['email']
        self.full_name = user_data['full_name']
        self.role = user_data['role']
        self.can_view = user_data['can_view']
        self.can_edit = user_data['can_edit']
        self.can_upload = user_data['can_upload']
        self.can_delete = user_data['can_delete']
        self.can_print = user_data['can_print']

@login_manager.user_loader
def load_user(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = %s AND is_active = TRUE", (user_id,))
    user_data = cursor.fetchone()
    cursor.close()
    db.close()
    if user_data:
        return User(user_data)
    return None

# Permission decorators
def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not getattr(current_user, permission, False):
                flash('You do not have permission to perform this action.', 'error')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Send OTP via email
def send_otp_email(email, otp_code, full_name):
    try:
        msg = Message(
            'CRL Filing System - OTP Verification',
            recipients=[email]
        )
        msg.html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; background-color: #1a1a2e; color: #e0e0e0; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; background-color: #16213e; border-radius: 10px; padding: 30px;">
                    <h2 style="color: #a3b9cc;">CRL Digital Filing System</h2>
                    <p>Hello {full_name},</p>
                    <p>Your One-Time Password (OTP) for login verification is:</p>
                    <div style="background-color: #0f3460; padding: 20px; border-radius: 5px; text-align: center; margin: 20px 0;">
                        <h1 style="color: #e94560; margin: 0; letter-spacing: 5px;">{otp_code}</h1>
                    </div>
                    <p>This OTP will expire in 10 minutes.</p>
                    <p style="color: #a3b9cc; font-size: 12px; margin-top: 30px;">
                        If you did not request this OTP, please ignore this email.
                    </p>
                </div>
            </body>
        </html>
        """
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

# Log user activity
def log_activity(user_id, activity_type, description, ip_address=None):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO user_activity_log (user_id, activity_type, activity_description, ip_address) VALUES (%s, %s, %s, %s)",
        (user_id, activity_type, description, ip_address or request.remote_addr)
    )
    db.commit()
    cursor.close()
    db.close()

# Log document access
def log_document_access(document_id, user_id, action_type):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO document_access_log (document_id, user_id, action_type, ip_address) VALUES (%s, %s, %s, %s)",
        (document_id, user_id, action_type, request.remote_addr)
    )
    db.commit()
    cursor.close()
    db.close()

# Count PDF pages
def count_pdf_pages(file_path):
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            return len(pdf_reader.pages)
    except:
        return 0

# Routes

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND is_active = TRUE", (username,))
        user_data = cursor.fetchone()
        cursor.close()
        db.close()

        if user_data and check_password_hash(user_data['password_hash'], password):
            # Generate OTP
            otp_code = ''.join([str(secrets.randbelow(10)) for _ in range(6)])
            expires_at = datetime.now() + timedelta(minutes=10)

            # Store OTP in database
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO otp_verification (user_id, otp_code, expires_at) VALUES (%s, %s, %s)",
                (user_data['user_id'], otp_code, expires_at)
            )
            db.commit()
            cursor.close()
            db.close()

            # Send OTP email
            if send_otp_email(user_data['email'], otp_code, user_data['full_name']):
                session['pending_user_id'] = user_data['user_id']
                flash('OTP has been sent to your email.', 'success')
                return redirect(url_for('verify_otp'))
            else:
                flash('Failed to send OTP. Please check email configuration.', 'error')
        else:
            flash('Invalid username or password.', 'error')

    return render_template('login.html')

@app.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    if 'pending_user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        otp_code = request.form.get('otp')
        user_id = session['pending_user_id']

        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "SELECT * FROM otp_verification WHERE user_id = %s AND otp_code = %s AND is_used = FALSE AND expires_at > NOW() ORDER BY created_at DESC LIMIT 1",
            (user_id, otp_code)
        )
        otp_data = cursor.fetchone()

        if otp_data:
            # Mark OTP as used
            cursor.execute("UPDATE otp_verification SET is_used = TRUE WHERE otp_id = %s", (otp_data['otp_id'],))

            # Update last login
            cursor.execute("UPDATE users SET last_login = NOW() WHERE user_id = %s", (user_id,))
            db.commit()

            # Load user and login
            cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            user_data = cursor.fetchone()
            cursor.close()
            db.close()

            user = User(user_data)
            login_user(user)
            log_activity(user_id, 'login', 'User logged in successfully')

            session.pop('pending_user_id', None)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            cursor.close()
            db.close()
            flash('Invalid or expired OTP.', 'error')

    return render_template('verify_otp.html')

@app.route('/logout')
@login_required
def logout():
    log_activity(current_user.id, 'logout', 'User logged out')
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    db = get_db()
    cursor = db.cursor()

    # Get companies
    cursor.execute("SELECT * FROM companies WHERE is_active = TRUE ORDER BY company_name")
    companies = cursor.fetchall()

    # Get document statistics
    cursor.execute("""
        SELECT
            COUNT(*) as total_documents,
            SUM(file_size) as total_size,
            SUM(page_count) as total_pages
        FROM documents
        WHERE is_deleted = FALSE
    """)
    stats = cursor.fetchone()

    # Get recent uploads
    cursor.execute("""
        SELECT d.*, c.company_name, u.full_name as uploader_name, cat.category_name
        FROM documents d
        JOIN companies c ON d.company_id = c.company_id
        JOIN users u ON d.uploaded_by = u.user_id
        JOIN document_categories cat ON d.category_id = cat.category_id
        WHERE d.is_deleted = FALSE
        ORDER BY d.uploaded_at DESC
        LIMIT 10
    """)
    recent_documents = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template('dashboard.html',
                         companies=companies,
                         stats=stats,
                         recent_documents=recent_documents)

@app.route('/documents')
@login_required
def documents():
    company_id = request.args.get('company_id', type=int)
    category_id = request.args.get('category_id', type=int)
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)
    search = request.args.get('search', '')

    db = get_db()
    cursor = db.cursor()

    # Get companies
    cursor.execute("SELECT * FROM companies WHERE is_active = TRUE ORDER BY company_name")
    companies = cursor.fetchall()

    # Get categories
    cursor.execute("SELECT * FROM document_categories ORDER BY category_path")
    categories = cursor.fetchall()

    # Build query
    query = """
        SELECT d.*, c.company_name, u.full_name as uploader_name, cat.category_name, cat.category_path
        FROM documents d
        JOIN companies c ON d.company_id = c.company_id
        JOIN users u ON d.uploaded_by = u.user_id
        JOIN document_categories cat ON d.category_id = cat.category_id
        WHERE d.is_deleted = FALSE
    """
    params = []

    if company_id:
        query += " AND d.company_id = %s"
        params.append(company_id)

    if category_id:
        query += " AND d.category_id = %s"
        params.append(category_id)

    if year:
        query += " AND d.document_year = %s"
        params.append(year)

    if month:
        query += " AND d.document_month = %s"
        params.append(month)

    if search:
        query += " AND (d.file_name LIKE %s OR d.file_description LIKE %s OR d.ao_name LIKE %s)"
        search_term = f"%{search}%"
        params.extend([search_term, search_term, search_term])

    query += " ORDER BY d.uploaded_at DESC"

    cursor.execute(query, params)
    documents = cursor.fetchall()

    # Get available years
    cursor.execute("SELECT DISTINCT document_year FROM documents WHERE is_deleted = FALSE AND document_year IS NOT NULL ORDER BY document_year DESC")
    years = [row['document_year'] for row in cursor.fetchall()]

    cursor.close()
    db.close()

    return render_template('documents.html',
                         documents=documents,
                         companies=companies,
                         categories=categories,
                         years=years,
                         current_company=company_id,
                         current_category=category_id,
                         current_year=year,
                         current_month=month,
                         search=search)

@app.route('/upload', methods=['GET', 'POST'])
@login_required
@permission_required('can_upload')
def upload_documents():
    if request.method == 'POST':
        files = request.files.getlist('files')
        company_id = request.form.get('company_id', type=int)
        category_id = request.form.get('category_id', type=int)
        ao_name = request.form.get('ao_name', '')
        file_description = request.form.get('file_description', '')
        document_year = request.form.get('document_year', type=int)
        document_month = request.form.get('document_month', type=int)
        scanned_date = request.form.get('scanned_date')
        storage_location = request.form.get('storage_location', '')

        if not files or not company_id or not category_id:
            flash('Please provide all required fields.', 'error')
            return redirect(url_for('upload_documents'))

        db = get_db()
        cursor = db.cursor()

        uploaded_count = 0
        for file in files:
            if file and file.filename.lower().endswith('.pdf'):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{timestamp}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                file.save(file_path)
                file_size = os.path.getsize(file_path)
                page_count = count_pdf_pages(file_path)

                cursor.execute("""
                    INSERT INTO documents
                    (company_id, category_id, ao_name, file_description, file_name, file_path,
                     file_size, file_type, document_year, document_month, scanned_date,
                     storage_location, page_count, uploaded_by)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (company_id, category_id, ao_name, file_description, filename, file_path,
                      file_size, 'application/pdf', document_year, document_month, scanned_date,
                      storage_location, page_count, current_user.id))

                uploaded_count += 1

        db.commit()
        cursor.close()
        db.close()

        log_activity(current_user.id, 'upload', f'Uploaded {uploaded_count} document(s)')
        flash(f'Successfully uploaded {uploaded_count} document(s).', 'success')
        return redirect(url_for('documents'))

    # GET request
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM companies WHERE is_active = TRUE ORDER BY company_name")
    companies = cursor.fetchall()
    cursor.execute("SELECT * FROM document_categories ORDER BY category_path")
    categories = cursor.fetchall()
    cursor.close()
    db.close()

    return render_template('upload.html', companies=companies, categories=categories)

@app.route('/document/<int:document_id>/delete', methods=['POST'])
@login_required
@permission_required('can_delete')
def delete_document(document_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE documents SET is_deleted = TRUE, deleted_at = NOW(), deleted_by = %s WHERE document_id = %s",
        (current_user.id, document_id)
    )
    db.commit()
    cursor.close()
    db.close()

    log_activity(current_user.id, 'delete', f'Moved document {document_id} to recycle bin')
    log_document_access(document_id, current_user.id, 'delete')
    flash('Document moved to recycle bin.', 'success')
    return redirect(request.referrer or url_for('documents'))

@app.route('/recycle-bin')
@login_required
@permission_required('can_delete')
def recycle_bin():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT d.*, c.company_name, u.full_name as uploader_name, cat.category_name
        FROM documents d
        JOIN companies c ON d.company_id = c.company_id
        JOIN users u ON d.uploaded_by = u.user_id
        JOIN document_categories cat ON d.category_id = cat.category_id
        WHERE d.is_deleted = TRUE
        ORDER BY d.deleted_at DESC
    """)
    documents = cursor.fetchall()
    cursor.close()
    db.close()

    return render_template('recycle_bin.html', documents=documents)

@app.route('/document/<int:document_id>/restore', methods=['POST'])
@login_required
@permission_required('can_delete')
def restore_document(document_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE documents SET is_deleted = FALSE, deleted_at = NULL, deleted_by = NULL WHERE document_id = %s",
        (document_id,)
    )
    db.commit()
    cursor.close()
    db.close()

    log_activity(current_user.id, 'restore', f'Restored document {document_id}')
    log_document_access(document_id, current_user.id, 'restore')
    flash('Document restored successfully.', 'success')
    return redirect(url_for('recycle_bin'))

@app.route('/document/<int:document_id>/permanent-delete', methods=['POST'])
@login_required
@permission_required('can_delete')
def permanent_delete_document(document_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT file_path FROM documents WHERE document_id = %s", (document_id,))
    document = cursor.fetchone()

    if document:
        # Delete physical file
        try:
            if os.path.exists(document['file_path']):
                os.remove(document['file_path'])
        except:
            pass

        # Delete from database
        cursor.execute("DELETE FROM documents WHERE document_id = %s", (document_id,))
        db.commit()

        log_activity(current_user.id, 'permanent_delete', f'Permanently deleted document {document_id}')
        flash('Document permanently deleted.', 'success')

    cursor.close()
    db.close()
    return redirect(url_for('recycle_bin'))

@app.route('/reports')
@login_required
def reports():
    db = get_db()
    cursor = db.cursor()

    # Get all documents with detailed info
    cursor.execute("""
        SELECT d.*, c.company_name, u.full_name as uploader_name, cat.category_name, cat.category_path
        FROM documents d
        JOIN companies c ON d.company_id = c.company_id
        JOIN users u ON d.uploaded_by = u.user_id
        JOIN document_categories cat ON d.category_id = cat.category_id
        WHERE d.is_deleted = FALSE
        ORDER BY d.uploaded_at DESC
    """)
    documents = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template('reports.html', documents=documents)

@app.route('/settings/users')
@login_required
def users_settings():
    if current_user.role not in ['admin', 'manager']:
        flash('Access denied.', 'error')
        return redirect(url_for('dashboard'))

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users ORDER BY created_at DESC")
    users = cursor.fetchall()
    cursor.close()
    db.close()

    return render_template('users.html', users=users)

@app.route('/settings/users/add', methods=['POST'])
@login_required
def add_user():
    if current_user.role != 'admin':
        return jsonify({'success': False, 'message': 'Access denied'}), 403

    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    full_name = request.form.get('full_name')
    role = request.form.get('role', 'user')

    db = get_db()
    cursor = db.cursor()

    try:
        password_hash = generate_password_hash(password)
        cursor.execute("""
            INSERT INTO users (username, email, password_hash, full_name, role)
            VALUES (%s, %s, %s, %s, %s)
        """, (username, email, password_hash, full_name, role))
        db.commit()
        flash('User added successfully.', 'success')
    except pymysql.IntegrityError:
        flash('Username or email already exists.', 'error')

    cursor.close()
    db.close()
    return redirect(url_for('users_settings'))

@app.route('/settings/users/<int:user_id>/update', methods=['POST'])
@login_required
def update_user(user_id):
    if current_user.role != 'admin':
        return jsonify({'success': False, 'message': 'Access denied'}), 403

    data = request.get_json()

    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        UPDATE users
        SET can_view = %s, can_edit = %s, can_upload = %s, can_delete = %s, can_print = %s, role = %s
        WHERE user_id = %s
    """, (data.get('can_view'), data.get('can_edit'), data.get('can_upload'),
          data.get('can_delete'), data.get('can_print'), data.get('role'), user_id))
    db.commit()
    cursor.close()
    db.close()

    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
