from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
                            QComboBox, QCheckBox, QHBoxLayout, QFormLayout, QMessageBox,
                            QStackedWidget, QDateEdit)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont, QPixmap
from database import HospitalDatabase

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.db = HospitalDatabase()
        self.setWindowTitle("MediCare Hospital - Login/Register")
        self.setFixedSize(600, 700)
        
        self.init_ui()
        
    def init_ui(self):
        self.setObjectName("login-page")
        
        # Create stacked widget for login/register views
        self.stacked_widget = QStackedWidget()
        
        # Login Page
        self.login_page = self.create_login_page()
        # Register Page
        self.register_page = self.create_register_page()
        
        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.register_page)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.stacked_widget)
        
    def create_login_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        # Logo and title
        logo = QLabel()
        logo.setPixmap(QPixmap("assets/icons/hospital.png").scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignCenter)
        
        title = QLabel("MediCare Hospital")
        title.setObjectName("login-title")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        
        subtitle = QLabel("Please login to access your dashboard")
        subtitle.setObjectName("login-subtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        
        # Form
        form_layout = QFormLayout()
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        
        self.role_combo = QComboBox()
        self.role_combo.addItems(["Patient", "Doctor", "Admin"])
        
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Password:", self.password_input)
        form_layout.addRow("Login as:", self.role_combo)
        
        # Remember me and forgot password
        remember_check = QCheckBox("Remember me")
        forgot_password = QPushButton("Forgot password?")
        forgot_password.setFlat(True)
        forgot_password.setStyleSheet("color: #ffffff; text-decoration: underline;")
        
        remember_layout = QHBoxLayout()
        remember_layout.addWidget(remember_check)
        remember_layout.addWidget(forgot_password)
        
        # Login button
        login_btn = QPushButton("Login")
        login_btn.setObjectName("login-btn")
        
        # Register link
        register_link = QPushButton("Don't have an account? Register here")
        register_link.setFlat(True)
        # register_link.setStyleSheet("color: #3b82f6; text-decoration: underline;")
        register_link.setStyleSheet("color: #ffffff; text-decoration: underline;")
        
        # Add widgets to layout
        layout.addWidget(logo)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(20)
        layout.addLayout(form_layout)
        layout.addLayout(remember_layout)
        layout.addSpacing(10)
        layout.addWidget(login_btn)
        layout.addSpacing(10)
        layout.addWidget(register_link)
        
        # Container widget for styling
        container = QWidget()
        container.setObjectName("login-container")
        container.setLayout(layout)
        container.setFixedWidth(400)
        
        # Set page layout
        page_layout = QVBoxLayout(page)
        page_layout.addWidget(container, alignment=Qt.AlignCenter)
        
        # Connect signals
        login_btn.clicked.connect(self.handle_login)
        register_link.clicked.connect(self.show_register_page)
        
        return page
    
    def create_register_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        # Logo and title
        logo = QLabel()
        logo.setPixmap(QPixmap("assets/icons/hospital.png").scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignCenter)
        
        title = QLabel("Register New Account")
        title.setObjectName("login-title")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        
        subtitle = QLabel("Please fill in your details")
        subtitle.setObjectName("login-subtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        
        # Form
        form_layout = QFormLayout()
        
        # Common fields
        self.reg_name_input = QLineEdit()
        self.reg_name_input.setPlaceholderText("Full Name")
        
        self.reg_email_input = QLineEdit()
        self.reg_email_input.setPlaceholderText("Email Address")
        
        self.reg_password_input = QLineEdit()
        self.reg_password_input.setPlaceholderText("Password")
        self.reg_password_input.setEchoMode(QLineEdit.Password)
        
        self.reg_confirm_password_input = QLineEdit()
        self.reg_confirm_password_input.setPlaceholderText("Confirm Password")
        self.reg_confirm_password_input.setEchoMode(QLineEdit.Password)
        
        self.reg_phone_input = QLineEdit()
        self.reg_phone_input.setPlaceholderText("Phone Number")
        
        self.reg_role_combo = QComboBox()
        self.reg_role_combo.addItems(["Patient", "Doctor"])
        
        # Patient-specific fields
        self.reg_dob_input = QDateEdit()
        self.reg_dob_input.setDisplayFormat("yyyy-MM-dd")
        self.reg_dob_input.setDate(QDate.currentDate().addYears(-18))
        self.reg_dob_input.setCalendarPopup(True)
        
        self.reg_blood_type_combo = QComboBox()
        self.reg_blood_type_combo.addItems(["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        
        self.reg_insurance_input = QLineEdit()
        self.reg_insurance_input.setPlaceholderText("Insurance Provider")
        
        # Doctor-specific fields
        self.reg_specialization_input = QLineEdit()
        self.reg_specialization_input.setPlaceholderText("Specialization")
        self.reg_specialization_input.setVisible(False)
        
        self.reg_department_input = QLineEdit()
        self.reg_department_input.setPlaceholderText("Department")
        self.reg_department_input.setVisible(False)
        
        # Add fields to form
        form_layout.addRow("Full Name:", self.reg_name_input)
        form_layout.addRow("Email:", self.reg_email_input)
        form_layout.addRow("Password:", self.reg_password_input)
        form_layout.addRow("Confirm Password:", self.reg_confirm_password_input)
        form_layout.addRow("Phone:", self.reg_phone_input)
        form_layout.addRow("Role:", self.reg_role_combo)
        form_layout.addRow("Date of Birth:", self.reg_dob_input)
        form_layout.addRow("Blood Type:", self.reg_blood_type_combo)
        form_layout.addRow("Insurance:", self.reg_insurance_input)
        form_layout.addRow("Specialization:", self.reg_specialization_input)
        form_layout.addRow("Department:", self.reg_department_input)
        
        # Register button
        register_btn = QPushButton("Register")
        register_btn.setObjectName("login-btn")
        
        # Back to login link
        login_link = QPushButton("Already have an account? Login here")
        login_link.setFlat(True)
        login_link.setStyleSheet("color: #3b82f6; text-decoration: underline;")
        
        # Add widgets to layout
        layout.addWidget(logo)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(20)
        layout.addLayout(form_layout)
        layout.addSpacing(10)
        layout.addWidget(register_btn)
        layout.addSpacing(10)
        layout.addWidget(login_link)
        
        # Container widget for styling
        container = QWidget()
        container.setObjectName("login-container")
        container.setLayout(layout)
        container.setFixedWidth(450)
        
        # Set page layout
        page_layout = QVBoxLayout(page)
        page_layout.addWidget(container, alignment=Qt.AlignCenter)
        
        # Connect signals
        register_btn.clicked.connect(self.handle_register)
        login_link.clicked.connect(self.show_login_page)
        self.reg_role_combo.currentTextChanged.connect(self.toggle_doctor_fields)
        
        return page
    
    def toggle_doctor_fields(self, role):
        is_doctor = role == "Doctor"
        
        # Show/hide patient fields
        self.reg_dob_input.setVisible(not is_doctor)
        self.reg_blood_type_combo.setVisible(not is_doctor)
        self.reg_insurance_input.setVisible(not is_doctor)
        
        # Show/hide doctor fields
        self.reg_specialization_input.setVisible(is_doctor)
        self.reg_department_input.setVisible(is_doctor)
    
    def show_register_page(self):
        self.stacked_widget.setCurrentIndex(1)
        self.setWindowTitle("MediCare Hospital - Register")
    
    def show_login_page(self):
        self.stacked_widget.setCurrentIndex(0)
        self.setWindowTitle("MediCare Hospital - Login")
    
    def handle_login(self):
        email = self.email_input.text()
        password = self.password_input.text()
        role = self.role_combo.currentText().lower()
        
        if not email or not password:
            QMessageBox.warning(self, "Login Failed", "Please enter both email and password")
            return
            
        user = self.db.get_user(email, password, role)
        if not user:
            QMessageBox.warning(self, "Login Failed", "Invalid email or password")
            return
            
        from ui.main_window import MainWindow
        self.main_app = MainWindow(user, role, self.db)
        self.main_app.show()
        self.close()
        
    def handle_register(self):
        # Get form data
        name = self.reg_name_input.text()
        email = self.reg_email_input.text()
        password = self.reg_password_input.text()
        confirm_password = self.reg_confirm_password_input.text()
        phone = self.reg_phone_input.text()
        role = self.reg_role_combo.currentText().lower()
        
        # Validate inputs
        if not all([name, email, password, confirm_password, phone]):
            QMessageBox.warning(self, "Registration Failed", "Please fill in all required fields")
            return
            
        if password != confirm_password:
            QMessageBox.warning(self, "Registration Failed", "Passwords do not match")
            return
            
        # Check if email already exists
        for user_type in ['patients', 'doctors', 'admins']:
            for user in self.db.data['users'][user_type]:
                if user['email'] == email:
                    QMessageBox.warning(self, "Registration Failed", "Email already registered")
                    return
        
        # Create new user data
        new_user = {
            "id": len(self.db.data['users'][f"{role}s"]) + 1,
            "name": name,
            "email": email,
            "password": password,
            "phone": phone
        }
        
        # Add role-specific fields
        if role == "patient":
            new_user.update({
                "date_of_birth": self.reg_dob_input.date().toString("yyyy-MM-dd"),
                "blood_type": self.reg_blood_type_combo.currentText(),
                "insurance": self.reg_insurance_input.text(),
                "address": ""  # Can be added in profile later
            })
            self.db.data['users']['patients'].append(new_user)
        elif role == "doctor":
            new_user.update({
                "specialization": self.reg_specialization_input.text(),
                "department": self.reg_department_input.text(),
                "schedule": "Mon-Fri, 9AM-5PM"  # Default schedule
            })
            self.db.data['users']['doctors'].append(new_user)
        
        # Save to database
        self.db._save_data(self.db.data)
        
        QMessageBox.information(self, "Registration Successful", 
                              "Account created successfully! You can now login.")
        self.show_login_page()