from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
import csv
import io
import os
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'admin' or 'teacher'

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    roll_number = db.Column(db.String(20), unique=True, nullable=False)
    department = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    section = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), db.ForeignKey('student.student_id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(10), nullable=False)  # 'present' or 'absent'
    marked_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    student = db.relationship('Student', backref=db.backref('attendance', lazy=True))

# Decorator for login required
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Get statistics
    total_students = Student.query.count()
    total_departments = db.session.query(Student.department).distinct().count()
    
    today = date.today()
    today_attendance = Attendance.query.filter_by(date=today).all()
    present_today = len([a for a in today_attendance if a.status == 'present'])
    absent_today = len([a for a in today_attendance if a.status == 'absent'])
    
    # Calculate attendance percentage
    if total_students > 0:
        attendance_percentage = round((present_today / total_students) * 100, 1)
    else:
        attendance_percentage = 0
    
    # Get monthly attendance data for chart
    monthly_data = []
    for month in range(1, 13):
        month_attendance = Attendance.query.filter(
            db.extract('month', Attendance.date) == month,
            db.extract('year', Attendance.date) == today.year
        ).all()
        present_count = len([a for a in month_attendance if a.status == 'present'])
        monthly_data.append(present_count)
    
    # Get recent attendance activity
    recent_activity = Attendance.query.order_by(Attendance.marked_at.desc()).limit(10).all()
    
    return render_template('dashboard.html',
                         total_students=total_students,
                         total_departments=total_departments,
                         present_today=present_today,
                         absent_today=absent_today,
                         attendance_percentage=attendance_percentage,
                         monthly_data=monthly_data,
                         recent_activity=recent_activity)

@app.route('/students')
@login_required
def students():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    search = request.args.get('search', '')
    department = request.args.get('department', '')
    year = request.args.get('year', '')
    
    query = Student.query
    
    if search:
        query = query.filter(
            (Student.name.contains(search)) |
            (Student.roll_number.contains(search))
        )
    
    if department:
        query = query.filter_by(department=department)
    
    if year:
        query = query.filter_by(year=year)
    
    students = query.order_by(Student.name).paginate(page=page, per_page=per_page, error_out=False)
    
    departments = db.session.query(Student.department).distinct().all()
    years = db.session.query(Student.year).distinct().all()
    
    return render_template('students.html',
                         students=students,
                         departments=[d[0] for d in departments],
                         years=[y[0] for y in years],
                         search=search,
                         selected_department=department,
                         selected_year=year)

@app.route('/students/add', methods=['GET', 'POST'])
@login_required
def add_student():
    if request.method == 'POST':
        # Generate student ID
        last_student = Student.query.order_by(Student.id.desc()).first()
        if last_student:
            new_id = f"STU{last_student.id + 1:04d}"
        else:
            new_id = "STU0001"
        
        student = Student(
            student_id=new_id,
            name=request.form.get('name'),
            roll_number=request.form.get('roll_number'),
            department=request.form.get('department'),
            year=int(request.form.get('year')),
            section=request.form.get('section'),
            email=request.form.get('email'),
            phone=request.form.get('phone')
        )
        
        try:
            db.session.add(student)
            db.session.commit()
            return redirect(url_for('students'))
        except Exception as e:
            db.session.rollback()
            return render_template('students.html', error=str(e))
    
    return redirect(url_for('students'))

@app.route('/students/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_student(id):
    student = Student.query.get_or_404(id)
    
    if request.method == 'POST':
        student.name = request.form.get('name')
        student.roll_number = request.form.get('roll_number')
        student.department = request.form.get('department')
        student.year = int(request.form.get('year'))
        student.section = request.form.get('section')
        student.email = request.form.get('email')
        student.phone = request.form.get('phone')
        
        try:
            db.session.commit()
            return redirect(url_for('students'))
        except Exception as e:
            db.session.rollback()
            return render_template('students.html', error=str(e))
    
    return redirect(url_for('students'))

@app.route('/students/delete/<int:id>', methods=['POST'])
@login_required
def delete_student(id):
    student = Student.query.get_or_404(id)
    try:
        # Delete associated attendance records
        Attendance.query.filter_by(student_id=student.student_id).delete()
        db.session.delete(student)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@app.route('/attendance')
@login_required
def attendance():
    today = date.today()
    selected_date = request.args.get('date', today.strftime('%Y-%m-%d'))
    selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
    
    students = Student.query.order_by(Student.name).all()
    
    # Get attendance for selected date
    attendance_records = {a.student_id: a.status for a in Attendance.query.filter_by(date=selected_date).all()}
    
    # Create a simple object to mimic pagination for attendance_history
    class EmptyPagination:
        def __init__(self):
            self.items = []
            self.page = 1
            self.pages = 1
            self.has_prev = False
            self.has_next = False
    
    attendance_history = EmptyPagination()
    
    return render_template('attendance.html',
                         students=students,
                         selected_date=selected_date,
                         attendance_records=attendance_records,
                         attendance_history=attendance_history)

@app.route('/attendance/mark', methods=['POST'])
@login_required
def mark_attendance():
    selected_date = request.form.get('date')
    selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
    
    # Delete existing attendance for this date
    Attendance.query.filter_by(date=selected_date).delete()
    
    # Add new attendance records
    students = Student.query.all()
    for student in students:
        status = request.form.get(f'status_{student.student_id}')
        if status:
            attendance = Attendance(
                student_id=student.student_id,
                date=selected_date,
                status=status
            )
            db.session.add(attendance)
    
    try:
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@app.route('/attendance/history')
@login_required
def attendance_history():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    search_date = request.args.get('date', '')
    
    query = Attendance.query
    
    if search_date:
        search_date = datetime.strptime(search_date, '%Y-%m-%d').date()
        query = query.filter_by(date=search_date)
    
    attendance = query.order_by(Attendance.date.desc(), Attendance.student_id).paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('attendance.html',
                         attendance_history=attendance,
                         search_date=search_date)

@app.route('/reports')
@login_required
def reports():
    report_type = request.args.get('type', 'student')
    department = request.args.get('department', '')
    month = request.args.get('month', '')
    
    students = Student.query.all()
    
    if report_type == 'student':
        # Student-wise attendance
        report_data = []
        for student in students:
            total_classes = Attendance.query.filter_by(student_id=student.student_id).count()
            present_count = Attendance.query.filter_by(student_id=student.student_id, status='present').count()
            absent_count = total_classes - present_count
            percentage = round((present_count / total_classes * 100), 1) if total_classes > 0 else 0
            
            report_data.append({
                'student_id': student.student_id,
                'name': student.name,
                'roll_number': student.roll_number,
                'department': student.department,
                'total_classes': total_classes,
                'present_count': present_count,
                'absent_count': absent_count,
                'percentage': percentage
            })
    
    elif report_type == 'department':
        # Department-wise attendance
        departments = db.session.query(Student.department).distinct().all()
        report_data = []
        
        for dept in departments:
            dept_name = dept[0]
            dept_students = Student.query.filter_by(department=dept_name).all()
            student_ids = [s.student_id for s in dept_students]
            
            total_classes = Attendance.query.filter(Attendance.student_id.in_(student_ids)).count()
            present_count = Attendance.query.filter(
                Attendance.student_id.in_(student_ids),
                Attendance.status == 'present'
            ).count()
            absent_count = total_classes - present_count
            percentage = round((present_count / total_classes * 100), 1) if total_classes > 0 else 0
            
            report_data.append({
                'department': dept_name,
                'total_students': len(dept_students),
                'total_classes': total_classes,
                'present_count': present_count,
                'absent_count': absent_count,
                'percentage': percentage
            })
    
    elif report_type == 'monthly':
        # Monthly attendance
        today = date.today()
        selected_month = int(month) if month else today.month
        selected_year = today.year
        
        report_data = []
        for student in students:
            monthly_attendance = Attendance.query.filter(
                Attendance.student_id == student.student_id,
                db.extract('month', Attendance.date) == selected_month,
                db.extract('year', Attendance.date) == selected_year
            ).all()
            
            total_classes = len(monthly_attendance)
            present_count = len([a for a in monthly_attendance if a.status == 'present'])
            absent_count = total_classes - present_count
            percentage = round((present_count / total_classes * 100), 1) if total_classes > 0 else 0
            
            report_data.append({
                'student_id': student.student_id,
                'name': student.name,
                'roll_number': student.roll_number,
                'department': student.department,
                'total_classes': total_classes,
                'present_count': present_count,
                'absent_count': absent_count,
                'percentage': percentage
            })
    
    departments = db.session.query(Student.department).distinct().all()
    
    return render_template('reports.html',
                         report_type=report_type,
                         report_data=report_data,
                         departments=[d[0] for d in departments],
                         selected_department=department,
                         selected_month=month)

@app.route('/export/<report_type>')
@login_required
def export_report(report_type):
    if report_type == 'student':
        students = Student.query.all()
        output = io.StringIO()
        writer = csv.writer(output)
        
        writer.writerow(['Student ID', 'Name', 'Roll Number', 'Department', 'Year', 'Section', 'Email', 'Phone'])
        
        for student in students:
            total_classes = Attendance.query.filter_by(student_id=student.student_id).count()
            present_count = Attendance.query.filter_by(student_id=student.student_id, status='present').count()
            absent_count = total_classes - present_count
            percentage = round((present_count / total_classes * 100), 1) if total_classes > 0 else 0
            
            writer.writerow([
                student.student_id,
                student.name,
                student.roll_number,
                student.department,
                student.year,
                student.section,
                student.email,
                student.phone,
                total_classes,
                present_count,
                absent_count,
                f"{percentage}%"
            ])
        
        output.seek(0)
        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8')),
            mimetype='text/csv',
            as_attachment=True,
            download_name='student_attendance_report.csv'
        )
    
    elif report_type == 'department':
        departments = db.session.query(Student.department).distinct().all()
        output = io.StringIO()
        writer = csv.writer(output)
        
        writer.writerow(['Department', 'Total Students', 'Total Classes', 'Present Count', 'Absent Count', 'Percentage'])
        
        for dept in departments:
            dept_name = dept[0]
            dept_students = Student.query.filter_by(department=dept_name).all()
            student_ids = [s.student_id for s in dept_students]
            
            total_classes = Attendance.query.filter(Attendance.student_id.in_(student_ids)).count()
            present_count = Attendance.query.filter(
                Attendance.student_id.in_(student_ids),
                Attendance.status == 'present'
            ).count()
            absent_count = total_classes - present_count
            percentage = round((present_count / total_classes * 100), 1) if total_classes > 0 else 0
            
            writer.writerow([
                dept_name,
                len(dept_students),
                total_classes,
                present_count,
                absent_count,
                f"{percentage}%"
            ])
        
        output.seek(0)
        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8')),
            mimetype='text/csv',
            as_attachment=True,
            download_name='department_attendance_report.csv'
        )
    
    return redirect(url_for('reports'))

# Initialize database
def init_db():
    with app.app_context():
        db.create_all()
        
        # Create default admin user if not exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                password=generate_password_hash('admin123'),
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()
        
        # Create default teacher user if not exists
        teacher = User.query.filter_by(username='teacher').first()
        if not teacher:
            teacher = User(
                username='teacher',
                password=generate_password_hash('teacher123'),
                role='teacher'
            )
            db.session.add(teacher)
            db.session.commit()
# Initialize database for Gunicorn/Render
with app.app_context():
    init_db()
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
