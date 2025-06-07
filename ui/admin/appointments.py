from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QGroupBox, QLineEdit, QDateEdit, QTableWidget, QTableWidgetItem,
    QHeaderView, QFormLayout, QComboBox, QTextEdit, QTimeEdit, 
    QMessageBox, QInputDialog
)
from PyQt5.QtCore import Qt, QDate, QTime

LANGUAGES = {
    'en': {
        'page_title': 'Manage Appointments',
        'refresh_button': 'Refresh',
        'search_filters': 'Search Filters',
        'patient': 'Patient',
        'doctor': 'Doctor',
        'patient_name': 'Patient name',
        'doctor_name': 'Doctor name',
        'date': 'Date',
        'search_button': 'Search',
        'clear_button': 'Clear',
        'table_headers': ["ID", "Patient", "Doctor", "Date", "Time", "Reason", "Status", "Actions"],
        'add_edit_group': 'Add/Edit Appointment',
        'appointment_id': 'Appointment ID',
        'auto_generated': 'Auto-generated',
        'select_patient': 'Select Patient',
        'select_doctor': 'Select Doctor',
        'time': 'Time',
        'reason': 'Reason',
        'status': 'Status',
        'status_options': ["scheduled", "completed", "cancelled", "no-show"],
        'save_button': 'Save',
        'edit_button': 'Edit',
        'cancel_button': 'Cancel',
        'restore_button': 'Restore',
        'confirm_title': 'Confirm',
        'confirm_cancel': 'Are you sure you want to cancel this appointment?',
        'confirm_restore': 'Are you sure you want to restore this appointment?',
        'success_title': 'Success',
        'appointment_cancelled': 'Appointment cancelled successfully',
        'appointment_restored': 'Appointment restored successfully',
        'appointment_updated': 'Appointment updated successfully',
        'appointment_added': 'Appointment added successfully',
        'error_title': 'Error',
        'required_fields': 'Patient and doctor are required',
        'update_error': 'Failed to update appointment: {error}',
        'save_error': 'Failed to save appointment: {error}'
    },
    'ru': {
        'page_title': 'Управление записями',
        'refresh_button': 'Обновить',
        'search_filters': 'Фильтры поиска',
        'patient': 'Пациент',
        'doctor': 'Врач',
        'patient_name': 'Имя пациента',
        'doctor_name': 'Имя врача',
        'date': 'Дата',
        'search_button': 'Поиск',
        'clear_button': 'Очистить',
        'table_headers': ["ID", "Пациент", "Врач", "Дата", "Время", "Причина", "Статус", "Действия"],
        'add_edit_group': 'Добавить/Редактировать запись',
        'appointment_id': 'ID записи',
        'auto_generated': 'Автоматически',
        'select_patient': 'Выберите пациента',
        'select_doctor': 'Выберите врача',
        'time': 'Время',
        'reason': 'Причина',
        'status': 'Статус',
        'status_options': ["запланировано", "завершено", "отменено", "не явился"],
        'save_button': 'Сохранить',
        'edit_button': 'Редактировать',
        'cancel_button': 'Отменить',
        'restore_button': 'Восстановить',
        'confirm_title': 'Подтверждение',
        'confirm_cancel': 'Вы уверены, что хотите отменить эту запись?',
        'confirm_restore': 'Вы уверены, что хотите восстановить эту запись?',
        'success_title': 'Успех',
        'appointment_cancelled': 'Запись успешно отменена',
        'appointment_restored': 'Запись успешно восстановлена',
        'appointment_updated': 'Запись успешно обновлена',
        'appointment_added': 'Запись успешно добавлена',
        'error_title': 'Ошибка',
        'required_fields': 'Необходимо указать пациента и врача',
        'update_error': 'Ошибка при обновлении записи: {error}',
        'save_error': 'Ошибка при сохранении записи: {error}'
    }
}

