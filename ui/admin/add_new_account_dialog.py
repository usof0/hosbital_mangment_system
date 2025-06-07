from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, 
    QDateEdit, QPushButton, QLabel, QMessageBox, QTimeEdit
)
from PyQt5.QtCore import Qt, QDate, QTime
from typing import Dict


ACCOUNT_LANGUAGES = {
    'en': {
        'titles': {
            'patient': 'Add New Patient',
            'doctor': 'Add New Doctor',
            'admin': 'Add New Admin'
        },
        'form_labels': {
            'name': 'Name:',
            'email': 'Email:',
            'password': 'Password:',
            'phone': 'Phone:',
            'dob': 'Date of Birth:',
            'blood_type': 'Blood Type:',
            'insurance': 'Insurance:',
            'address': 'Address:',
            'specialization': 'Specialization:',
            'department': 'Department:',
            'from_time': 'Working Hours From:',
            'until_time': 'Working Hours Until:',
            'role_detail': 'Role Details:'
        },
        'placeholders': {
            'name': 'Full Name',
            'email': 'Email',
            'password': 'Password',
            'phone': 'Phone Number',
            'insurance': 'Insurance Information',
            'address': 'Address',
            'specialization': 'Specialization',
            'department': 'Department',
            'role_detail': 'Admin Role Details'
        },
        'blood_types': ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
        'buttons': {
            'submit': 'Add {role}',
            'cancel': 'Cancel'
        },
        'messages': {
            'required_fields': 'Name, email, and password are required!',
            'success': '{role} added successfully!',
            'error': 'Failed to add {role}. Please try again.'
        }
    },
    'ru': {
        'titles': {
            'patient': 'Добавить нового пациента',
            'doctor': 'Добавить нового врача',
            'admin': 'Добавить нового администратора'
        },
        'form_labels': {
            'name': 'Имя:',
            'email': 'Email:',
            'password': 'Пароль:',
            'phone': 'Телефон:',
            'dob': 'Дата рождения:',
            'blood_type': 'Группа крови:',
            'insurance': 'Страховка:',
            'address': 'Адрес:',
            'specialization': 'Специализация:',
            'department': 'Отделение:',
            'from_time': 'Рабочие часы с:',
            'until_time': 'Рабочие часы до:',
            'role_detail': 'Детали роли:'
        },
        'placeholders': {
            'name': 'Полное имя',
            'email': 'Email',
            'password': 'Пароль',
            'phone': 'Номер телефона',
            'insurance': 'Информация о страховке',
            'address': 'Адрес',
            'specialization': 'Специализация',
            'department': 'Отделение',
            'role_detail': 'Детали роли администратора'
        },
        'blood_types': ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
        'buttons': {
            'submit': 'Добавить {role}',
            'cancel': 'Отмена'
        },
        'messages': {
            'required_fields': 'Имя, email и пароль обязательны!',
            'success': '{role} успешно добавлен!',
            'error': 'Не удалось добавить {role}. Пожалуйста, попробуйте снова.'
        }
    }
}


