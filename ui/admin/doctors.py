from .needs import *

LANGUAGES = {
    'en': {
        'page_title': 'Manage Doctors',
        'refresh_button': 'Refresh',
        'table_headers': ["ID", "Name", "Specialization", "Department", "Status", "Actions"],
        'form_title': 'Add/Edit Doctor',
        'form_labels': {
            'doctor_id': 'Doctor ID:',
            'full_name': 'Full Name:',
            'email': 'Email:',
            'phone': 'Phone:',
            'specialization': 'Specialization:',
            'department': 'Department:',
            'status': 'Status:'
        },
        'doctor_id_placeholder': 'Auto-generated',
        'specializations': ["Cardiology", "Neurology", "Pediatrics", "Orthopedics", "Dermatology", "General"],
        'departments': ["Cardiology", "Neurology", "Pediatrics", "Orthopedics", "Dermatology", "General Medicine"],
        'statuses': ["Active", "Inactive", "On Leave"],
        'buttons': {
            'save': 'Save',
            'clear': 'Clear',
            'edit': 'Edit',
            'delete': 'Delete'
        },
        'messages': {
            'confirm_delete': 'Are you sure you want to delete Dr. {name}?',
            'delete_success': 'Doctor deleted successfully',
            'delete_error': 'Failed to delete doctor: {error}',
            'save_success': 'Doctor {action} successfully',
            'save_error': 'Failed to save doctor: {error}',
            'name_required': 'Name is required'
        }
    },
    'ru': {
        'page_title': 'Управление врачами',
        'refresh_button': 'Обновить',
        'table_headers': ["ID", "Имя", "Специализация", "Отделение", "Статус", "Действия"],
        'form_title': 'Добавить/Редактировать врача',
        'form_labels': {
            'doctor_id': 'ID врача:',
            'full_name': 'Полное имя:',
            'email': 'Email:',
            'phone': 'Телефон:',
            'specialization': 'Специализация:',
            'department': 'Отделение:',
            'status': 'Статус:'
        },
        'doctor_id_placeholder': 'Автогенерация',
        'specializations': ["Кардиология", "Неврология", "Педиатрия", "Ортопедия", "Дерматология", "Общая"],
        'departments': ["Кардиология", "Неврология", "Педиатрия", "Ортопедия", "Дерматология", "Общая медицина"],
        'statuses': ["Активен", "Неактивен", "В отпуске"],
        'buttons': {
            'save': 'Сохранить',
            'clear': 'Очистить',
            'edit': 'Редактировать',
            'delete': 'Удалить'
        },
        'messages': {
            'confirm_delete': 'Вы уверены, что хотите удалить врача {name}?',
            'delete_success': 'Врач успешно удален',
            'delete_error': 'Ошибка при удалении врача: {error}',
            'save_success': 'Врач успешно {action}',
            'save_error': 'Ошибка при сохранении врача: {error}',
            'name_required': 'Имя обязательно для заполнения'
        }
    }
}

