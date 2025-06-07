from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
                            QComboBox, QCheckBox, QHBoxLayout, QFormLayout, QMessageBox,
                            QStackedWidget, QDateEdit)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont, QPixmap
from db import HospitalDatabase
    

LANGUAGES = {
    'en': {
        'app_title': 'MediCare Hospital',
        'login_title': 'Login',
        'login_subtitle': 'Please login to access your dashboard',
        'email_label': 'Email:',
        'password_label': 'Password:',
        'role_label': 'Login as:',
        'remember_me': 'Remember me',
        'forgot_password': 'Forgot password?',
        'login_button': 'Login',
        'register_prompt': "Don't have an account? Register here",
        'register_title': 'Register New Account',
        'register_subtitle': 'Please fill in your details',
        'name_label': 'Full Name:',
        'confirm_password_label': 'Confirm Password:',
        'phone_label': 'Phone Number:',
        'dob_label': 'Date of Birth:',
        'blood_type_label': 'Blood Type:',
        'insurance_label': 'Insurance:',
        'specialization_label': 'Specialization:',
        'department_label': 'Department:',
        'register_button': 'Register',
        'login_prompt': 'Already have an account? Login here',
        'patient_role': 'Patient',
        'doctor_role': 'Doctor',
        'admin_role': 'Admin'
    },
    'ru': {
        'app_title': 'Больница MediCare',
        'login_title': 'Вход',
        'login_subtitle': 'Пожалуйста, войдите в систему',
        'email_label': 'Email:',
        'password_label': 'Пароль:',
        'role_label': 'Войти как:',
        'remember_me': 'Запомнить меня',
        'forgot_password': 'Забыли пароль?',
        'login_button': 'Войти',
        'register_prompt': "Нет аккаунта? Зарегистрируйтесь",
        'register_title': 'Регистрация',
        'register_subtitle': 'Пожалуйста, заполните данные',
        'name_label': 'Полное имя:',
        'confirm_password_label': 'Подтвердите пароль:',
        'phone_label': 'Телефон:',
        'dob_label': 'Дата рождения:',
        'blood_type_label': 'Группа крови:',
        'insurance_label': 'Страховка:',
        'specialization_label': 'Специализация:',
        'department_label': 'Отделение:',
        'register_button': 'Зарегистрироваться',
        'login_prompt': 'Уже есть аккаунт? Войти',
        'patient_role': 'Пациент',
        'doctor_role': 'Врач',
        'admin_role': 'Админ'
    }
}

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        # self.db = HospitalDatabase()
        self.db = HospitalDatabase()
        self.current_lang = 'en'  # default language
        self.setWindowTitle(LANGUAGES[self.current_lang]['app_title'])
        self.setFixedSize(600, 800)
        
        self.init_ui()
        
    def init_ui(self):
        self.setObjectName("login-page")
        
        # Language switcher
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(['EN', 'RU'])
        self.lang_combo.setCurrentText(self.current_lang.upper())
        self.lang_combo.currentTextChanged.connect(self.change_language)
        
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
        main_layout.addWidget(self.lang_combo, alignment=Qt.AlignRight)
        main_layout.addWidget(self.stacked_widget)
        
    def change_language(self, lang_code):
        self.current_lang = lang_code.lower()
        self.setWindowTitle(LANGUAGES[self.current_lang]['app_title'])
        self.update_ui_text()
        
    def update_ui_text(self):
        """Update all UI elements with current language text"""
        lang = LANGUAGES[self.current_lang]
        
        # Update login page
        self.login_title.setText(lang['login_title'])
        self.login_subtitle.setText(lang['login_subtitle'])
        self.email_label.setText(lang['email_label'])
        self.password_label.setText(lang['password_label'])
        self.reg_role_label.setText(lang['role_label'])
        self.remember_check.setText(lang['remember_me'])
        self.forgot_password.setText(lang['forgot_password'])
        self.login_btn.setText(lang['login_button'])
        self.register_link.setText(lang['register_prompt'])
        
        # Update role combo items
        # self.role_combo.clear()
        # self.role_combo.addItems([lang['patient_role'], lang['doctor_role'], lang['admin_role']])
        
        # Update register page
        self.register_title.setText(lang['register_title'])
        self.register_subtitle.setText(lang['register_subtitle'])
        self.reg_name_label.setText(lang['name_label'])
        self.reg_email_label.setText(lang['email_label'])
        self.reg_password_label.setText(lang['password_label'])
        self.reg_confirm_password_label.setText(lang['confirm_password_label'])
        self.reg_phone_label.setText(lang['phone_label'])
        self.reg_role_label.setText(lang['role_label'])
        self.reg_dob_label.setText(lang['dob_label'])
        self.reg_blood_type_label.setText(lang['blood_type_label'])
        self.reg_insurance_label.setText(lang['insurance_label'])
        self.reg_specialization_label.setText(lang['specialization_label'])
        self.reg_department_label.setText(lang['department_label'])
        self.register_btn.setText(lang['register_button'])
        self.login_link.setText(lang['login_prompt'])
        
        # Update role combo items in register page
        self.reg_role_combo.clear()
        self.reg_role_combo.addItems([lang['patient_role'], lang['doctor_role']])
        
    def create_login_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        # Logo and title
        logo = QLabel()
        logo.setPixmap(QPixmap("assets/icons/hospital.png").scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignCenter)
        
        self.login_title = QLabel(LANGUAGES[self.current_lang]['login_title'])
        self.login_title.setObjectName("login-title")
        self.login_title.setAlignment(Qt.AlignCenter)
        self.login_title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        
        self.login_subtitle = QLabel(LANGUAGES[self.current_lang]['login_subtitle'])
        self.login_subtitle.setObjectName("login-subtitle")
        self.login_subtitle.setAlignment(Qt.AlignCenter)
        
        # Form
        form_layout = QFormLayout()
        
        self.email_label = QLabel(LANGUAGES[self.current_lang]['email_label'])
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText(LANGUAGES[self.current_lang]['email_label'])
        
        self.password_label = QLabel(LANGUAGES[self.current_lang]['password_label'])
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText(LANGUAGES[self.current_lang]['password_label'])
        self.password_input.setEchoMode(QLineEdit.Password)
        
        # self.role_label = QLabel(LANGUAGES[self.current_lang]['role_label'])
        # self.role_combo = QComboBox()
        # self.role_combo.addItems([
        #     LANGUAGES[self.current_lang]['patient_role'],
        #     LANGUAGES[self.current_lang]['doctor_role'],
        #     LANGUAGES[self.current_lang]['admin_role']
        # ])
        
        form_layout.addRow(self.email_label, self.email_input)
        form_layout.addRow(self.password_label, self.password_input)
        # form_layout.addRow(self.role_label, self.role_combo)
        
        # Remember me and forgot password
        self.remember_check = QCheckBox(LANGUAGES[self.current_lang]['remember_me'])
        self.forgot_password = QPushButton(LANGUAGES[self.current_lang]['forgot_password'])
        self.forgot_password.setFlat(True)
        self.forgot_password.setStyleSheet("color: #ffffff; text-decoration: underline;")
        
        remember_layout = QHBoxLayout()
        remember_layout.addWidget(self.remember_check)
        remember_layout.addWidget(self.forgot_password)
        
        # Login button
        self.login_btn = QPushButton(LANGUAGES[self.current_lang]['login_button'])
        self.login_btn.setObjectName("login-btn")
        
        # Register link
        self.register_link = QPushButton(LANGUAGES[self.current_lang]['register_prompt'])
        self.register_link.setFlat(True)
        self.register_link.setStyleSheet("color: #ffffff; text-decoration: underline;")
        
        # Add widgets to layout
        layout.addWidget(logo)
        layout.addWidget(self.login_title)
        layout.addWidget(self.login_subtitle)
        layout.addSpacing(20)
        layout.addLayout(form_layout)
        layout.addLayout(remember_layout)
        layout.addSpacing(10)
        layout.addWidget(self.login_btn)
        layout.addSpacing(10)
        layout.addWidget(self.register_link)
        
        # Container widget for styling
        container = QWidget()
        container.setObjectName("login-container")
        container.setLayout(layout)
        container.setFixedWidth(400)
        
        # Set page layout
        page_layout = QVBoxLayout(page)
        page_layout.addWidget(container, alignment=Qt.AlignCenter)
        
        # Connect signals
        self.login_btn.clicked.connect(self.handle_login)
        self.register_link.clicked.connect(self.show_register_page)
        
        return page
    
    def create_register_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        # Logo and title
        logo = QLabel()
        logo.setPixmap(QPixmap("assets/icons/hospital.png").scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignCenter)
        
        self.register_title = QLabel(LANGUAGES[self.current_lang]['register_title'])
        self.register_title.setObjectName("login-title")
        self.register_title.setAlignment(Qt.AlignCenter)
        self.register_title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        
        self.register_subtitle = QLabel(LANGUAGES[self.current_lang]['register_subtitle'])
        self.register_subtitle.setObjectName("login-subtitle")
        self.register_subtitle.setAlignment(Qt.AlignCenter)
        
        # Form
        form_layout = QFormLayout()
        
        # Create labels and inputs
        self.reg_name_label = QLabel(LANGUAGES[self.current_lang]['name_label'])
        self.reg_name_input = QLineEdit()
        self.reg_name_input.setPlaceholderText(LANGUAGES[self.current_lang]['name_label'])
        
        self.reg_email_label = QLabel(LANGUAGES[self.current_lang]['email_label'])
        self.reg_email_input = QLineEdit()
        self.reg_email_input.setPlaceholderText(LANGUAGES[self.current_lang]['email_label'])
        
        self.reg_password_label = QLabel(LANGUAGES[self.current_lang]['password_label'])
        self.reg_password_input = QLineEdit()
        self.reg_password_input.setPlaceholderText(LANGUAGES[self.current_lang]['password_label'])
        self.reg_password_input.setEchoMode(QLineEdit.Password)
        
        self.reg_confirm_password_label = QLabel(LANGUAGES[self.current_lang]['confirm_password_label'])
        self.reg_confirm_password_input = QLineEdit()
        self.reg_confirm_password_input.setPlaceholderText(LANGUAGES[self.current_lang]['confirm_password_label'])
        self.reg_confirm_password_input.setEchoMode(QLineEdit.Password)
        
        self.reg_phone_label = QLabel(LANGUAGES[self.current_lang]['phone_label'])
        self.reg_phone_input = QLineEdit()
        self.reg_phone_input.setPlaceholderText(LANGUAGES[self.current_lang]['phone_label'])
        
        self.reg_role_label = QLabel(LANGUAGES[self.current_lang]['role_label'])
        self.reg_role_combo = QComboBox()
        self.reg_role_combo.addItems([
            LANGUAGES[self.current_lang]['patient_role'],
            LANGUAGES[self.current_lang]['doctor_role']
        ])
        
        self.reg_dob_label = QLabel(LANGUAGES[self.current_lang]['dob_label'])
        self.reg_dob_input = QDateEdit()
        self.reg_dob_input.setDisplayFormat("yyyy-MM-dd")
        self.reg_dob_input.setDate(QDate.currentDate().addYears(-18))
        self.reg_dob_input.setCalendarPopup(True)
        
        self.reg_blood_type_label = QLabel(LANGUAGES[self.current_lang]['blood_type_label'])
        self.reg_blood_type_combo = QComboBox()
        self.reg_blood_type_combo.addItems(["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        
        self.reg_insurance_label = QLabel(LANGUAGES[self.current_lang]['insurance_label'])
        self.reg_insurance_input = QLineEdit()
        self.reg_insurance_input.setPlaceholderText(LANGUAGES[self.current_lang]['insurance_label'])
        
        # Doctor-specific fields
        self.reg_specialization_label = QLabel(LANGUAGES[self.current_lang]['specialization_label'])
        self.reg_specialization_input = QLineEdit()
        self.reg_specialization_input.setPlaceholderText(LANGUAGES[self.current_lang]['specialization_label'])
        self.reg_specialization_input.setVisible(False)
        
        self.reg_department_label = QLabel(LANGUAGES[self.current_lang]['department_label'])
        self.reg_department_input = QLineEdit()
        self.reg_department_input.setPlaceholderText(LANGUAGES[self.current_lang]['department_label'])
        self.reg_department_input.setVisible(False)
        
        # Add fields to form
        form_layout.addRow(self.reg_name_label, self.reg_name_input)
        form_layout.addRow(self.reg_email_label, self.reg_email_input)
        form_layout.addRow(self.reg_password_label, self.reg_password_input)
        form_layout.addRow(self.reg_confirm_password_label, self.reg_confirm_password_input)
        form_layout.addRow(self.reg_phone_label, self.reg_phone_input)
        form_layout.addRow(self.reg_role_label, self.reg_role_combo)
        form_layout.addRow(self.reg_dob_label, self.reg_dob_input)
        form_layout.addRow(self.reg_blood_type_label, self.reg_blood_type_combo)
        form_layout.addRow(self.reg_insurance_label, self.reg_insurance_input)
        form_layout.addRow(self.reg_specialization_label, self.reg_specialization_input)
        form_layout.addRow(self.reg_department_label, self.reg_department_input)
        
        # Register button
        self.register_btn = QPushButton(LANGUAGES[self.current_lang]['register_button'])
        self.register_btn.setObjectName("login-btn")
        
        # Back to login link
        self.login_link = QPushButton(LANGUAGES[self.current_lang]['login_prompt'])
        self.login_link.setFlat(True)
        self.login_link.setStyleSheet("color: #ffffff; text-decoration: underline;")
        
        # Add widgets to layout
        layout.addWidget(logo)
        layout.addWidget(self.register_title)
        # layout.addWidget(self.register_subtitle)
        layout.addSpacing(20)
        layout.addLayout(form_layout)
        layout.addSpacing(10)
        layout.addWidget(self.register_btn)
        layout.addSpacing(10)
        layout.addWidget(self.login_link)
        
        # Container widget for styling
        container = QWidget()
        container.setObjectName("login-container")
        container.setLayout(layout)
        container.setFixedWidth(450)
        
        # Set page layout
        page_layout = QVBoxLayout(page)
        page_layout.addWidget(container, alignment=Qt.AlignCenter)
        
        # Connect signals
        self.register_btn.clicked.connect(self.handle_register)
        self.login_link.clicked.connect(self.show_login_page)
        self.reg_role_combo.currentTextChanged.connect(self.toggle_doctor_fields)
        
        return page
    
    # ... rest of the methods remain the same ...

    def toggle_doctor_fields(self, role):
        is_doctor = role == "Doctor" or role == 'Врач'
        
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
        # role = self.role_combo.currentText().lower()
        # if self.current_lang == 'ru':
        #     if role == 'пациент':
        #         role = 'patient'
        #     elif role == 'врач':
        #         role = 'doctor'
        #     else:
        #         role = 'admin'
        
        if not email or not password:
            QMessageBox.warning(self, "Login Failed", "Please enter both email and password")
            return
        
        user = self.db.get_user(email, password)

        if not user:
            QMessageBox.warning(self, "Login Failed", "Invalid email or password")
            return
            
        role = user['role']
        from ui.main_window import MainWindow
        self.main_app = MainWindow(user, role, self.db, self.current_lang)
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
            
        try:
            # Check if email already exists
            if role == 'patient' or role =='Пациент':
                existing_user = self.db.get_patient_by_email(email)
            elif role == 'doctor' or role == 'Врач':
                existing_user = self.db.get_doctor_by_email(email)
            else:
                existing_user = None
                
            if existing_user:
                QMessageBox.warning(self, "Registration Failed", "Email already registered")
                return
            
            # Create new user data
            user_data = {
                "name": name,
                "email": email,
                "password": password,
                "phone": phone
            }
            
            # Add role-specific fields and create the user
            if role == "patient":
                user_data.update({
                    "date_of_birth": self.reg_dob_input.date().toString("yyyy-MM-dd"),
                    "blood_type": self.reg_blood_type_combo.currentText(),
                    "insurance": self.reg_insurance_input.text(),
                    "address": ""  # Can be added in profile later
                })
                new_user = self.db.add_patient(user_data)
            elif role == "doctor":
                user_data.update({
                    "specialization": self.reg_specialization_input.text(),
                    "department": self.reg_department_input.text(),
                    "from_time": "09:00 AP",
                    "until_time": "05:00 AP",
                })
                new_user = self.db.add_doctor(user_data)
            
            if not new_user:
                QMessageBox.warning(self, "Registration Failed", "Failed to create account. Please try again.")
                return
                
            QMessageBox.information(self, "Registration Successful", 
                                "Account created successfully! You can now login.")
            self.show_login_page()
            
        except Exception as e:
            QMessageBox.warning(self, "Registration Error", f"An error occurred: {str(e)}")
            print(f"Registration error: {e}")