class AddNewAccountDialog(QDialog):
    def __init__(self, role: str, db, parent=None, lang='en'):
        super().__init__(parent)
        self.db = db
        self.role = role.lower()
        self.lang = lang
        self.setWindowTitle(ACCOUNT_LANGUAGES[self.lang]['titles'][self.role])
        self.setModal(True)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Common fields for all roles
        form_layout = QFormLayout()
        
        labels = ACCOUNT_LANGUAGES[self.lang]['form_labels']
        placeholders = ACCOUNT_LANGUAGES[self.lang]['placeholders']
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText(placeholders['name'])
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText(placeholders['email'])
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText(placeholders['password'])
        self.password_input.setEchoMode(QLineEdit.Password)
        
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText(placeholders['phone'])
        
        # Add common fields to form
        form_layout.addRow(labels['name'], self.name_input)
        form_layout.addRow(labels['email'], self.email_input)
        form_layout.addRow(labels['password'], self.password_input)
        form_layout.addRow(labels['phone'], self.phone_input)
        
        # Role-specific fields
        if self.role == 'patient':
            self.setup_patient_fields(form_layout, labels, placeholders)
        elif self.role == 'doctor':
            self.setup_doctor_fields(form_layout, labels, placeholders)
        elif self.role == 'admin':
            self.setup_admin_fields(form_layout, labels, placeholders)
        
        # Add form to main layout
        layout.addLayout(form_layout)
        
        # Buttons
        buttons_layout = QVBoxLayout()
        
        role_translation = {
            'patient': 'пациента' if self.lang == 'ru' else 'Patient',
            'doctor': 'врача' if self.lang == 'ru' else 'Doctor',
            'admin': 'администратора' if self.lang == 'ru' else 'Admin'
        }
        
        submit_text = ACCOUNT_LANGUAGES[self.lang]['buttons']['submit'].format(role=role_translation[self.role])
        self.submit_btn = QPushButton(submit_text)
        self.submit_btn.clicked.connect(self.handle_submit)
        
        self.cancel_btn = QPushButton(ACCOUNT_LANGUAGES[self.lang]['buttons']['cancel'])
        self.cancel_btn.clicked.connect(self.reject)
        
        buttons_layout.addWidget(self.submit_btn)
        buttons_layout.addWidget(self.cancel_btn)
        layout.addLayout(buttons_layout)
    
    def setup_patient_fields(self, form_layout, labels, placeholders):
        """Add patient-specific fields to the form"""
        self.dob_input = QDateEdit()
        self.dob_input.setDisplayFormat("yyyy-MM-dd")
        self.dob_input.setDate(QDate.currentDate().addYears(-18))
        self.dob_input.setCalendarPopup(True)
        
        self.blood_type_combo = QComboBox()
        self.blood_type_combo.addItems(ACCOUNT_LANGUAGES[self.lang]['blood_types'])
        
        self.insurance_input = QLineEdit()
        self.insurance_input.setPlaceholderText(placeholders['insurance'])
        
        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText(placeholders['address'])
        
        form_layout.addRow(labels['dob'], self.dob_input)
        form_layout.addRow(labels['blood_type'], self.blood_type_combo)
        form_layout.addRow(labels['insurance'], self.insurance_input)
        form_layout.addRow(labels['address'], self.address_input)
    
    def setup_doctor_fields(self, form_layout, labels, placeholders):
        """Add doctor-specific fields to the form"""
        self.specialization_input = QLineEdit()
        self.specialization_input.setPlaceholderText(placeholders['specialization'])
        
        self.department_input = QLineEdit()
        self.department_input.setPlaceholderText(placeholders['department'])
        
        self.from_time_input = QTimeEdit()
        self.from_time_input.setDisplayFormat("hh:mm AP" if self.lang == 'en' else "hh:mm")
        self.from_time_input.setTime(QTime(9, 0))  # Default 9:00 AM
        
        self.until_time_input = QTimeEdit()
        self.until_time_input.setDisplayFormat("hh:mm AP" if self.lang == 'en' else "hh:mm")
        self.until_time_input.setTime(QTime(17, 0))  # Default 5:00 PM
        
        form_layout.addRow(labels['specialization'], self.specialization_input)
        form_layout.addRow(labels['department'], self.department_input)
        form_layout.addRow(labels['from_time'], self.from_time_input)
        form_layout.addRow(labels['until_time'], self.until_time_input)
    
    def setup_admin_fields(self, form_layout, labels, placeholders):
        """Add admin-specific fields to the form"""
        self.role_detail_input = QLineEdit()
        self.role_detail_input.setPlaceholderText(placeholders['role_detail'])
        
        form_layout.addRow(labels['role_detail'], self.role_detail_input)
    
    def handle_submit(self):
        """Handle form submission based on role"""
        # Get common fields
        data = {
            'name': self.name_input.text(),
            'email': self.email_input.text(),
            'password': self.password_input.text(),
            'phone': self.phone_input.text()
        }
        
        # Validate required fields
        if not all([data['name'], data['email'], data['password']]):
            QMessageBox.warning(self, "Error", ACCOUNT_LANGUAGES[self.lang]['messages']['required_fields'])
            return
        
        # Add role-specific fields
        if self.role == 'patient':
            data.update({
                'date_of_birth': self.dob_input.date().toString("yyyy-MM-dd"),
                'blood_type': self.blood_type_combo.currentText(),
                'insurance': self.insurance_input.text(),
                'address': self.address_input.text()
            })
            result = self.db.add_patient(data)
        elif self.role == 'doctor':
            data.update({
                'specialization': self.specialization_input.text(),
                'department': self.department_input.text(),
                'from_time': self.from_time_input.time().toString("hh:mm AP" if self.lang == 'en' else "hh:mm"),
                'until_time': self.until_time_input.time().toString("hh:mm AP" if self.lang == 'en' else "hh:mm")
            })
            result = self.db.add_doctor(data)
        elif self.role == 'admin':
            data.update({
                'role_detail': self.role_detail_input.text()
            })
            result = self.db.add_admin(data)
        
        if result:
            role_translation = {
                'patient': 'пациент' if self.lang == 'ru' else 'Patient',
                'doctor': 'врач' if self.lang == 'ru' else 'Doctor',
                'admin': 'администратор' if self.lang == 'ru' else 'Admin'
            }
            success_msg = ACCOUNT_LANGUAGES[self.lang]['messages']['success'].format(role=role_translation[self.role])
            QMessageBox.information(self, "Success", success_msg)
            self.accept()
        else:
            error_msg = ACCOUNT_LANGUAGES[self.lang]['messages']['error'].format(role=role_translation[self.role])
            QMessageBox.warning(self, "Error", error_msg)