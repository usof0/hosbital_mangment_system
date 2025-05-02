from .needs import *

class DoctorSchedulePage(QWidget):
    def __init__(self, user_data, db):
        super().__init__()
        self.user_data = user_data
        self.db = db
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        title = QLabel("My Schedule")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 15px;")
        layout.addWidget(title)
        
        # Date selector
        date_layout = QHBoxLayout()
        date_layout.addWidget(QLabel("Select Date:"))
        self.date_edit = QDateEdit(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        date_layout.addWidget(self.date_edit)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.load_appointments)
        date_layout.addWidget(refresh_btn)
        
        layout.addLayout(date_layout)
        
        # Appointments table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Time", "Patient", "Reason", "Status"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(self.table)
        self.load_appointments()
        
    def load_appointments(self):
        date = self.date_edit.date().toString("yyyy-MM-dd")
        appointments = [a for a in self.db.get_doctor_appointments(self.user_data['id']) 
                      if a['date'] == date]
        
        self.table.setRowCount(len(appointments))
        
        for row, appt in enumerate(appointments):
            patient = self.db.get_patient_by_id(appt['patient_id'])
            
            self.table.setItem(row, 0, QTableWidgetItem(appt['time']))
            self.table.setItem(row, 1, QTableWidgetItem(patient['name'] if patient else "Unknown"))
            self.table.setItem(row, 2, QTableWidgetItem(appt.get('reason', '')))
            
            status = QTableWidgetItem(appt['status'].capitalize())
            if appt['status'] == 'completed':
                status.setForeground(Qt.darkGreen)
            elif appt['status'] == 'cancelled':
                status.setForeground(Qt.red)
            self.table.setItem(row, 3, status)
