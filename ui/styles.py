# STYLESHEET = """
# /* Main styles */
# QWidget {
#     font-family: 'Segoe UI', Arial, sans-serif;
# }

# /* Login page */
# #login-page {
#     background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3b82f6, stop:1 #2563eb);
# }

# .login-container {
#     background: white;
#     border-radius: 8px;
#     padding: 32px;
# }

# .login-title {
#     font-size: 24px;
#     font-weight: bold;
#     color: #1f2937;
# }

# .login-subtitle {
#     font-size: 14px;
#     color: #6b7280;
# }

# /* Input fields */
# QLineEdit, QComboBox {
#     border: 1px solid #d1d5db;
#     border-radius: 6px;
#     padding: 8px 12px;
#     font-size: 14px;
# }

# QLineEdit:focus, QComboBox:focus {
#     border: 1px solid #3b82f6;
#     outline: none;
# }

# /* Buttons */
# QPushButton {
#     background-color: #3b82f6;
#     color: white;
#     border: none;
#     border-radius: 6px;
#     padding: 8px 16px;
#     font-size: 14px;
# }

# QPushButton:hover {
#     background-color: #2563eb;
# }

# /* Sidebar */
# #sidebar {
#     background-color: #1f2937;
#     color: white;
# }

# .nav-item {
#     padding: 8px 16px;
#     border-radius: 6px;
#     color: #e5e7eb;
# }

# .nav-item:hover {
#     background-color: #374151;
# }

# .nav-item.active {
#     background-color: #3b82f6;
#     color: white;
# }

# /* Cards */
# .card {
#     background: white;
#     border-radius: 8px;
#     padding: 16px;
# }

# .card:hover {
#     transform: translateY(-5px);
# }

# /* Charts */
# .chart-container {
#     background: white;
#     border-radius: 8px;
#     padding: 16px;
# }

# /* Notification dropdown */
# .notification-dropdown {
#     background: white;
#     border-radius: 6px;
#     border: 1px solid #e5e7eb;
# }

# /* Utility classes */
# .bg-blue-100 { background-color: #dbeafe; }
# .text-blue-600 { color: #2563eb; }
# .bg-green-100 { background-color: #d1fae5; }
# .text-green-600 { color: #059669; }
# .bg-purple-100 { background-color: #ede9fe; }
# .text-purple-600 { color: #7c3aed; }
# .bg-yellow-100 { background-color: #fef3c7; }
# .text-yellow-600 { color: #d97706; }
# .bg-red-100 { background-color: #fee2e2; }
# .text-red-600 { color: #dc2626; }
# """


STYLESHEET = """
/* Main styles */
QWidget {
    font-family: 'Segoe UI', Arial, sans-serif;
}

/* Login page */
#login-page {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3b82f6, stop:1 #2563eb);
}

.login-container {
    background: white;
    border-radius: 8px;
    padding: 32px;
}

.login-title {
    font-size: 24px;
    font-weight: bold;
    color: #1f2937;
}

.login-subtitle {
    font-size: 14px;
    color: #6b7280;
}

/* Input fields */
QLineEdit, QComboBox {
    border: 1px solid #d1d5db;
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 14px;
}

QLineEdit:focus, QComboBox:focus {
    border: 1px solid #3b82f6;
    outline: none;
}

/* Buttons */
QPushButton {
    background-color: #3b82f6;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    font-size: 14px;
}

QPushButton:hover {
    background-color: #2563eb;
}

/* Sidebar */
#sidebar {
    background-color: #1f2937;
    color: white;
}

.nav-item {
    padding: 8px 16px;
    border-radius: 6px;
    color: #e5e7eb;
    text-align: left;
    margin: 2px 0;
}

.nav-item:hover {
    background-color: #374151;
}

.nav-item[active="true"] {
    background-color: #3b82f6;
    color: white;
}

/* Cards */
.card {
    background: white;
    border-radius: 8px;
    padding: 16px;
    margin: 4px;
}

# .card:hover {
#     transform: translateY(-2px);
# }

/* Charts */
.chart-container {
    background: white;
    border-radius: 8px;
    padding: 16px;
    margin: 4px;
}

/* Tables */
QTableWidget {
    border: 1px solid #e5e7eb;
    border-radius: 6px;
}

QTableWidget::item {
    padding: 8px;
}

QHeaderView::section {
    background-color: #f9fafb;
    padding: 8px;
    border: none;
    font-weight: bold;
}

/* Utility classes */
.bg-blue-100 { background-color: #dbeafe; }
.text-blue-600 { color: #2563eb; }
.bg-green-100 { background-color: #d1fae5; }
.text-green-600 { color: #059669; }
.bg-purple-100 { background-color: #ede9fe; }
.text-purple-600 { color: #7c3aed; }
.bg-yellow-100 { background-color: #fef3c7; }
.text-yellow-600 { color: #d97706; }
.bg-red-100 { background-color: #fee2e2; }
.text-red-600 { color: #dc2626; }
"""