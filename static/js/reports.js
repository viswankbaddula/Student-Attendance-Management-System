// Reports JavaScript
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

function changeReportType() {
    const reportType = document.getElementById('reportType').value;
    window.location.href = `/reports?type=${reportType}`;
}

function applyReportFilters() {
    const reportType = document.getElementById('reportType').value;
    const department = document.getElementById('departmentFilter') ? document.getElementById('departmentFilter').value : '';
    const month = document.getElementById('monthFilter') ? document.getElementById('monthFilter').value : '';
    
    const params = new URLSearchParams();
    params.append('type', reportType);
    if (department) params.append('department', department);
    if (month) params.append('month', month);
    
    window.location.href = `/reports?${params.toString()}`;
}

function exportReport() {
    const reportType = document.getElementById('reportType').value;
    window.location.href = `/export/${reportType}`;
}
