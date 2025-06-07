from .needs import *

LANGUAGES = {
    'en': {
        'page_title': 'My Appointments',
        'refresh_btn': 'Refresh',
        'table_headers': ["Date", "Time", "Doctor", "Department", "Reason", "Status"],
        'actions_header': "Actions",
        'cancel_btn': 'Cancel',
        'cancel_confirm_title': 'Confirm Cancellation',
        'cancel_confirm_msg': 'Are you sure you want to cancel this appointment?',
        'cancel_success': 'Appointment cancelled successfully',
        'cancel_error': 'Failed to cancel appointment: {}',
        'unknown_doctor': 'Unknown',
        'unknown_department': 'Unknown',
        'status_confirmed': 'Confirmed',
        'status_scheduled': 'Scheduled',
        'status_cancelled': 'Cancelled'
    },
    'ru': {
        'page_title': 'Мои записи',
        'refresh_btn': 'Обновить',
        'table_headers': ["Дата", "Время", "Врач", "Отделение", "Причина", "Статус"],
        'actions_header': "Действия",
        'cancel_btn': 'Отменить',
        'cancel_confirm_title': 'Подтверждение отмены',
        'cancel_confirm_msg': 'Вы уверены, что хотите отменить эту запись?',
        'cancel_success': 'Запись успешно отменена',
        'cancel_error': 'Ошибка отмены записи: {}',
        'unknown_doctor': 'Неизвестно',
        'unknown_department': 'Неизвестно',
        'status_confirmed': 'Подтверждено',
        'status_scheduled': 'Запланировано',
        'status_cancelled': 'Отменено'
    }
}

class PatientAppointmentsPage(QWidget):
    def __init__(self, user_data, db, lang='en'):
        super().__init__()
        self.user_data = user_data
        self.db = db
        self.lang = lang
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Header
        header = QHBoxLayout()
        title = QLabel(LANGUAGES[self.lang]['page_title'])
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        
        self.refresh_btn = QPushButton(LANGUAGES[self.lang]['refresh_btn'])
        self.refresh_btn.clicked.connect(self.load_appointments)
        
        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.refresh_btn)
        
        # Appointments table
        self.appointments_table = QTableWidget()
        self.appointments_table.setColumnCount(6)
        self.appointments_table.setHorizontalHeaderLabels(
            LANGUAGES[self.lang]['table_headers']
        )
        self.appointments_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.appointments_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        # Cancel button column
        self.appointments_table.setColumnCount(7)
        self.appointments_table.setHorizontalHeaderItem(6, QTableWidgetItem(LANGUAGES[self.lang]['actions_header']))
        
        layout.addLayout(header)
        layout.addWidget(self.appointments_table)
        
        self.load_appointments()
        
    def load_appointments(self):
        appointments = self.db.get_patient_appointments(self.user_data['id'])
        self.appointments_table.setRowCount(len(appointments))
        
        for row_idx, appt in enumerate(appointments):
            doctor = self.db.get_doctor_by_id(appt['doctor_id'])

            # Convert date to string if it's a date object
            date_str = appt['date'].strftime("%Y-%m-%d") if hasattr(appt['date'], 'strftime') else str(appt['date'])
            # Convert time to string if needed
            time_str = appt['time'].strftime("%H:%M") if hasattr(appt['time'], 'strftime') else str(appt['time'])

            # Create table items
            items = [
                QTableWidgetItem(date_str),
                QTableWidgetItem(time_str),
                QTableWidgetItem(doctor['name'] if doctor else LANGUAGES[self.lang]['unknown_doctor']),
                QTableWidgetItem(doctor['department'] if doctor else LANGUAGES[self.lang]['unknown_department']),
                QTableWidgetItem(appt.get('reason', '')),
                QTableWidgetItem(self.translate_status(appt['status']))
            ]
            
            # Status styling
            if appt['status'] == 'confirmed':
                items[-1].setForeground(Qt.darkGreen)
            elif appt['status'] == 'scheduled':
                items[-1].setForeground(Qt.darkYellow)
            elif appt['status'] == 'cancelled':
                items[-1].setForeground(Qt.red)
            
            # Add items to table
            for col_idx, item in enumerate(items):
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.appointments_table.setItem(row_idx, col_idx, item)
            
            # Add cancel button if appointment can be cancelled
            if appt['status'] == 'scheduled':
                cancel_btn = QPushButton(LANGUAGES[self.lang]['cancel_btn'])
                cancel_btn.setStyleSheet("background-color: #ef4444; color: white;")
                cancel_btn.clicked.connect(lambda _, a=appt: self.cancel_appointment(a['id']))
                self.appointments_table.setCellWidget(row_idx, 6, cancel_btn)
            else:
                cancel_btn = QPushButton(LANGUAGES[self.lang]['cancel_btn'])
                cancel_btn.setEnabled(False)
                cancel_btn.setStyleSheet("background-color: #efffff; color: white;")
                self.appointments_table.setCellWidget(row_idx, 6, cancel_btn)
        
    def translate_status(self, status):
        """Translate status to current language"""
        status_map = {
            'confirmed': LANGUAGES[self.lang]['status_confirmed'],
            'scheduled': LANGUAGES[self.lang]['status_scheduled'],
            'cancelled': LANGUAGES[self.lang]['status_cancelled']
        }
        return status_map.get(status, status.capitalize())
        
    def cancel_appointment(self, appointment_id):
        reply = QMessageBox.question(
            self, 
            LANGUAGES[self.lang]['cancel_confirm_title'],
            LANGUAGES[self.lang]['cancel_confirm_msg'],
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.db.update_appointment_status(appointment_id, 'cancelled')
                QMessageBox.information(
                    self, 
                    LANGUAGES[self.lang]['cancel_confirm_title'],  # Reuse title as success title
                    LANGUAGES[self.lang]['cancel_success']
                )
                self.load_appointments()
            except Exception as e:
                QMessageBox.critical(
                    self, 
                    LANGUAGES[self.lang]['cancel_confirm_title'],  # Reuse title as error title
                    LANGUAGES[self.lang]['cancel_error'].format(str(e))
                )