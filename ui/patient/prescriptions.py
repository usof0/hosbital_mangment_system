from .needs import *

class PatientPrescriptionsPage(QWidget):
    def __init__(self, user_data, db):
        super().__init__()
        self.user_data = user_data
        self.db = db
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Header
        header = QHBoxLayout()
        title = QLabel("My Prescriptions")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.load_prescriptions)
        
        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.refresh_btn)
        
        # Prescriptions table
        self.prescriptions_table = QTableWidget()
        self.prescriptions_table.setColumnCount(6)
        self.prescriptions_table.setHorizontalHeaderLabels(
            ["Date", "Medication", "Dosage", "Doctor", "Status", "Actions"]
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
            
            # Create table items
            items = [
                QTableWidgetItem(presc['date']),
                QTableWidgetItem(presc['medication']),
                QTableWidgetItem(presc['dosage']),
                QTableWidgetItem(doctor['name'] if doctor else "Unknown"),
                QTableWidgetItem(presc['status'].capitalize())
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
                refill_btn = QPushButton("Request Refill")
                refill_btn.setStyleSheet("color: #3b82f6;")
                refill_btn.clicked.connect(lambda _, p=presc: self.request_refill(p['id']))
                self.prescriptions_table.setCellWidget(row_idx, 5, refill_btn)
        
        # self.prescriptions_table.resizeColumnsToContents()
        
    def request_refill(self, prescription_id):
        prescription = next((p for p in self.db.get_patient_prescriptions(self.user_data['id']) 
                           if p['id'] == prescription_id), None)
        
        if not prescription:
            QMessageBox.warning(self, "Error", "Prescription not found")
            return
            
        reply = QMessageBox.question(
            self, 'Confirm Refill Request',
            f"Request refill for:\n\n"
            f"Medication: {prescription['medication']}\n"
            f"Dosage: {prescription['dosage']}\n\n"
            f"This request will be sent to your doctor for approval.",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.db.update_prescription(prescription_id, {'refill_requested': True})
                QMessageBox.information(
                    self, "Success", 
                    "Refill request submitted. You'll be notified when approved."
                )
                self.load_prescriptions()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to request refill: {str(e)}")
