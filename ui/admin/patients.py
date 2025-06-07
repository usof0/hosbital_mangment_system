from .needs import *
from datetime import date

LANGUAGES = {
    'en': {
        'page_title': 'Manage Patients',
        'refresh_button': 'Refresh',
        'table_headers': ["ID", "Name", "Age", "Phone", "Actions"],
        'form_title': 'Add/Edit Patient',
        'form_labels': {
            'patient_id': 'Patient ID:',
            'full_name': 'Full Name:',
            'email': 'Email:',
            'phone': 'Phone:',
            'gender': 'Gender:',
            'dob': 'Date of Birth:',
            'blood_type': 'Blood Type:',
            'address': 'Address:'
        },
        'patient_id_placeholder': 'Auto-generated',
        'genders': ["Male", "Female", "Other"],
        'blood_types': ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", "Unknown"],
        'buttons': {
            'save': 'Save',
            'clear': 'Clear',
            'edit': 'Edit',
            'delete': 'Delete'
        },
        'messages': {
            'confirm_delete': 'Are you sure you want to delete {name}?',
            'delete_success': 'Patient deleted successfully',
            'delete_error': 'Failed to delete patient: {error}',
            'save_success': 'Patient {action} successfully',
            'save_error': 'Failed to save patient: {error}',
            'name_required': 'Name is required',
            'age_na': 'N/A'
        }
    },
    'ru': {
        'page_title': 'Управление пациентами',
        'refresh_button': 'Обновить',
        'table_headers': ["ID", "Имя", "Возраст", "Телефон", "Действия"],
        'form_title': 'Добавить/Редактировать пациента',
        'form_labels': {
            'patient_id': 'ID пациента:',
            'full_name': 'Полное имя:',
            'email': 'Email:',
            'phone': 'Телефон:',
            'gender': 'Пол:',
            'dob': 'Дата рождения:',
            'blood_type': 'Группа крови:',
            'address': 'Адрес:'
        },
        'patient_id_placeholder': 'Автогенерация',
        'genders': ["Мужской", "Женский", "Другой"],
        'blood_types': ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", "Неизвестно"],
        'buttons': {
            'save': 'Сохранить',
            'clear': 'Очистить',
            'edit': 'Редактировать',
            'delete': 'Удалить'
        },
        'messages': {
            'confirm_delete': 'Вы уверены, что хотите удалить {name}?',
            'delete_success': 'Пациент успешно удален',
            'delete_error': 'Ошибка при удалении пациента: {error}',
            'save_success': 'Пациент успешно {action}',
            'save_error': 'Ошибка при сохранении пациента: {error}',
            'name_required': 'Имя обязательно для заполнения',
            'age_na': 'Н/Д'
        }
    }
}


