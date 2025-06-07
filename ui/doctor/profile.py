from .needs import *

LANGUAGES = {
    'en': {
        'role': 'Doctor',
        'form_labels': {
            'specialization': 'Specialization',
            'department': 'Department',
            'email': 'Email',
            'phone': 'Phone'
        },
        'save_button': 'Save Profile',
        'messages': {
            'success_title': 'Success',
            'success_text': 'Profile updated successfully!',
            'error_title': 'Error',
            'error_text': 'Failed to update profile'
        }
    },
    'ru': {
        'role': 'Врач',
        'form_labels': {
            'specialization': 'Специализация',
            'department': 'Отделение',
            'email': 'Электронная почта',
            'phone': 'Телефон'
        },
        'save_button': 'Сохранить профиль',
        'messages': {
            'success_title': 'Успех',
            'success_text': 'Профиль успешно обновлен!',
            'error_title': 'Ошибка',
            'error_text': 'Не удалось обновить профиль'
        }
    }
}

class DoctorProfilePage(QWidget):
    def __init__(self, user_data, db, lang='en'):
        super().__init__()
        self.user_data = user_data
        self.db = db
        self.lang = lang
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Header with avatar and basic info
        header = QHBoxLayout()
        
        # Avatar
        avatar = QLabel()
        avatar.setPixmap(QPixmap("assets/icons/doctor.png").scaled(80, 80))
        avatar.setStyleSheet("margin-right: 15px;")
        
        # Doctor info
        info = QVBoxLayout()
        name = QLabel(self.user_data['name'])
        name.setStyleSheet("font-size: 18px; font-weight: bold;")
        
        role = QLabel(LANGUAGES[self.lang]['role'])
        role.setStyleSheet("font-size: 14px; color: #666;")
        
        info.addWidget(name)
        info.addWidget(role)
        
        header.addWidget(avatar)
        header.addLayout(info)
        layout.addLayout(header)
        
        # Profile form
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)
        form.setSpacing(15)
        
        # Form fields
        self.specialization_input = QLineEdit(self.user_data.get('specialization', ''))
        self.department_input = QLineEdit(self.user_data.get('department', ''))
        self.email_input = QLineEdit(self.user_data.get('email', ''))
        self.phone_input = QLineEdit(self.user_data.get('phone', ''))
        
        # Add form rows with translated labels
        lang_labels = LANGUAGES[self.lang]['form_labels']
        form.addRow(f"{lang_labels['specialization']}:", self.specialization_input)
        form.addRow(f"{lang_labels['department']}:", self.department_input)
        form.addRow(f"{lang_labels['email']}:", self.email_input)
        form.addRow(f"{lang_labels['phone']}:", self.phone_input)
        
        layout.addLayout(form)
        
        # Save button
        save_btn = QPushButton(LANGUAGES[self.lang]['save_button'])
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        save_btn.clicked.connect(self.save_profile)
        layout.addWidget(save_btn, alignment=Qt.AlignRight)
        
    def save_profile(self):
        profile_data = {
            'specialization': self.specialization_input.text(),
            'department': self.department_input.text(),
            'email': self.email_input.text(),
            'phone': self.phone_input.text()
        }
        
        try:
            result = self.db.update_doctor_data(self.user_data['id'], profile_data)
            
            if result:
                QMessageBox.information(
                    self,
                    LANGUAGES[self.lang]['messages']['success_title'],
                    LANGUAGES[self.lang]['messages']['success_text']
                )
                # Update local user data
                self.user_data.update(profile_data)
            else:
                QMessageBox.warning(
                    self,
                    LANGUAGES[self.lang]['messages']['error_title'],
                    LANGUAGES[self.lang]['messages']['error_text']
                )
        except Exception as e:
            QMessageBox.critical(
                self,
                LANGUAGES[self.lang]['messages']['error_title'],
                f"{LANGUAGES[self.lang]['messages']['error_text']}: {str(e)}"
            )
