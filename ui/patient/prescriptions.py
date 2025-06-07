
from .needs import *

LANGUAGES = {
    'en': {
        'page_title': 'My Prescriptions',
        'refresh_btn': 'Refresh',
        'table_headers': ["Date", "Medication", "Dosage", "Doctor", "Status"],
        'refill_btn': 'Request Refill',
        'error_title': 'Error',
        'prescription_not_found': 'Prescription not found',
        'refill_confirm_title': 'Confirm Refill Request',
        'refill_confirm_msg': 'Request refill for:\n\nMedication: {}\nDosage: {}\n\nThis request will be sent to your doctor for approval.',
        'refill_success': 'Refill request submitted. You\'ll be notified when approved.',
        'refill_error': 'Failed to request refill: {}',
        'unknown_doctor': 'Unknown',
        'status_active': 'Active',
        'status_expired': 'Expired'
    },
    'ru': {
        'page_title': 'Мои рецепты',
        'refresh_btn': 'Обновить',
        'table_headers': ["Дата", "Лекарство", "Дозировка", "Врач", "Статус"],
        'refill_btn': 'Запросить повторный',
        'error_title': 'Ошибка',
        'prescription_not_found': 'Рецепт не найден',
        'refill_confirm_title': 'Подтверждение запроса',
        'refill_confirm_msg': 'Запросить повторный рецепт:\n\nЛекарство: {}\nДозировка: {}\n\nЗапрос будет отправлен вашему врачу на подтверждение.',
        'refill_success': 'Запрос на повторный рецепт отправлен. Вы получите уведомление при подтверждении.',
        'refill_error': 'Ошибка запроса повторного рецепта: {}',
        'unknown_doctor': 'Неизвестно',
        'status_active': 'Активен',
        'status_expired': 'Просрочен'
    }
}

class PatientPrescriptionsPage(QWidget):
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
        self.refresh_btn.clicked.connect(self.load_prescriptions)
        
        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.refresh_btn)
        
        # Prescriptions table
        self.prescriptions_table = QTableWidget()
        self.prescriptions_table.setColumnCount(5)
        self.prescriptions_table.setHorizontalHeaderLabels(
            LANGUAGES[self.lang]['table_headers']
        )
        self.prescriptions_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.prescriptions_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        layout.addLayout(header)
        layout.addWidget(self.prescriptions_table)
        
        self.load_prescriptions()
        
    def load_prescriptions(self):
        prescriptions = self.db.get_patient_prescriptions(self.user_data['id'])
        self.prescriptions_table.setRowCount(len(prescriptions))
        
        for row_idx, presc in enumerate(prescriptions):
            doctor = self.db.get_doctor_by_id(presc['doctor_id'])
            
            # Convert date to string if it's a date object
            date_str = presc['date'].strftime("%Y-%m-%d") if hasattr(presc['date'], 'strftime') else str(presc['date'])

            # Create table items
            items = [
                QTableWidgetItem(date_str),
                QTableWidgetItem(presc['medication']),
                QTableWidgetItem(presc['dosage']),
                QTableWidgetItem(doctor['name'] if doctor else LANGUAGES[self.lang]['unknown_doctor']),
                QTableWidgetItem(self.translate_status(presc['status']))
            ]
            
            # Status styling
            if presc['status'] == 'active':
                items[-1].setForeground(Qt.darkGreen)
            elif presc['status'] == 'expired':
                items[-1].setForeground(Qt.darkRed)
            
            # Add items to table
            for col_idx, item in enumerate(items):
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.prescriptions_table.setItem(row_idx, col_idx, item)
            
            # Add refill button if prescription is active
            if presc['status'] == 'active':
                refill_btn = QPushButton(LANGUAGES[self.lang]['refill_btn'])
                refill_btn.setStyleSheet("color: #3b82f6;")
                refill_btn.clicked.connect(lambda _, p=presc: self.request_refill(p['id']))
                self.prescriptions_table.setCellWidget(row_idx, 5, refill_btn)
    
    def translate_status(self, status):
        """Translate status to current language"""
        status_map = {
            'active': LANGUAGES[self.lang]['status_active'],
            'expired': LANGUAGES[self.lang]['status_expired']
        }
        return status_map.get(status, status.capitalize())
        
    def request_refill(self, prescription_id):
        prescription = next((p for p in self.db.get_patient_prescriptions(self.user_data['id']) 
                           if p['id'] == prescription_id), None)
        
        if not prescription:
            QMessageBox.warning(
                self, 
                LANGUAGES[self.lang]['error_title'], 
                LANGUAGES[self.lang]['prescription_not_found']
            )
            return
            
        reply = QMessageBox.question(
            self, 
            LANGUAGES[self.lang]['refill_confirm_title'],
            LANGUAGES[self.lang]['refill_confirm_msg'].format(
                prescription['medication'],
                prescription['dosage']
            ),
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.db.update_prescription(prescription_id, {'refill_requested': True})
                QMessageBox.information(
                    self, 
                    LANGUAGES[self.lang]['refill_confirm_title'],  # Reuse title
                    LANGUAGES[self.lang]['refill_success']
                )
                self.load_prescriptions()
            except Exception as e:
                QMessageBox.critical(
                    self, 
                    LANGUAGES[self.lang]['error_title'], 
                    LANGUAGES[self.lang]['refill_error'].format(str(e))
                )