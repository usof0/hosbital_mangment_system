
from .needs import *

LANGUAGES = {
    'en': {
        'page_title': 'Patient Profile',
        'role': 'Patient',
        'personal_info': '<b>Personal Information</b>',
        'contact_info': '<b>Contact Information</b>',
        'full_name': 'Full Name:',
        'dob': 'Date of Birth:',
        'gender': 'Gender:',
        'blood_type': 'Blood Type:',
        'email': 'Email:',
        'phone': 'Phone:',
        'address': 'Address:',
        'save_btn': 'Save Changes',
        'success_title': 'Success',
        'success_msg': 'Profile updated successfully',
        'error_title': 'Error',
        'error_msg': 'Failed to update profile: {}',
        'genders': ['Male', 'Female', 'Other'],
        'blood_types': ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-', 'Unknown']
    },
    'ru': {
        'page_title': 'Профиль пациента',
        'role': 'Пациент',
        'personal_info': '<b>Личная информация</b>',
        'contact_info': '<b>Контактная информация</b>',
        'full_name': 'Полное имя:',
        'dob': 'Дата рождения:',
        'gender': 'Пол:',
        'blood_type': 'Группа крови:',
        'email': 'Email:',
        'phone': 'Телефон:',
        'address': 'Адрес:',
        'save_btn': 'Сохранить изменения',
        'success_title': 'Успех',
        'success_msg': 'Профиль успешно обновлен',
        'error_title': 'Ошибка',
        'error_msg': 'Ошибка обновления профиля: {}',
        'genders': ['Мужской', 'Женский', 'Другой'],
        'blood_types': ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-', 'Неизвестно']
    }
}

class PatientProfilePage(QWidget):
    def __init__(self, user_data, db, lang='en'):
        super().__init__()
        self.user_data = user_data
        self.db = db
        self.lang = lang
        self.init_ui()
        print(user_data)
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        header = QHBoxLayout()
        avatar = QLabel()
        avatar.setPixmap(QPixmap("assets/icons/user.png").scaled(80, 80))

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
        
        # Form layout
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)
        
        # Personal Info
        self.name_input = QLineEdit(self.user_data.get('name', ''))
        self.dob_input = QDateEdit()
        self.dob_input.setDisplayFormat("yyyy-MM-dd")
        if 'date_of_birth' in self.user_data:
            # self.dob_input.setDate(QDate.fromString(self.user_data['date_of_birth'], "yyyy-MM-dd"))
            dob = self.user_data['date_of_birth']
            self.dob_input.setDate(QDate(dob.year, dob.month, dob.day))
        
        self.gender_input = QComboBox()
        self.gender_input.addItems(LANGUAGES[self.lang]['genders'])
        if 'gender' in self.user_data:
            # Find matching gender in current language
            gender_index = LANGUAGES['en']['genders'].index(self.user_data['gender']) if self.user_data['gender'] in LANGUAGES['en']['genders'] else -1
            if gender_index >= 0:
                self.gender_input.setCurrentIndex(gender_index)
        
        self.blood_type_input = QComboBox()
        self.blood_type_input.addItems(LANGUAGES[self.lang]['blood_types'])
        if 'blood_type' in self.user_data:
            index = self.blood_type_input.findText(self.user_data['blood_type'])
            if index >= 0:
                self.blood_type_input.setCurrentIndex(index)
        
        # Contact Info
        self.email_input = QLineEdit(self.user_data.get('email', ''))
        self.phone_input = QLineEdit(self.user_data.get('phone', ''))
        self.address_input = QTextEdit()
        self.address_input.setPlainText(self.user_data.get('address', ''))
        self.address_input.setMaximumHeight(80)
        
        # Add to form
        form.addRow(QLabel(LANGUAGES[self.lang]['personal_info']))
        form.addRow(LANGUAGES[self.lang]['full_name'], self.name_input)
        form.addRow(LANGUAGES[self.lang]['dob'], self.dob_input)
        form.addRow(LANGUAGES[self.lang]['gender'], self.gender_input)
        form.addRow(LANGUAGES[self.lang]['blood_type'], self.blood_type_input)
        
        form.addRow(QLabel(LANGUAGES[self.lang]['contact_info']))
        form.addRow(LANGUAGES[self.lang]['email'], self.email_input)
        form.addRow(LANGUAGES[self.lang]['phone'], self.phone_input)
        form.addRow(LANGUAGES[self.lang]['address'], self.address_input)
        
        # Save button
        save_btn = QPushButton(LANGUAGES[self.lang]['save_btn'])
        save_btn.setStyleSheet("background-color: #10b981; color: white;")
        save_btn.clicked.connect(self.save_profile)
        
        layout.addLayout(form)
        layout.addWidget(save_btn, alignment=Qt.AlignRight)
        
    def save_profile(self):
        # Convert gender back to English for database storage
        gender_index = self.gender_input.currentIndex()
        gender = LANGUAGES['en']['genders'][gender_index] if gender_index >= 0 else self.gender_input.currentText()
        
        updated_data = {
            'name': self.name_input.text(),
            'dob': self.dob_input.date().toString("yyyy-MM-dd"),
            'gender': gender,
            'blood_type': self.blood_type_input.currentText(),
            'email': self.email_input.text(),
            'phone': self.phone_input.text(),
            'address': self.address_input.toPlainText()
        }
        
        try:
            result = self.db.update_patient_data(self.user_data['id'], updated_data)
            if not result:
                raise

            QMessageBox.information(
                self, 
                LANGUAGES[self.lang]['success_title'], 
                LANGUAGES[self.lang]['success_msg']
            )
        except Exception as e:
            QMessageBox.critical(
                self, 
                LANGUAGES[self.lang]['error_title'], 
                LANGUAGES[self.lang]['error_msg'].format(str(e))
            )