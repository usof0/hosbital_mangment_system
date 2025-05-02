from .needs import *

class WritePrescriptionPage(QWidget):
    def __init__(self, user_data, db):
        super().__init__()
        self.user_data = user_data
        self.db = db
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        title = QLabel("Write New Prescription")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 15px;")
        layout.addWidget(title)
        
        form = QFormLayout()
        
        # Patient selection
        self.patient_combo = QComboBox()
        patient_ids = {a['patient_id'] for a in self.db.get_doctor_appointments(self.user_data['id'])}
        patients = [self.db.get_patient_by_id(pid) for pid in patient_ids if pid]
        self.patient_combo.addItems([p['name'] for p in patients])
        form.addRow("Patient:", self.patient_combo)
        
        # Medication details
        self.medication_input = QLineEdit()
        self.dosage_input = QLineEdit()
        self.instructions_input = QTextEdit()
        self.instructions_input.setMaximumHeight(100)
        
        form.addRow("Medication:", self.medication_input)
        form.addRow("Dosage:", self.dosage_input)
        form.addRow("Instructions:", self.instructions_input)
        
        layout.addLayout(form)
        
        # Submit button
        submit_btn = QPushButton("Submit Prescription")
        submit_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px;")
        submit_btn.clicked.connect(self.submit_prescription)
        layout.addWidget(submit_btn, alignment=Qt.AlignRight)
        
    def submit_prescription(self):
        patient_name = self.patient_combo.currentText()
        patient = next(
            (p for p in self.db.data['users']['patients'] 
             if p['name'] == patient_name),
            None
        )
        
        if not patient:
            QMessageBox.warning(self, "Error", "Please select a valid patient")
            return
            
        if not all([self.medication_input.text(), self.dosage_input.text()]):
            QMessageBox.warning(self, "Error", "Please fill in all required fields")
            return
            
        prescription = {
            'id': len(self.db.data['prescriptions']) + 1,
            'patient_id': patient['id'],
            'doctor_id': self.user_data['id'],
            'date': datetime.now().strftime('%Y-%m-%d'),
            'medication': self.medication_input.text(),
            'dosage': self.dosage_input.text(),
            'instructions': self.instructions_input.toPlainText(),
            'status': 'active'
        }
        
        self.db.data['prescriptions'].append(prescription)
        self.db._save_data(self.db.data)
        
        QMessageBox.information(self, "Success", "Prescription submitted successfully!")
        self.medication_input.clear()
        self.dosage_input.clear()
        self.instructions_input.clear()