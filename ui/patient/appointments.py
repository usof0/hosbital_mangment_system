from .needs import *

class PatientAppointmentsPage(QWidget):
    def __init__(self, user_data, db):
        super().__init__()
        self.user_data = user_data
        self.db = db
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Header
        header = QHBoxLayout()
        title = QLabel("My Appointments")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.load_appointments)
        
        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.refresh_btn)
        
        # Appointments table
        self.appointments_table = QTableWidget()
        self.appointments_table.setColumnCount(6)
        self.appointments_table.setHorizontalHeaderLabels(
            ["Date", "Time", "Doctor", "Department", "Reason", "Status"]
        )
        self.appointments_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.appointments_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        # Cancel button column
        self.appointments_table.setColumnCount(7)
        self.appointments_table.setHorizontalHeaderItem(6, QTableWidgetItem("Actions"))
        
        layout.addLayout(header)
        layout.addWidget(self.appointments_table)
        
        self.load_appointments()
        
    def load_appointments(self):
        appointments = self.db.get_patient_appointments(self.user_data['id'])
        self.appointments_table.setRowCount(len(appointments))
        
        for row_idx, appt in enumerate(appointments):
            doctor = self.db.get_doctor_by_id(appt['doctor_id'])

            # Create table items
            items = [
                QTableWidgetItem(appt['date']),
                QTableWidgetItem(appt['time']),
                QTableWidgetItem(doctor['name'] if doctor else "Unknown"),
                QTableWidgetItem(doctor['department'] if doctor else "Unknown"),
                QTableWidgetItem(appt.get('reason', '')),
                QTableWidgetItem(appt['status'].capitalize())
            ]
            
            # Status styling
            if appt['status'] == 'confirmed':
                items[-1].setForeground(Qt.darkGreen)
            elif appt['status'] == 'pending':
                items[-1].setForeground(Qt.darkYellow)
            elif appt['status'] == 'cancelled':
                items[-1].setForeground(Qt.red)
            
            # Add items to table
            for col_idx, item in enumerate(items):
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.appointments_table.setItem(row_idx, col_idx, item)
            
            # Add cancel button if appointment can be cancelled
            if appt['status'] in ['pending', 'confirmed']:
                cancel_btn = QPushButton("Cancel")
                cancel_btn.setStyleSheet("background-color: #ef4444; color: white;")
                cancel_btn.clicked.connect(lambda _, a=appt: self.cancel_appointment(a['id']))
                self.appointments_table.setCellWidget(row_idx, 6, cancel_btn)
            else:
                cancel_btn = cancel_btn = QPushButton("Cancel")
                cancel_btn.setEnabled(False)
                cancel_btn.setStyleSheet("background-color: #efffff; color: white;")
                self.appointments_table.setCellWidget(row_idx, 6, cancel_btn)
        
        # self.appointments_table.resizeColumnsToContents()
        
    def cancel_appointment(self, appointment_id):
        reply = QMessageBox.question(
            self, 'Confirm Cancellation',
            "Are you sure you want to cancel this appointment?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.db.update_appointment_status(appointment_id, 'cancelled')
                QMessageBox.information(self, "Success", "Appointment cancelled successfully")
                self.load_appointments()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to cancel appointment: {str(e)}")
    
    # def add_appointment():