class ManagePatientsPage(QWidget):
    def __init__(self, user_data, db, lang='en'):
        super().__init__()
        self.user_data = user_data
        self.db = db
        self.lang = lang
        self.init_ui()
        
    def init_ui(self):
        self.setup_main_layout()
        self.setup_header()
        self.setup_patient_table()
        self.setup_patient_form()
        self.load_patients()
        
    def setup_main_layout(self):
        self.layout = QVBoxLayout(self)
        
    def setup_header(self):
        header = QHBoxLayout()
        
        title = QLabel(LANGUAGES[self.lang]['page_title'])
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        
        refresh_btn = QPushButton(LANGUAGES[self.lang]['refresh_button'])
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
        """)
        refresh_btn.clicked.connect(self.load_patients)
        
        header.addWidget(title)
        header.addStretch()
        header.addWidget(refresh_btn)
        
        self.layout.addLayout(header)
        
    def setup_patient_table(self):
        self.patients_table = QTableWidget()
        self.patients_table.setColumnCount(5)
        self.patients_table.setHorizontalHeaderLabels(
            LANGUAGES[self.lang]['table_headers']
        )
        self.patients_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.patients_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.patients_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        self.layout.addWidget(self.patients_table)
        
    def setup_patient_form(self):
        group = QGroupBox(LANGUAGES[self.lang]['form_title'])
        group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                border: 1px solid #e5e7eb;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
        """)
        
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)
        
        self.patient_id = QLineEdit()
        self.patient_id.setPlaceholderText(LANGUAGES[self.lang]['patient_id_placeholder'])
        self.patient_id.setReadOnly(True)
        
        self.patient_name = QLineEdit()
        self.patient_email = QLineEdit()
        self.patient_phone = QLineEdit()
        
        self.patient_gender = QComboBox()
        self.patient_gender.addItems(LANGUAGES[self.lang]['genders'])
        
        self.patient_dob = QDateEdit()
        self.patient_dob.setDisplayFormat("yyyy-MM-dd")
        self.patient_dob.setCalendarPopup(True)
        self.patient_dob.setMaximumDate(QDate.currentDate())
        self.patient_dob.setDate(QDate.currentDate().addYears(-30))
        
        self.patient_blood_type = QComboBox()
        self.patient_blood_type.addItems(LANGUAGES[self.lang]['blood_types'])
        
        self.patient_address = QTextEdit()
        self.patient_address.setMaximumHeight(80)
        
        # Buttons
        btn_layout = QHBoxLayout()
        save_btn = QPushButton(LANGUAGES[self.lang]['buttons']['save'])
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
        save_btn.clicked.connect(self.save_patient)
        
        clear_btn = QPushButton(LANGUAGES[self.lang]['buttons']['clear'])
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #ef4444;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #dc2626;
            }
        """)
        clear_btn.clicked.connect(self.clear_form)
        
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(clear_btn)
        
        labels = LANGUAGES[self.lang]['form_labels']
        form.addRow(labels['patient_id'], self.patient_id)
        form.addRow(labels['full_name'], self.patient_name)
        form.addRow(labels['email'], self.patient_email)
        form.addRow(labels['phone'], self.patient_phone)
        form.addRow(labels['gender'], self.patient_gender)
        form.addRow(labels['dob'], self.patient_dob)
        form.addRow(labels['blood_type'], self.patient_blood_type)
        form.addRow(labels['address'], self.patient_address)
        form.addRow(btn_layout)
        
        group.setLayout(form)
        self.layout.addWidget(group)
        
    def load_patients(self):
        patients = self.db.get_all_patients()
        self.patients_table.setRowCount(len(patients))
        
        for row_idx, patient in enumerate(patients):
            dob_python = patient.get('date_of_birth', None)
            
            if dob_python and isinstance(dob_python, date):
                dob_str = dob_python.strftime("%Y-%m-%d")
                dob = QDate.fromString(dob_str, "yyyy-MM-dd")
                age = QDate.currentDate().year() - dob.year() if dob.isValid() else LANGUAGES[self.lang]['messages']['age_na']
            else:
                age = LANGUAGES[self.lang]['messages']['age_na']
            
            items = [
                QTableWidgetItem(str(patient.get('id', ''))),
                QTableWidgetItem(patient['name']),
                QTableWidgetItem(str(age)),
                QTableWidgetItem(patient.get('phone', ''))
            ]
            
            # Action buttons
            edit_btn = QPushButton(LANGUAGES[self.lang]['buttons']['edit'])
            edit_btn.setStyleSheet("""
                QPushButton {
                    background-color: #3b82f6;
                    color: white;
                    padding: 5px 10px;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #2563eb;
                }
            """)
            edit_btn.clicked.connect(lambda _, p=patient: self.edit_patient(p))
            
            delete_btn = QPushButton(LANGUAGES[self.lang]['buttons']['delete'])
            delete_btn.setStyleSheet("""
                QPushButton {
                    background-color: #ef4444;
                    color: white;
                    padding: 5px 10px;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #dc2626;
                }
            """)
            delete_btn.clicked.connect(lambda _, p=patient: self.delete_patient(p))
            
            btn_widget = QWidget()
            btn_layout = QHBoxLayout(btn_widget)
            btn_layout.addWidget(edit_btn)
            btn_layout.addWidget(delete_btn)
            btn_layout.setContentsMargins(0, 0, 0, 0)
            
            for col_idx, item in enumerate(items):
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.patients_table.setItem(row_idx, col_idx, item)
            
            self.patients_table.setCellWidget(row_idx, 4, btn_widget)
        
        self.patients_table.resizeColumnsToContents()
        
    def edit_patient(self, patient):
        self.patient_id.setText(str(patient.get('id', '')))
        self.patient_name.setText(patient['name'])
        self.patient_email.setText(patient.get('email', ''))
        self.patient_phone.setText(patient.get('phone', ''))
        
        index = self.patient_gender.findText(patient.get('gender', ''))
        if index >= 0:
            self.patient_gender.setCurrentIndex(index)
            
        if 'date_of_birth' in patient and patient['date_of_birth']:
            dob_str = patient['date_of_birth'].strftime("%Y-%m-%d") if isinstance(patient['date_of_birth'], date) else patient['date_of_birth']
            self.patient_dob.setDate(QDate.fromString(dob_str, "yyyy-MM-dd"))
            
        index = self.patient_blood_type.findText(patient.get('blood_type', LANGUAGES[self.lang]['blood_types'][-1]))
        if index >= 0:
            self.patient_blood_type.setCurrentIndex(index)
            
        self.patient_address.setPlainText(patient.get('address', ''))
        
    def delete_patient(self, patient):
        reply = QMessageBox.question(
            self, LANGUAGES[self.lang]['messages']['confirm_delete'].format(name=patient['name']),
            LANGUAGES[self.lang]['messages']['confirm_delete'].format(name=patient['name']),
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.db.delete_patient(patient['id'])
                QMessageBox.information(self, "Success", LANGUAGES[self.lang]['messages']['delete_success'])
                self.load_patients()
            except Exception as e:
                QMessageBox.critical(self, "Error", LANGUAGES[self.lang]['messages']['delete_error'].format(error=str(e)))
        
    def save_patient(self):
        patient_data = {
            'name': self.patient_name.text(),
            'email': self.patient_email.text(),
            'phone': self.patient_phone.text(),
            'gender': self.patient_gender.currentText(),
            'date_of_birth': self.patient_dob.date().toString("yyyy-MM-dd"),
            'blood_type': self.patient_blood_type.currentText(),
            'address': self.patient_address.toPlainText()
        }
        
        if not patient_data['name']:
            QMessageBox.warning(self, "Error", LANGUAGES[self.lang]['messages']['name_required'])
            return
            
        try:
            if self.patient_id.text():  # Update existing
                patient_data['id'] = int(self.patient_id.text())
                self.db.update_patient_data(patient_data['id'], patient_data)
                action = "updated" if self.lang == 'en' else "обновлен"
                QMessageBox.information(self, "Success", LANGUAGES[self.lang]['messages']['save_success'].format(action=action))
            else:  # Create new
                self.db.add_patient(patient_data)
                action = "added" if self.lang == 'en' else "добавлен"
                QMessageBox.information(self, "Success", LANGUAGES[self.lang]['messages']['save_success'].format(action=action))
                
            self.clear_form()
            self.load_patients()
        except Exception as e:
            QMessageBox.critical(self, "Error", LANGUAGES[self.lang]['messages']['save_error'].format(error=str(e)))
        
    def clear_form(self):
        self.patient_id.clear()
        self.patient_name.clear()
        self.patient_email.clear()
        self.patient_phone.clear()
        self.patient_gender.setCurrentIndex(0)
        self.patient_dob.setDate(QDate.currentDate().addYears(-30))
        self.patient_blood_type.setCurrentIndex(0)
        self.patient_address.clear()