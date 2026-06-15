// Students management JavaScript
let deleteStudentId = null;

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
    
    // Search on Enter key
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                applyFilters();
            }
        });
    }
});

function openAddModal() {
    document.getElementById('addModal').classList.add('active');
}

function openEditModal(id) {
    // Fetch student data and populate form
    fetch(`/students/edit/${id}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('editStudentId').value = id;
            document.getElementById('editName').value = data.name;
            document.getElementById('editRollNumber').value = data.roll_number;
            document.getElementById('editDepartment').value = data.department;
            document.getElementById('editYear').value = data.year;
            document.getElementById('editSection').value = data.section;
            document.getElementById('editEmail').value = data.email;
            document.getElementById('editPhone').value = data.phone;
            
            document.getElementById('editForm').action = `/students/edit/${id}`;
            document.getElementById('editModal').classList.add('active');
        })
        .catch(error => {
            console.error('Error fetching student data:', error);
            // Fallback: open modal with empty form
            document.getElementById('editForm').action = `/students/edit/${id}`;
            document.getElementById('editModal').classList.add('active');
        });
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
}

function deleteStudent(id) {
    deleteStudentId = id;
    document.getElementById('deleteModal').classList.add('active');
}

document.getElementById('confirmDeleteBtn').addEventListener('click', function() {
    if (deleteStudentId) {
        fetch(`/students/delete/${deleteStudentId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                closeModal('deleteModal');
                location.reload();
            } else {
                alert('Error deleting student: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error deleting student');
        });
    }
});

function applyFilters() {
    const search = document.getElementById('searchInput').value;
    const department = document.getElementById('departmentFilter').value;
    const year = document.getElementById('yearFilter').value;
    
    const params = new URLSearchParams();
    if (search) params.append('search', search);
    if (department) params.append('department', department);
    if (year) params.append('year', year);
    
    window.location.href = `/students?${params.toString()}`;
}

// Close modal when clicking outside
window.addEventListener('click', function(e) {
    if (e.target.classList.contains('modal')) {
        e.target.classList.remove('active');
    }
});
