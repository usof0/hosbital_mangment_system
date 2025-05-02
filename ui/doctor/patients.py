from .needs import *

class MyPatientsPage(QWidget):
    def __init__(self, user_data, db):
        super().__init__()
        self.user_data = user_data
        self.db = db
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        title = QLabel("My Patients")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 15px;")
        layout.addWidget(title)
        
        # Patient table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Name", "Last Visit", "Condition", "Actions"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(self.table)
        self.load_patients()
        
    def load_patients(self):
        patient_ids = {a['patient_id'] for a in self.db.get_doctor_appointments(self.user_data['id'])}
        patients = [self.db.get_patient_by_id(pid) for pid in patient_ids if pid]
        
        self.table.setRowCount(len(patients))
        
        for row, patient in enumerate(patients):
            self.table.setItem(row, 0, QTableWidgetItem(patient['name']))
            
            # Get last appointment date
            last_appt = max(
                (a['date'] for a in self.db.get_patient_appointments(patient['id'])
                if a['doctor_id'] == self.user_data['id']),
                default="Never"
            )
            self.table.setItem(row, 1, QTableWidgetItem(last_appt))
            
            # Get most recent condition (simplified)
            records = self.db.get_patient_medical_records(patient['id'])
            condition = records[-1]['diagnosis'] if records else "No records"
            self.table.setItem(row, 2, QTableWidgetItem(condition))
            
            # View button
            btn = QPushButton("View")
            btn.clicked.connect(lambda _, p=patient: self.view_patient(p))
            self.table.setCellWidget(row, 3, btn)
    
    def view_patient(self, patient):
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Patient: {patient['name']}")
        dialog.setFixedSize(400, 300)
        
        layout = QVBoxLayout(dialog)
        
        info = QLabel(f"""
        <b>Name:</b> {patient['name']}<br>
        <b>DOB:</b> {patient.get('date_of_birth', 'Unknown')}<br>
        <b>Blood Type:</b> {patient.get('blood_type', 'Unknown')}<br>
        <b>Last Visit:</b> {patient.get('last_visit', 'Never')}
        """)
        info.setTextFormat(Qt.RichText)
        
        layout.addWidget(info)
        dialog.exec_()