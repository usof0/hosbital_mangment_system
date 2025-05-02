from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QTableWidget, QTableWidgetItem, QPushButton,
                            QTextEdit, QDateEdit, QTimeEdit, QComboBox,
                            QMessageBox, QHeaderView, QDialog)
from PyQt5.QtCore import Qt, QDate, QTime
from .dashboard import Dashboard
from .patient import BookAppointmentDialog


class PatientDashboard(Dashboard):
    def __init__(self, user_data, db):
        super().__init__("patient", user_data, db)
        # self.init_ui()
        
    def init_ui(self):
        # Clear existing layout if any
        if self.layout():
            QWidget().setLayout(self.layout())

        super().init_ui()
        self.load_data()
        self.setup_ui_components()
        
    def load_data(self):
        """Load all necessary data from database"""
        self.patient_id = self.user_data['id']
        self.appointments = self.db.get_patient_appointments(self.patient_id)
        self.prescriptions = self.db.get_patient_prescriptions(self.patient_id)
        self.medical_records = self.db.get_patient_medical_records(self.patient_id)
        self.bills = self.db.get_patient_bills(self.patient_id)
        self.doctors = self.db.get_all_doctors()
        
    def setup_ui_components(self):
        """Setup all UI components"""
        
        self.setup_stats_cards()
        self.setup_appointments_table()
        self.create_prescriptions_widget()
        self.setup_health_summary()
        
    def setup_stats_cards(self):
        """Create and display stats cards"""
        cards_widget = QWidget()
        cards_layout = QHBoxLayout(cards_widget)
        
        stats = [
            ("Upcoming Appointments", 
             str(len([a for a in self.appointments if a['status'] != 'completed'])), 
             "appointment", "blue"),
            ("Active Prescriptions", 
             str(len([p for p in self.prescriptions if p['status'] == 'active'])), 
             "prescription", "green"),
            ("Medical Records", 
             str(len(self.medical_records)), 
             "file-medical", "purple"),
            ("Pending Bills", 
             f"${sum(b['amount'] for b in self.bills if b['status'] == 'pending'):.2f}", 
             "file-invoice-dollar", "yellow")
        ]
        
        for title, value, icon, color in stats:
            card = self.create_card(title, value, icon, color)
            cards_layout.addWidget(card)
            
        self.layout.addWidget(cards_widget)
        
    def setup_appointments_table(self):
        """Setup appointments table with interactive elements"""
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        
        # Appointments Widget
        appointments_widget = QWidget()
        appointments_widget.setObjectName("card")
        appointments_layout = QVBoxLayout(appointments_widget)
        
        # Header with buttons
        header_widget = QWidget()
        header = QHBoxLayout(header_widget)
        appointments_title = QLabel("Upcoming Appointments")
        appointments_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        self.book_appt_btn = QPushButton("Book Appointment")
        self.book_appt_btn.setStyleSheet("background-color: #10b981; color: white;")
        self.book_appt_btn.clicked.connect(self.show_book_appointment_dialog)
        
        view_all_btn = QPushButton("View All")
        view_all_btn.setStyleSheet("color: #3b82f6; text-decoration: underline;")
        view_all_btn.clicked.connect(lambda: self.parent().switch_page_by_name("appointments"))
        
        header.addWidget(appointments_title)
        header.addWidget(self.book_appt_btn)
        header.addWidget(view_all_btn)
        
        # Table setup
        self.appointments_table = QTableWidget()
        self.appointments_table.setColumnCount(5)
        self.appointments_table.setHorizontalHeaderLabels(["Date", "Time", "Doctor", "Department", "Status"])
        self.appointments_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.appointments_table.verticalHeader().setVisible(False)
        
        self.update_appointments_table()
        
        appointments_layout.addWidget(header_widget)
        appointments_layout.addWidget(self.appointments_table)
        
        # Prescriptions Widget
        prescriptions_widget = self.create_prescriptions_widget()
        
        content_layout.addWidget(appointments_widget, stretch=2)
        content_layout.addWidget(prescriptions_widget, stretch=1)

        self.layout.addWidget(content_widget)
        
    def update_appointments_table(self):
        """Update the appointments table with current data"""
        upcoming_appts = [a for a in self.appointments if a['status'] != 'completed']
        self.appointments_table.setRowCount(len(upcoming_appts))
        
        for row_idx, appt in enumerate(upcoming_appts):
            doctor = self.db.get_doctor_by_id(appt['doctor_id'])
            
            # Create items for each column
            date_item = QTableWidgetItem(appt['date'])
            time_item = QTableWidgetItem(appt['time'])
            doctor_item = QTableWidgetItem(doctor['name'] if doctor else "Unknown")
            dept_item = QTableWidgetItem(doctor['department'] if doctor else "Unknown")
            status_item = QTableWidgetItem(appt['status'].capitalize())
            
            # Status styling
            if appt['status'] == 'confirmed':
                status_item.setForeground(Qt.darkGreen)
            elif appt['status'] == 'pending':
                status_item.setForeground(Qt.darkYellow)
            elif appt['status'] == 'cancelled':
                status_item.setForeground(Qt.red)
            
            # Add items to table
            self.appointments_table.setItem(row_idx, 0, date_item)
            self.appointments_table.setItem(row_idx, 1, time_item)
            self.appointments_table.setItem(row_idx, 2, doctor_item)
            self.appointments_table.setItem(row_idx, 3, dept_item)
            self.appointments_table.setItem(row_idx, 4, status_item)
            
        self.appointments_table.resizeColumnsToContents()
        
    def create_prescriptions_widget(self):
        """Create the prescriptions widget"""
        prescriptions_widget = QWidget()
        prescriptions_widget.setObjectName("card")
        prescriptions_layout = QVBoxLayout(prescriptions_widget)
        
        prescriptions_title = QLabel("Recent Prescriptions")
        prescriptions_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        # Get active prescriptions (sorted by date, newest first)
        active_prescriptions = sorted(
            [p for p in self.prescriptions if p['status'] == 'active'],
            key=lambda x: x['date'],
            reverse=True
        )[:3]  # Show only 3 most recent
        
        for presc in active_prescriptions:
            doctor = self.db.get_doctor_by_id(presc['doctor_id'])
            color = "blue" if presc['status'] == 'active' else "green"
            
            prescription = QWidget()
            prescription.setStyleSheet(f"""
                border-left: 4px solid {color};
                padding-left: 8px;
                margin-bottom: 8px;
            """)
            
            pres_layout = QVBoxLayout(prescription)
            
            # Header with medication and status
            header_widget = QWidget()
            header = QHBoxLayout(header_widget)
            name = QLabel(presc['medication'])
            name.setStyleSheet("font-weight: bold;")
            
            status_label = QLabel(presc['status'].capitalize())
            status_label.setStyleSheet(f"""
                background-color: {color}100;
                color: {color}800;
                padding: 2px 4px;
                border-radius: 4px;
                font-size: 12px;
            """)
            
            header.addWidget(name)
            header.addWidget(status_label)
            
            # Details
            details = QLabel(f"Prescribed by Dr. {doctor['name']} on {presc['date']}" if doctor else presc['date'])
            details.setStyleSheet("color: #6b7280; font-size: 12px;")
            
            # Dosage and instructions
            dosage = QLabel(f"<b>Dosage:</b> {presc['dosage']}")
            dosage.setTextFormat(Qt.RichText)
            
            instructions = QLabel(f"<b>Instructions:</b> {presc.get('instructions', 'None')}")
            instructions.setTextFormat(Qt.RichText)
            instructions.setWordWrap(True)
            
            # Refill button
            refill_btn = QPushButton("Request Refill")
            refill_btn.setStyleSheet("""
                color: #3b82f6;
                text-decoration: underline;
                border: none;
                text-align: left;
                padding: 0;
            """)
            refill_btn.clicked.connect(lambda _, p=presc: self.request_prescription_refill(p['id']))
            
            pres_layout.addWidget(header_widget)
            pres_layout.addWidget(details)
            pres_layout.addWidget(dosage)
            pres_layout.addWidget(instructions)
            pres_layout.addWidget(refill_btn)
            
            prescriptions_layout.addWidget(prescription)
            
        view_all_btn = QPushButton("View All Prescriptions")
        view_all_btn.setStyleSheet("color: #3b82f6; text-decoration: underline;")
        view_all_btn.clicked.connect(lambda: self.parent().switch_page_by_name("prescriptions"))
        
        prescriptions_layout.addWidget(prescriptions_title)
        prescriptions_layout.addSpacing(10)
        prescriptions_layout.addWidget(view_all_btn, alignment=Qt.AlignRight)
        
        return prescriptions_widget
        
    def setup_health_summary(self):
        """Setup health summary section"""
        health_widget = QWidget()
        health_widget.setObjectName("chart-container")
        health_layout = QVBoxLayout(health_widget)
        
        health_title = QLabel("Health Summary")
        health_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        # Add actual health summary (simplified for example)
        summary_text = QTextEdit()
        summary_text.setReadOnly(True)
        
        # Generate summary from medical records
        if self.medical_records:
            summary_html = "<h3>Recent Medical History</h3><ul>"
            for record in sorted(self.medical_records, 
                               key=lambda x: x['date'], 
                               reverse=True)[:3]:  # Show 3 most recent
                doctor = self.db.get_doctor_by_id(record['doctor_id'])
                summary_html += f"""
                <li>
                    <b>{record['date']}</b> - {doctor['name'] if doctor else 'Unknown'}<br>
                    <b>Diagnosis:</b> {record['diagnosis']}<br>
                    <b>Treatment:</b> {record['treatment']}
                </li>
                """
            summary_html += "</ul>"
        else:
            summary_html = "<p>No medical records found</p>"
            
        # Add vital statistics (simulated)
        summary_html += """
        <h3>Vital Statistics</h3>
        <table border='0' cellspacing='10'>
            <tr><td><b>Blood Pressure:</b></td><td>120/80 mmHg</td></tr>
            <tr><td><b>Heart Rate:</b></td><td>72 bpm</td></tr>
            <tr><td><b>Blood Type:</b></td><td>{blood_type}</td></tr>
            <tr><td><b>Last Checkup:</b></td><td>{last_checkup}</td></tr>
        </table>
        """.format(
            blood_type=self.user_data.get('blood_type', 'Unknown'),
            last_checkup=max([r['date'] for r in self.medical_records], default="Never")
        )
        
        summary_text.setHtml(summary_html)
        
        view_records_btn = QPushButton("View Full Medical Records")
        view_records_btn.setStyleSheet("color: #3b82f6; text-decoration: underline;")
        view_records_btn.clicked.connect(lambda: self.parent().switch_page_by_name("medical-records"))
        
        health_layout.addWidget(health_title)
        health_layout.addWidget(summary_text)
        health_layout.addWidget(view_records_btn, alignment=Qt.AlignRight)
        
        self.layout.addWidget(health_widget)
        
    def show_book_appointment_dialog(self):
        """Show dialog to book new appointment"""
        dialog = BookAppointmentDialog(self.user_data, self.db)
        if dialog.exec_() == QDialog.Accepted:
            self.load_data()
            self.update_appointments_table()
            dialog.close()
    #     dialog = QDialog()
    #     dialog.setWindowTitle("Book New Appointment")
    #     dialog.setFixedSize(500, 400)
        
    #     layout = QVBoxLayout(dialog)
        
    #     # Doctor selection
    #     doctor_label = QLabel("Doctor:")
    #     self.doctor_combo = QComboBox()
    #     self.doctor_combo.addItems([f"{d['name']} ({d['specialization']})" for d in self.doctors])
        
    #     # Date and time
    #     date_label = QLabel("Date:")
    #     self.appt_date = QDateEdit()
    #     self.appt_date.setDate(QDate.currentDate())
    #     self.appt_date.setMinimumDate(QDate.currentDate())
        
    #     time_label = QLabel("Time:")
    #     self.appt_time = QTimeEdit()
    #     self.appt_time.setTime(QTime(9, 0))
    #     self.appt_time.setDisplayFormat("hh:mm AP")
        
    #     # Reason
    #     reason_label = QLabel("Reason:")
    #     self.appt_reason = QTextEdit()
    #     self.appt_reason.setPlaceholderText("Describe the reason for your appointment...")
    #     self.appt_reason.setMaximumHeight(100)
        
    #     # Buttons
    #     button_layout = QHBoxLayout()
    #     book_btn = QPushButton("Book Appointment")
    #     book_btn.setStyleSheet("background-color: #10b981; color: white;")
    #     book_btn.clicked.connect(self.book_appointment)
        
    #     cancel_btn = QPushButton("Cancel")
    #     cancel_btn.setStyleSheet("background-color: #ef4444; color: white;")
    #     cancel_btn.clicked.connect(dialog.close)
        
    #     button_layout.addWidget(book_btn)
    #     button_layout.addWidget(cancel_btn)
        
    #     # Add widgets to layout
    #     layout.addWidget(doctor_label)
    #     layout.addWidget(self.doctor_combo)
    #     layout.addWidget(date_label)
    #     layout.addWidget(self.appt_date)
    #     layout.addWidget(time_label)
    #     layout.addWidget(self.appt_time)
    #     layout.addWidget(reason_label)
    #     layout.addWidget(self.appt_reason)
    #     layout.addLayout(button_layout)
        
    #     dialog.exec_()
        
    # def book_appointment(self):
    #     """Book new appointment in database"""
    #     selected_doctor = self.doctors[self.doctor_combo.currentIndex()]
    #     doctor_id = selected_doctor['id']
        
    #     if not self.appt_reason.toPlainText():
    #         QMessageBox.warning(self, "Error", "Please provide a reason for the appointment")
    #         return
            
    #     appointment = {
    #         "patient_id": self.patient_id,
    #         "doctor_id": doctor_id,
    #         "date": self.appt_date.date().toString("yyyy-MM-dd"),
    #         "time": self.appt_time.time().toString("hh:mm"),
    #         "reason": self.appt_reason.toPlainText(),
    #         "status": "pending"
    #     }
        
    #     # Add to database
    #     self.db.add_appointment(appointment)
    #     QMessageBox.information(self, "Success", "Appointment booked successfully!")
        
    #     # Refresh data
    #     self.load_data()
    #     self.update_appointments_table()
    #     self.sender().parent().close()
        
    def request_prescription_refill(self, prescription_id):
        """Request refill for a prescription"""
        prescription = next((p for p in self.prescriptions if p['id'] == prescription_id), None)
        if not prescription:
            QMessageBox.warning(self, "Error", "Prescription not found")
            return
            
        # Show confirmation dialog
        reply = QMessageBox.question(
            self, 'Confirm Refill Request',
            f"Request refill for:\n\n"
            f"Medication: {prescription['medication']}\n"
            f"Dosage: {prescription['dosage']}\n\n"
            f"This request will be sent to your doctor for approval.",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # In a real app, this would create a refill request in the database
            QMessageBox.information(
                self, "Request Sent",
                "Your refill request has been sent to your doctor.\n"
                "You will be notified when it's approved."
            )
            
            # Could update prescription status or create a refill request record
            # prescription['refill_requested'] = True
            # self.db._save_data(self.db.data)