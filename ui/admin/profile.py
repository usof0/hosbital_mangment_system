from .needs import *

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFormLayout, QLineEdit, QMessageBox
)
from PyQt5.QtCore import Qt

LANGUAGES = {
    'en': {
        'page_title': 'My Profile',
        'save_button': 'Save Changes',
        'form_labels': {
            'name': 'Full Name',
            'email': 'Email',
            'phone': 'Phone',
            'current_password': 'Current Password',
            'new_password': 'New Password',
            'confirm_password': 'Confirm Password'
        },
        'messages': {
            'success_title': 'Success',
            'profile_updated': 'Profile updated successfully',
            'error_title': 'Error',
            'password_mismatch': 'New passwords don\'t match',
            'incorrect_password': 'Current password is incorrect',
            'update_error': 'Failed to update profile: {error}'
        }
    },
    'ru': {
        'page_title': 'Мой профиль',
        'save_button': 'Сохранить изменения',
        'form_labels': {
            'name': 'Полное имя',
            'email': 'Электронная почта',
            'phone': 'Телефон',
            'current_password': 'Текущий пароль',
            'new_password': 'Новый пароль',
            'confirm_password': 'Подтвердите пароль'
        },
        'messages': {
            'success_title': 'Успех',
            'profile_updated': 'Профиль успешно обновлен',
            'error_title': 'Ошибка',
            'password_mismatch': 'Новые пароли не совпадают',
            'incorrect_password': 'Текущий пароль неверен',
            'update_error': 'Ошибка при обновлении профиля: {error}'
        }
    }
}

class AdminProfilePage(QWidget):
    def __init__(self, user_data, db, lang='en'):
        super().__init__()
        self.user_data = user_data
        self.db = db
        self.lang = lang
        self.init_ui()
        
    def init_ui(self):
        self.setup_main_layout()
        self.setup_header()
        self.setup_profile_form()
        
    def setup_main_layout(self):
        self.layout = QVBoxLayout(self)
        
    def setup_header(self):
        header = QHBoxLayout()
        
        title = QLabel(LANGUAGES[self.lang]['page_title'])
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        
        save_btn = QPushButton(LANGUAGES[self.lang]['save_button'])
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        save_btn.clicked.connect(self.save_profile)
        
        header.addWidget(title)
        header.addStretch()
        header.addWidget(save_btn)
        
        self.layout.addLayout(header)
        
    def setup_profile_form(self):
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)
        
        lang = LANGUAGES[self.lang]
        
        self.name = QLineEdit(self.user_data.get('name', ''))
        self.email = QLineEdit(self.user_data.get('email', ''))
        self.phone = QLineEdit(self.user_data.get('phone', ''))
        
        self.current_password = QLineEdit()
        self.current_password.setEchoMode(QLineEdit.Password)
        
        self.new_password = QLineEdit()
        self.new_password.setEchoMode(QLineEdit.Password)
        
        self.confirm_password = QLineEdit()
        self.confirm_password.setEchoMode(QLineEdit.Password)
        
        form.addRow(lang['form_labels']['name'] + ":", self.name)
        form.addRow(lang['form_labels']['email'] + ":", self.email)
        form.addRow(lang['form_labels']['phone'] + ":", self.phone)
        form.addRow(lang['form_labels']['current_password'] + ":", self.current_password)
        form.addRow(lang['form_labels']['new_password'] + ":", self.new_password)
        form.addRow(lang['form_labels']['confirm_password'] + ":", self.confirm_password)
        
        self.layout.addLayout(form)
        
    def save_profile(self):
        profile_data = {
            'name': self.name.text(),
            'email': self.email.text(),
            'phone': self.phone.text()
        }
        
        # Password change logic
        current_pass = self.current_password.text()
        new_pass = self.new_password.text()
        confirm_pass = self.confirm_password.text()
        
        lang = LANGUAGES[self.lang]['messages']
        
        if current_pass or new_pass or confirm_pass:
            if new_pass != confirm_pass:
                QMessageBox.warning(
                    self, 
                    lang['error_title'],
                    lang['password_mismatch']
                )
                return
                
            # Verify current password
            if not self.db.verify_password(self.user_data['id'], current_pass):
                QMessageBox.warning(
                    self, 
                    lang['error_title'],
                    lang['incorrect_password']
                )
                return
                
            profile_data['password'] = new_pass
        
        try:
            self.db.update_admin_data(self.user_data['id'], profile_data)
            QMessageBox.information(
                self, 
                lang['success_title'],
                lang['profile_updated']
            )
            
            # Update user data in memory
            self.user_data.update(profile_data)
            
        except Exception as e:
            QMessageBox.critical(
                self, 
                lang['error_title'],
                lang['update_error'].format(error=str(e))
            )