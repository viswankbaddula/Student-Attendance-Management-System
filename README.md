# Student Attendance Management System

A modern, responsive web application for managing student attendance with a beautiful glassmorphism UI design. Built with Flask, SQLite, HTML5, CSS3, and JavaScript.

## Features

### Authentication
- Secure login system for Admin and Teacher roles
- Password hashing using Werkzeug
- Session management
- Logout functionality

### Dashboard
- Real-time statistics (Total Students, Departments, Present/Absent Today)
- Attendance percentage calculation
- Monthly attendance chart using Chart.js
- Recent activity feed

### Student Management
- Add new students with auto-generated Student IDs
- Edit student information
- Delete students with confirmation
- Search by name or roll number
- Filter by department and year
- Pagination support

### Attendance Management
- Mark attendance for any date
- Mark all present/absent with one click
- View attendance history
- Search attendance by date
- Prevent duplicate attendance for same date

### Reports
- Student-wise attendance reports
- Department-wise attendance reports
- Monthly attendance reports
- Export reports to CSV
- Summary statistics with color-coded attendance percentages

### User Interface
- Modern glassmorphism design
- Dark/Light mode toggle
- Responsive layout for all devices
- Animated cards and transitions
- Beautiful color scheme
- Font Awesome icons

## Technology Stack

- **Backend**: Python 3.x, Flask 3.0.0
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Custom CSS with glassmorphism effects
- **Icons**: Font Awesome 6.4.0
- **Charts**: Chart.js
- **ORM**: Flask-SQLAlchemy 3.1.1

## Installation Guide

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Clone or Download the Project
```bash
cd StudentAttendanceSystem
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
python app.py
```

The application will start on `http://127.0.0.1:5000`

## Default Credentials

### Admin Account
- **Username**: admin
- **Password**: admin123

### Teacher Account
- **Username**: teacher
- **Password**: teacher123

**Important**: Change these passwords in production!

## Project Structure

```
StudentAttendanceSystem/
│
├── static/
│   ├── css/
│   │   └── style.css          # Main stylesheet with glassmorphism design
│   ├── js/
│   │   ├── login.js           # Login page functionality
│   │   ├── dashboard.js       # Dashboard interactivity
│   │   ├── students.js        # Student management functionality
│   │   ├── attendance.js      # Attendance marking functionality
│   │   └── reports.js         # Reports and export functionality
│   └── images/                # Image assets (if needed)
│
├── templates/
│   ├── login.html             # Login page
│   ├── dashboard.html         # Dashboard with statistics and charts
│   ├── students.html          # Student management page
│   ├── attendance.html        # Attendance marking and history
│   └── reports.html           # Reports and export page
│
├── app.py                     # Main Flask application with routes and models
├── requirements.txt           # Python dependencies
├── database.db                # SQLite database (auto-created)
└── README.md                  # This file
```

## Database Schema

### Users Table
- `id` (Integer, Primary Key)
- `username` (String, Unique)
- `password` (String, Hashed)
- `role` (String: 'admin' or 'teacher')

### Students Table
- `id` (Integer, Primary Key)
- `student_id` (String, Unique, Auto-generated)
- `name` (String)
- `roll_number` (String, Unique)
- `department` (String)
- `year` (Integer)
- `section` (String)
- `email` (String)
- `phone` (String)
- `created_at` (DateTime)

### Attendance Table
- `id` (Integer, Primary Key)
- `student_id` (String, Foreign Key)
- `date` (Date)
- `status` (String: 'present' or 'absent')
- `marked_at` (DateTime)

## Usage Guide

### 1. Login
- Navigate to `http://127.0.0.1:5000`
- Enter your username and password
- Click Login

### 2. Dashboard
- View real-time statistics
- Check monthly attendance trends
- Monitor recent activity

### 3. Managing Students
- Click "Add Student" to register new students
- Use search bar to find students
- Filter by department or year
- Edit or delete students using action buttons

### 4. Marking Attendance
- Select the date from the date picker
- Mark students as Present or Absent
- Use "Mark All Present/Absent" for quick marking
- Click "Save Attendance" to save

### 5. Viewing History
- Click "View History" button
- Search attendance by date
- Navigate through pages using pagination

### 6. Generating Reports
- Select report type (Student-wise, Department-wise, Monthly)
- Apply filters if needed
- View summary statistics
- Click "Export CSV" to download reports

## Security Considerations

1. **Change Default Passwords**: Update the default admin and teacher passwords in production
2. **Secret Key**: Change the `SECRET_KEY` in `app.py` to a secure random string
3. **HTTPS**: Use HTTPS in production environments
4. **Input Validation**: All forms include client-side and server-side validation
5. **SQL Injection Protection**: Using SQLAlchemy ORM prevents SQL injection
6. **Password Hashing**: Passwords are hashed using Werkzeug's security functions

## Customization

### Changing the Color Theme
Edit the CSS variables in `static/css/style.css`:
```css
:root {
    --primary-color: #3498db;
    --secondary-color: #2ecc71;
    --danger-color: #e74c3c;
    /* ... other colors */
}
```

### Adding New Departments
Edit the department dropdown in `templates/students.html`:
```html
<option value="Your Department">Your Department</option>
```

### Modifying the Database Schema
1. Update the model classes in `app.py`
2. Delete the existing `database.db` file
3. Restart the application to recreate the database

## Troubleshooting

### Database Locked Error
If you encounter a database locked error:
- Close all database connections
- Delete `database.db` and restart the application
- Ensure only one instance of the app is running

### Port Already in Use
If port 5000 is already in use:
```bash
# Change the port in app.py
if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5001)  # Use port 5001
```

### Import Errors
If you encounter import errors:
```bash
pip install --upgrade -r requirements.txt
```

## Future Enhancements

- [ ] QR Code-based attendance scanning
- [ ] Face recognition attendance
- [ ] Email notifications for low attendance
- [ ] Student profile photo upload
- [ ] Advanced analytics and graphs
- [ ] REST API support
- [ ] Docker deployment
- [ ] Unit testing with pytest
- [ ] Multi-language support
- [ ] Parent portal for attendance viewing
- [ ] Mobile app version

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available for educational purposes.

## Support

For issues, questions, or suggestions, please create an issue in the project repository.

## Acknowledgments

- Flask Framework
- Chart.js for beautiful charts
- Font Awesome for icons
- Glassmorphism design inspiration

---

**Note**: This is a demonstration project. For production use, additional security measures and optimizations should be implemented.