class ManageAppointmentsPage(QWidget):
    def __init__(self, user_data, db, lang='en'):
        super().__init__()
        self.user_data = user_data
        self.db = db
        self.lang = lang
        self.init_ui()
        
    def init_ui(self):
        self.setup_main_layout()
        self.setup_header()
        self.setup_search_filters()
        self.setup_appointments_table()
        self.setup_appointment_form()
        self.load_appointments()
        
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
        refresh_btn.clicked.connect(self.load_appointments)
        
        header.addWidget(title)
        header.addStretch()
        header.addWidget(refresh_btn)
        
        self.layout.addLayout(header)
        
    def setup_search_filters(self):
        filter_group = QGroupBox(LANGUAGES[self.lang]['search_filters'])
        filter_layout = QHBoxLayout()
        
        self.search_patient = QLineEdit()
        self.search_patient.setPlaceholderText(LANGUAGES[self.lang]['patient_name'])
        
        self.search_doctor = QLineEdit()
        self.search_doctor.setPlaceholderText(LANGUAGES[self.lang]['doctor_name'])
        
        self.search_date = QDateEdit()
        self.search_date.setDisplayFormat("yyyy-MM-dd")
        self.search_date.setCalendarPopup(True)
        
        search_btn = QPushButton(LANGUAGES[self.lang]['search_button'])
        search_btn.setStyleSheet("""
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
        search_btn.clicked.connect(self.load_appointments)
        
        clear_btn = QPushButton(LANGUAGES[self.lang]['clear_button'])
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
        clear_btn.clicked.connect(self.clear_search_filters)
        
        filter_layout.addWidget(QLabel(LANGUAGES[self.lang]['patient'] + ":"))
        filter_layout.addWidget(self.search_patient)
        filter_layout.addWidget(QLabel(LANGUAGES[self.lang]['doctor'] + ":"))
        filter_layout.addWidget(self.search_doctor)
        filter_layout.addWidget(QLabel(LANGUAGES[self.lang]['date'] + ":"))
        filter_layout.addWidget(self.search_date)
        filter_layout.addWidget(search_btn)
        filter_layout.addWidget(clear_btn)
        
        filter_group.setLayout(filter_layout)
        self.layout.addWidget(filter_group)
        
    def setup_appointments_table(self):
        self.appointments_table = QTableWidget()
        self.appointments_table.setColumnCount(8)
        self.appointments_table.setHorizontalHeaderLabels(
            LANGUAGES[self.lang]['table_headers']
        )
        self.appointments_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.appointments_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.appointments_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        self.layout.addWidget(self.appointments_table)
        
    def setup_appointment_form(self):
        group = QGroupBox(LANGUAGES[self.lang]['add_edit_group'])
        group.setStyleSheet(group.styleSheet())
        
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)
        
        self.appointment_id = QLineEdit()
        self.appointment_id.setPlaceholderText(LANGUAGES[self.lang]['auto_generated'])
        self.appointment_id.setReadOnly(True)
        
        # Get patients and doctors for dropdowns
        patients = self.db.get_all_patients()
        doctors = self.db.get_all_doctors()
        
        self.patient_combo = QComboBox()
        self.patient_combo.addItem(LANGUAGES[self.lang]['select_patient'], None)
        for patient in patients:
            self.patient_combo.addItem(patient['name'], patient['id'])
            
        self.doctor_combo = QComboBox()
        self.doctor_combo.addItem(LANGUAGES[self.lang]['select_doctor'], None)
        for doctor in doctors:
            self.doctor_combo.addItem(doctor['name'], doctor['id'])
        
        self.appointment_date = QDateEdit()
        self.appointment_date.setDisplayFormat("yyyy-MM-dd")
        self.appointment_date.setCalendarPopup(True)
        self.appointment_date.setMinimumDate(QDate.currentDate())
        
        self.appointment_time = QTimeEdit()
        self.appointment_time.setDisplayFormat("hh:mm AP")
        
        self.appointment_reason = QTextEdit()
        self.appointment_reason.setMaximumHeight(80)
        
        self.appointment_status = QComboBox()
        self.appointment_status.addItems(LANGUAGES[self.lang]['status_options'])
        
        # Buttons
        btn_layout = QHBoxLayout()
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
        save_btn.clicked.connect(self.save_appointment)
        
        clear_btn = QPushButton(LANGUAGES[self.lang]['clear_button'])
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
        
        form.addRow(LANGUAGES[self.lang]['appointment_id'] + ":", self.appointment_id)
        form.addRow(LANGUAGES[self.lang]['patient'] + ":", self.patient_combo)
        form.addRow(LANGUAGES[self.lang]['doctor'] + ":", self.doctor_combo)
        form.addRow(LANGUAGES[self.lang]['date'] + ":", self.appointment_date)
        form.addRow(LANGUAGES[self.lang]['time'] + ":", self.appointment_time)
        form.addRow(LANGUAGES[self.lang]['reason'] + ":", self.appointment_reason)
        form.addRow(LANGUAGES[self.lang]['status'] + ":", self.appointment_status)
        form.addRow(btn_layout)
        
        group.setLayout(form)
        self.layout.addWidget(group)
        
    def load_appointments(self):
        filters = {
            'patient_name': self.search_patient.text(),
            'doctor_name': self.search_doctor.text(),
            'date': self.search_date.date().toString("yyyy-MM-dd") if self.search_date.date() else None
        }
        
        appointments = self.db.get_appointments_with_details(filters)
        self.appointments_table.setRowCount(len(appointments))
        
        for row_idx, appt in enumerate(appointments):
            items = [
                QTableWidgetItem(str(appt.get('id', ''))),
                QTableWidgetItem(appt.get('patient_name', '')),
                QTableWidgetItem(appt.get('doctor_name', '')),
                QTableWidgetItem(appt.get('date', '')),
                QTableWidgetItem(appt.get('time', '')),
                QTableWidgetItem(appt.get('reason', '')),
                QTableWidgetItem(appt.get('status', ''))
            ]
            
            # Action buttons
            edit_btn = QPushButton(LANGUAGES[self.lang]['edit_button'])
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
            edit_btn.clicked.connect(lambda _, a=appt: self.edit_appointment(a))
            
            cancel_text = LANGUAGES[self.lang]['cancel_button'] if appt['status'] != 'cancelled' else LANGUAGES[self.lang]['restore_button']
            cancel_btn = QPushButton(cancel_text)
            cancel_btn.setStyleSheet("""
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
            cancel_btn.clicked.connect(lambda _, a=appt: self.toggle_cancel_appointment(a))
            
            btn_widget = QWidget()
            btn_layout = QHBoxLayout(btn_widget)
            btn_layout.addWidget(edit_btn)
            btn_layout.addWidget(cancel_btn)
            btn_layout.setContentsMargins(0, 0, 0, 0)
            
            for col_idx, item in enumerate(items):
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.appointments_table.setItem(row_idx, col_idx, item)
            
            self.appointments_table.setCellWidget(row_idx, 7, btn_widget)
        
        self.appointments_table.resizeColumnsToContents()
        
    def edit_appointment(self, appointment):
        self.appointment_id.setText(str(appointment.get('id', '')))
        
        # Set patient
        index = self.patient_combo.findData(appointment['patient_id'])
        if index >= 0:
            self.patient_combo.setCurrentIndex(index)
            
        # Set doctor
        index = self.doctor_combo.findData(appointment['doctor_id'])
        if index >= 0:
            self.doctor_combo.setCurrentIndex(index)
            
        if 'date' in appointment:
            self.appointment_date.setDate(QDate.fromString(appointment['date'], "yyyy-MM-dd"))
            
        if 'time' in appointment:
            self.appointment_time.setTime(QTime.fromString(appointment['time'], "hh:mm AP"))
            
        self.appointment_reason.setPlainText(appointment.get('reason', ''))
        
        index = self.appointment_status.findText(appointment.get('status', 'scheduled'))
        if index >= 0:
            self.appointment_status.setCurrentIndex(index)
        
    def toggle_cancel_appointment(self, appointment):
        new_status = 'cancelled' if appointment['status'] != 'cancelled' else 'scheduled'
        
        confirm_msg = LANGUAGES[self.lang]['confirm_cancel'] if new_status == 'cancelled' else LANGUAGES[self.lang]['confirm_restore']
        
        reply = QMessageBox.question(
            self, 
            LANGUAGES[self.lang]['confirm_title'],
            confirm_msg,
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.db.update_appointment_status(appointment['id'], new_status)
                success_msg = LANGUAGES[self.lang]['appointment_cancelled'] if new_status == 'cancelled' else LANGUAGES[self.lang]['appointment_restored']
                QMessageBox.information(self, LANGUAGES[self.lang]['success_title'], success_msg)
                self.load_appointments()
            except Exception as e:
                QMessageBox.critical(
                    self, 
                    LANGUAGES[self.lang]['error_title'], 
                    LANGUAGES[self.lang]['update_error'].format(error=str(e))
                )
        
    def save_appointment(self):
        appointment_data = {
            'patient_id': self.patient_combo.currentData(),
            'doctor_id': self.doctor_combo.currentData(),
            'date': self.appointment_date.date().toString("yyyy-MM-dd"),
            'time': self.appointment_time.time().toString("hh:mm AP"),
            'reason': self.appointment_reason.toPlainText(),
            'status': self.appointment_status.currentText()
        }
        
        if not all([appointment_data['patient_id'], appointment_data['doctor_id']]):
            QMessageBox.warning(self, LANGUAGES[self.lang]['error_title'], LANGUAGES[self.lang]['required_fields'])
            return
            
        try:
            if self.appointment_id.text():  # Update existing
                appointment_data['id'] = int(self.appointment_id.text())
                self.db.update_appointment(appointment_data)
                QMessageBox.information(
                    self, 
                    LANGUAGES[self.lang]['success_title'], 
                    LANGUAGES[self.lang]['appointment_updated']
                )
            else:  # Create new
                self.db.add_appointment(appointment_data)
                QMessageBox.information(
                    self, 
                    LANGUAGES[self.lang]['success_title'], 
                    LANGUAGES[self.lang]['appointment_added']
                )
                
            self.clear_form()
            self.load_appointments()
        except Exception as e:
            QMessageBox.critical(
                self, 
                LANGUAGES[self.lang]['error_title'], 
                LANGUAGES[self.lang]['save_error'].format(error=str(e))
            )
        
    def clear_form(self):
        self.appointment_id.clear()
        self.patient_combo.setCurrentIndex(0)
        self.doctor_combo.setCurrentIndex(0)
        self.appointment_date.setDate(QDate.currentDate())
        self.appointment_time.setTime(QTime(9, 0))  # Default to 9:00 AM
        self.appointment_reason.clear()
        self.appointment_status.setCurrentIndex(0)
        
    def clear_search_filters(self):
        self.search_patient.clear()
        self.search_doctor.clear()
        self.search_date.setDate(QDate())
        self.load_appointments()