from .needs import *

LANGUAGES = {
    'en': {
        'page_title': 'Write New Prescription',
        'form_labels': {
            'patient': 'Patient',
            'medication': 'Medication',
            'dosage': 'Dosage',
            'notes': 'Notes'
        },
        'submit_button': 'Submit Prescription',
        'status': 'active',
        'messages': {
            'success_title': 'Success',
            'success_text': 'Prescription submitted successfully!',
            'error_title': 'Error',
            'invalid_patient': 'Please select a valid patient',
            'missing_fields': 'Please fill in all required fields'
        }
    },
    'ru': {
        'page_title': 'Выписать рецепт',
        'form_labels': {
            'patient': 'Пациент',
            'medication': 'Лекарство',
            'dosage': 'Дозировка',
            'notes': 'Примечания'
        },
        'submit_button': 'Отправить рецепт',
        'status': 'активный',
        'messages': {
            'success_title': 'Успех',
            'success_text': 'Рецепт успешно отправлен!',
            'error_title': 'Ошибка',
            'invalid_patient': 'Пожалуйста, выберите пациента',
            'missing_fields': 'Пожалуйста, заполните все обязательные поля'
        }
    }
}

class WritePrescriptionPage(QWidget):
    def __init__(self, user_data, db, lang='en'):
        super().__init__()
        self.user_data = user_data
        self.db = db
        self.lang = lang
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Page title
        title = QLabel(LANGUAGES[self.lang]['page_title'])
        title.setStyleSheet("""
            font-size: 20px; 
            font-weight: bold; 
            margin-bottom: 15px;
        """)
        layout.addWidget(title)
        
        # Prescription form
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)
        form.setSpacing(10)
        
        # Patient selection
        self.patient_combo = QComboBox()
        patient_ids = {a['patient_id'] for a in self.db.get_doctor_appointments(self.user_data['id'])}
        patients = [self.db.get_patient_by_id(pid) for pid in patient_ids if pid]
        self.patient_combo.addItems([p['name'] for p in patients])
        
        # Medication fields
        self.medication_input = QLineEdit()
        self.dosage_input = QLineEdit()
        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(100)
        
        # Add form rows with translated labels
        labels = LANGUAGES[self.lang]['form_labels']
        form.addRow(f"{labels['patient']}:", self.patient_combo)
        form.addRow(f"{labels['medication']}:", self.medication_input)
        form.addRow(f"{labels['dosage']}:", self.dosage_input)
        form.addRow(f"{labels['notes']}:", self.notes_input)
        
        layout.addLayout(form)
        
        # Submit button
        submit_btn = QPushButton(LANGUAGES[self.lang]['submit_button'])
        submit_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        submit_btn.clicked.connect(self.submit_prescription)
        layout.addWidget(submit_btn, alignment=Qt.AlignRight)
        
    def submit_prescription(self):
        patient_name = self.patient_combo.currentText()
        patients = self.db.get_all_patients()
        patient = next(
            (p for p in patients 
             if p['name'] == patient_name),
            None
        )
        
        messages = LANGUAGES[self.lang]['messages']
        
        if not patient:
            QMessageBox.warning(
                self, 
                messages['error_title'],
                messages['invalid_patient']
            )
            return
            
        if not all([self.medication_input.text(), self.dosage_input.text()]):
            QMessageBox.warning(
                self,
                messages['error_title'],
                messages['missing_fields']
            )
            return
            
        prescription = {
            'patient_id': patient['id'],
            'doctor_id': self.user_data['id'],
            'date': datetime.now().strftime('%Y-%m-%d'),
            'medication': self.medication_input.text(),
            'dosage': self.dosage_input.text(),
            'notes': self.notes_input.toPlainText(),
            'status': LANGUAGES[self.lang]['status']
        }
        
        try:
            self.db.add_prescription(prescription)
            QMessageBox.information(
                self,
                messages['success_title'],
                messages['success_text']
            )
            self.clear_form()
        except Exception as e:
            QMessageBox.critical(
                self,
                messages['error_title'],
                f"{messages['error_title']}: {str(e)}"
            )
    
    def clear_form(self):
        self.medication_input.clear()
        self.dosage_input.clear()
        self.notes_input.clear()
