// Attendance management JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Theme toggle
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        const body = document.body;
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            body.setAttribute('data-theme', savedTheme);
            updateThemeIcon(savedTheme);
        }
        
        themeToggle.addEventListener('click', function() {
            const currentTheme = body.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            body.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeIcon(newTheme);
        });
    }
    
    function updateThemeIcon(theme) {
        const icon = themeToggle.querySelector('i');
        if (theme === 'dark') {
            icon.classList.remove('fa-moon');
            icon.classList.add('fa-sun');
        } else {
            icon.classList.remove('fa-sun');
            icon.classList.add('fa-moon');
        }
    }
});

function loadAttendanceForDate() {
    const date = document.getElementById('attendanceDate').value;
    document.getElementById('hiddenDate').value = date;
    window.location.href = `/attendance?date=${date}`;
}

function markAllPresent() {
    const form = document.getElementById('attendanceForm');
    const presentRadios = form.querySelectorAll('input[type="radio"][value="present"]');
    presentRadios.forEach(radio => {
        radio.checked = true;
    });
}

function markAllAbsent() {
    const form = document.getElementById('attendanceForm');
    const absentRadios = form.querySelectorAll('input[type="radio"][value="absent"]');
    absentRadios.forEach(radio => {
        radio.checked = true;
    });
}

function saveAttendance() {
    const form = document.getElementById('attendanceForm');
    const formData = new FormData(form);
    
    // Check if at least one student has attendance marked
    let hasAttendance = false;
    const radioButtons = form.querySelectorAll('input[type="radio"]');
    radioButtons.forEach(radio => {
        if (radio.checked) {
            hasAttendance = true;
        }
    });
    
    if (!hasAttendance) {
        alert('Please mark attendance for at least one student.');
        return;
    }
    
    fetch('/attendance/mark', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Attendance saved successfully!');
        } else {
            alert('Error saving attendance: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error saving attendance');
    });
}

function showHistory() {
    document.getElementById('markAttendanceSection').style.display = 'none';
    document.getElementById('historySection').style.display = 'block';
}

function showMarkAttendance() {
    document.getElementById('historySection').style.display = 'none';
    document.getElementById('markAttendanceSection').style.display = 'block';
}

function searchHistory() {
    const date = document.getElementById('searchDate').value;
    window.location.href = `/attendance/history?date=${date}`;
}