class ManageDoctorsPage(QWidget):
    def __init__(self, user_data, db, lang='en'):
        super().__init__()
        self.user_data = user_data
        self.db = db
        self.lang = lang
        self.init_ui()
        
    def init_ui(self):
        self.setup_main_layout()
        self.setup_header()
        self.setup_doctor_table()
        self.setup_doctor_form()
        self.load_doctors()
        
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
        refresh_btn.clicked.connect(self.load_doctors)
        
        header.addWidget(title)
        header.addStretch()
        header.addWidget(refresh_btn)
        
        self.layout.addLayout(header)
        
    def setup_doctor_table(self):
        self.doctors_table = QTableWidget()
        self.doctors_table.setColumnCount(6)
        self.doctors_table.setHorizontalHeaderLabels(
            LANGUAGES[self.lang]['table_headers']
        )
        self.doctors_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.doctors_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.doctors_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        self.layout.addWidget(self.doctors_table)
        
    def setup_doctor_form(self):
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
        
        self.doctor_id = QLineEdit()
        self.doctor_id.setPlaceholderText(LANGUAGES[self.lang]['doctor_id_placeholder'])
        self.doctor_id.setReadOnly(True)
        
        self.doctor_name = QLineEdit()
        self.doctor_email = QLineEdit()
        self.doctor_phone = QLineEdit()
        
        self.doctor_specialization = QComboBox()
        self.doctor_specialization.addItems(LANGUAGES[self.lang]['specializations'])
        
        self.doctor_department = QComboBox()
        self.doctor_department.addItems(LANGUAGES[self.lang]['departments'])
        
        self.doctor_status = QComboBox()
        self.doctor_status.addItems(LANGUAGES[self.lang]['statuses'])
        
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
        save_btn.clicked.connect(self.save_doctor)
        
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
        form.addRow(labels['doctor_id'], self.doctor_id)
        form.addRow(labels['full_name'], self.doctor_name)
        form.addRow(labels['email'], self.doctor_email)
        form.addRow(labels['phone'], self.doctor_phone)
        form.addRow(labels['specialization'], self.doctor_specialization)
        form.addRow(labels['department'], self.doctor_department)
        form.addRow(labels['status'], self.doctor_status)
        form.addRow(btn_layout)
        
        group.setLayout(form)
        self.layout.addWidget(group)
        
    def load_doctors(self):
        doctors = self.db.get_all_doctors()
        self.doctors_table.setRowCount(len(doctors))
        
        for row_idx, doctor in enumerate(doctors):
            items = [
                QTableWidgetItem(str(doctor.get('id', ''))),
                QTableWidgetItem(doctor['name']),
                QTableWidgetItem(doctor['specialization']),
                QTableWidgetItem(doctor['department']),
                QTableWidgetItem(doctor.get('status', LANGUAGES[self.lang]['statuses'][0]))
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
            edit_btn.clicked.connect(lambda _, d=doctor: self.edit_doctor(d))
            
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
            delete_btn.clicked.connect(lambda _, d=doctor: self.delete_doctor(d))
            
            btn_widget = QWidget()
            btn_layout = QHBoxLayout(btn_widget)
            btn_layout.addWidget(edit_btn)
            btn_layout.addWidget(delete_btn)
            btn_layout.setContentsMargins(0, 0, 0, 0)
            
            for col_idx, item in enumerate(items):
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.doctors_table.setItem(row_idx, col_idx, item)
            
            self.doctors_table.setCellWidget(row_idx, 5, btn_widget)
        
        self.doctors_table.resizeColumnsToContents()
        
    def edit_doctor(self, doctor):
        self.doctor_id.setText(str(doctor.get('id', '')))
        self.doctor_name.setText(doctor['name'])
        self.doctor_email.setText(doctor.get('email', ''))
        self.doctor_phone.setText(doctor.get('phone', ''))
        
        index = self.doctor_specialization.findText(doctor['specialization'])
        if index >= 0:
            self.doctor_specialization.setCurrentIndex(index)
            
        index = self.doctor_department.findText(doctor['department'])
        if index >= 0:
            self.doctor_department.setCurrentIndex(index)
            
        index = self.doctor_status.findText(doctor.get('status', LANGUAGES[self.lang]['statuses'][0]))
        if index >= 0:
            self.doctor_status.setCurrentIndex(index)
        
    def delete_doctor(self, doctor):
        reply = QMessageBox.question(
            self, LANGUAGES[self.lang]['messages']['confirm_delete'].format(name=doctor['name']),
            LANGUAGES[self.lang]['messages']['confirm_delete'].format(name=doctor['name']),
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.db.delete_doctor(doctor['id'])
                QMessageBox.information(self, "Success", LANGUAGES[self.lang]['messages']['delete_success'])
                self.load_doctors()
            except Exception as e:
                QMessageBox.critical(self, "Error", LANGUAGES[self.lang]['messages']['delete_error'].format(error=str(e)))
        
    def save_doctor(self):
        doctor_data = {
            'name': self.doctor_name.text(),
            'email': self.doctor_email.text(),
            'phone': self.doctor_phone.text(),
            'specialization': self.doctor_specialization.currentText(),
            'department': self.doctor_department.currentText(),
            'status': self.doctor_status.currentText()
        }
        
        if not doctor_data['name']:
            QMessageBox.warning(self, "Error", LANGUAGES[self.lang]['messages']['name_required'])
            return
            
        try:
            if self.doctor_id.text():  # Update existing
                doctor_data['id'] = int(self.doctor_id.text())
                self.db.update_doctor_data(doctor_data)
                action = "updated" if self.lang == 'en' else "обновлен"
                QMessageBox.information(self, "Success", LANGUAGES[self.lang]['messages']['save_success'].format(action=action))
            else:  # Create new
                self.db.add_doctor(doctor_data)
                action = "added" if self.lang == 'en' else "добавлен"
                QMessageBox.information(self, "Success", LANGUAGES[self.lang]['messages']['save_success'].format(action=action))
                
            self.clear_form()
            self.load_doctors()
        except Exception as e:
            QMessageBox.critical(self, "Error", LANGUAGES[self.lang]['messages']['save_error'].format(error=str(e)))
        
    def clear_form(self):
        self.doctor_id.clear()
        self.doctor_name.clear()
        self.doctor_email.clear()
        self.doctor_phone.clear()
        self.doctor_specialization.setCurrentIndex(0)
        self.doctor_department.setCurrentIndex(0)
        self.doctor_status.setCurrentIndex(0)