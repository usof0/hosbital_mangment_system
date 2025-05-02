from .doctor.needs import *
from .dashboard import Dashboard

class DoctorDashboard(Dashboard):
    def __init__(self, user_data, db):
        self.user_data = user_data
        self.db = db
        self.doctor_id = user_data['id']  # Initialize doctor_id first
        self.today = datetime.now().strftime('%Y-%m-%d')
        super().__init__("doctor", user_data, db)  # Then call parent init

    def init_ui(self):
        # Clear existing layout if any
        if self.layout():
            QWidget().setLayout(self.layout())
            
        super().init_ui()  # Initialize base dashboard UI
        self.load_data()
        self.setup_ui_components()

    def load_data(self):
        """Load all necessary data from database"""
        self.appointments = self.db.get_todays_appointments(self.doctor_id, self.today)
        self.all_appointments = self.db.get_doctor_appointments(self.doctor_id)
        self.patients = self.get_unique_patients()
        self.prescriptions = [p for p in self.db.get_all_prescriptions() 
                             if p['doctor_id'] == self.doctor_id]

    def switch_page(self, page_name):
        """Handle page switching"""
        if self.main_window:
            self.main_window.switch_page_by_name(page_name)

    def get_unique_patients(self):
        """Get unique patients for this doctor"""
        patient_ids = {a['patient_id'] for a in self.all_appointments if a.get('patient_id')}
        patients = {}
        for pid in patient_ids:
            patient = self.db.get_patient_by_id(pid)
            if patient:  # Only add valid patients
                patients[pid] = patient
        return patients

    def setup_ui_components(self):
        """Setup all UI components"""
        self.setup_stats_cards()
        self.setup_schedule_table()
        self.create_patient_alerts_widget()
        self.setup_appointment_stats()

    def setup_stats_cards(self):
        """Create and display stats cards"""
        cards_layout = QHBoxLayout()
        
        # Calculate stats
        active_patients = len(self.patients)
        today_appts = len(self.appointments)
        monthly_prescriptions = len([p for p in self.prescriptions 
                                   if p['date'].startswith(self.today[:7])])
        
        stats = [
            ("Today's Appointments", str(today_appts), "appointment", "blue"),
            ("Active Patients", str(active_patients), "user-injured", "green"),
            ("Prescriptions This Month", str(monthly_prescriptions), "prescription", "purple"),
            ("Avg. Consultation Time", "15 min", "clock", "yellow")
        ]
        
        for title, value, icon, color in stats:
            card = self.create_card(title, value, icon, color)
            cards_layout.addWidget(card)
            
        self.layout.addLayout(cards_layout)

    # def create_card(self, title, value, icon, color):
    #     """Create a dashboard statistic card"""
    #     card = QWidget()
    #     card.setObjectName("card")
    #     card.setStyleSheet(f"""
    #         QWidget#card {{
    #             background: white;
    #             border-radius: 8px;
    #             padding: 16px;
    #             margin: 4px;
    #         }}
    #     """)
        
    #     layout = QHBoxLayout(card)
        
    #     # Icon
    #     icon_label = QLabel()
    #     try:
    #         icon_path = f"assets/icons/{icon}.png"
    #         if os.path.exists(icon_path):
    #             icon_label.setPixmap(QPixmap(icon_path).scaled(40, 40))
    #         else:
    #             icon_label.setText(icon[0].upper())  # Fallback to first letter
    #     except Exception as e:
    #         print(f"Error loading icon {icon}: {str(e)}")
    #         icon_label.setText(icon[0].upper())
        
        # icon_label.setStyleSheet(f"""
        #     background-color: {color}20;
        #     color: {color};
        #     padding: 8px;
        #     border-radius: 50%;
        #     min-width: 40px;
        #     max-width: 40px;
        #     min-height: 40px;
        #     max-height: 40px;
        #     font-weight: bold;
        # """)
        
    #     # Text
    #     text_widget = QWidget()
    #     text_layout = QVBoxLayout(text_widget)
        
    #     title_label = QLabel(title)
    #     title_label.setStyleSheet("color: #6b7280; font-size: 14px;")
        
    #     value_label = QLabel(value)
    #     value_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        
    #     text_layout.addWidget(title_label)
    #     text_layout.addWidget(value_label)
    #     text_layout.addStretch()
        
    #     layout.addWidget(icon_label)
    #     layout.addWidget(text_widget)
        
    #     return card

    def setup_schedule_table(self):
        """Setup today's schedule table"""
        content_layout = QHBoxLayout()
        
        # Schedule Table Widget
        schedule_widget = QWidget()
        schedule_widget.setObjectName("card")
        schedule_layout = QVBoxLayout(schedule_widget)

        # Header with buttons
        header = QHBoxLayout()
        schedule_title = QLabel("Today's Schedule")
        schedule_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        self.add_appt_btn = QPushButton("Add Appointment")
        self.add_appt_btn.setStyleSheet("""
            background-color: #10b981; 
            color: white;
            padding: 8px;
            border-radius: 4px;
        """)
        self.add_appt_btn.clicked.connect(self.show_add_appointment_dialog)
        
        view_all_btn = QPushButton("View Full Schedule")
        view_all_btn.setStyleSheet("""
            color: #3b82f6; 
            text-decoration: underline;
            border: none;
            padding: 8px;
        """)
        view_all_btn.clicked.connect(lambda: self.switch_page("schedule"))

        header.addWidget(schedule_title)
        header.addWidget(self.add_appt_btn)
        header.addWidget(view_all_btn)

        # Table setup
        self.schedule_table = QTableWidget()
        self.schedule_table.setColumnCount(5)
        self.schedule_table.setHorizontalHeaderLabels(["Time", "Patient", "Reason", "Status", "Actions"])
        self.schedule_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.schedule_table.verticalHeader().setVisible(False)
        self.schedule_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        self.update_schedule_table()

        schedule_layout.addLayout(header)
        schedule_layout.addWidget(self.schedule_table)

        # Patient Alerts Widget
        alerts_widget = self.create_patient_alerts_widget()
        content_layout.addWidget(schedule_widget, stretch=2)
        content_layout.addWidget(alerts_widget, stretch=1)

        self.layout.addLayout(content_layout)

    def update_schedule_table(self):
        """Update the schedule table with current data"""
        self.schedule_table.setRowCount(len(self.appointments))
        
        for row_idx, appt in enumerate(self.appointments):
            patient = self.db.get_patient_by_id(appt['patient_id'])

            time_item = QTableWidgetItem(appt['time'])
            patient_item = QTableWidgetItem(patient['name'] if patient else "Unknown")
            reason_item = QTableWidgetItem(appt['reason'])
            status_item = QTableWidgetItem(appt['status'].capitalize())

            # Status styling
            if appt['status'] == 'completed':
                status_item.setForeground(Qt.darkGreen)
            elif appt['status'] == 'pending':
                status_item.setForeground(Qt.darkYellow)
            elif appt['status'] == 'cancelled':
                status_item.setForeground(Qt.red)

            # Action buttons
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(0, 0, 0, 0)
            action_layout.setSpacing(5)
            
            complete_btn = QPushButton("Complete")
            complete_btn.setStyleSheet("""
                background-color: #10b981; 
                color: white; 
                padding: 2px 5px;
                border-radius: 3px;
            """)
            complete_btn.clicked.connect(lambda _, a=appt: self.update_appointment_status(a['id'], 'completed'))

            cancel_btn = QPushButton("Cancel")
            cancel_btn.setStyleSheet("""
                background-color: #ef4444; 
                color: white; 
                padding: 2px 5px;
                border-radius: 3px;
            """)
            cancel_btn.clicked.connect(lambda _, a=appt: self.update_appointment_status(a['id'], 'cancelled'))

            prescribe_btn = QPushButton("Prescribe")
            prescribe_btn.setStyleSheet("""
                background-color: #3b82f6; 
                color: white; 
                padding: 2px 5px;
                border-radius: 3px;
            """)
            prescribe_btn.clicked.connect(lambda _, a=appt: self.show_prescription_dialog(a['patient_id']))

            action_layout.addWidget(complete_btn)
            action_layout.addWidget(cancel_btn)
            action_layout.addWidget(prescribe_btn)

            self.schedule_table.setItem(row_idx, 0, time_item)
            self.schedule_table.setItem(row_idx, 1, patient_item)
            self.schedule_table.setItem(row_idx, 2, reason_item)
            self.schedule_table.setItem(row_idx, 3, status_item)
            self.schedule_table.setCellWidget(row_idx, 4, action_widget)

    def create_patient_alerts_widget(self):
        """Create the patient alerts widget"""
        alerts_widget = QWidget()
        alerts_widget.setObjectName("card")
        alerts_layout = QVBoxLayout(alerts_widget)
        
        alerts_title = QLabel("Patient Alerts")
        alerts_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        alerts = self.generate_patient_alerts()
        for alert in alerts[:3]:  # Show max 3 alerts
            alert_widget = QWidget()
            alert_widget.setStyleSheet(f"""
                border-left: 4px solid {alert['color']};
                padding-left: 8px;
                margin-bottom: 8px;
            """)
            
            alert_layout = QVBoxLayout(alert_widget)
            
            # Header
            header = QHBoxLayout()
            title = QLabel(alert['title'])
            title.setStyleSheet("font-weight: bold;")
            
            status = QLabel(alert['status'])
            status.setStyleSheet(f"""
                background-color: {alert['color']}20;
                color: {alert['color']};
                padding: 2px 8px;
                border-radius: 4px;
                font-size: 12px;
            """)
            
            header.addWidget(title)
            header.addWidget(status)
            
            # Details
            details = QLabel(alert['details'])
            details.setStyleSheet("color: #6b7280; font-size: 12px;")
            
            alert_layout.addLayout(header)
            alert_layout.addWidget(details)
            
            # Action button if exists
            if alert.get('action'):
                action_btn = QPushButton(alert['action_text'])
                action_btn.setStyleSheet(f"""
                    color: {alert['color']};
                    text-decoration: underline;
                    border: none;
                    text-align: left;
                    padding: 0;
                    margin-top: 4px;
                """)
                action_btn.clicked.connect(alert['action'])
                alert_layout.addWidget(action_btn)
            
            alerts_layout.addWidget(alert_widget)
        
        view_all_btn = QPushButton("View All Patients")
        view_all_btn.setStyleSheet("""
            color: #3b82f6;
            text-decoration: underline;
            border: none;
            padding: 8px 0;
        """)
        view_all_btn.clicked.connect(lambda: self.switch_page("my-patients"))
        
        alerts_layout.addWidget(alerts_title)
        alerts_layout.addSpacing(10)
        alerts_layout.addWidget(view_all_btn, alignment=Qt.AlignRight)
        
        return alerts_widget

    def generate_patient_alerts(self):
        """Generate patient alerts based on conditions"""
        alerts = []
        
        # 1. Critical blood types
        for pid, patient in self.patients.items():
            if patient.get('blood_type') in ['O-', 'AB-']:
                alerts.append({
                    'title': "Critical Blood Type",
                    'details': f"{patient['name']} (Blood Type: {patient.get('blood_type', 'Unknown')}",
                    'status': "High Risk",
                    'color': "red",
                    'action_text': "View Patient",
                    'action': lambda _, p=pid: self.view_patient_report(p)
                })
        
        # 2. Expiring prescriptions
        for presc in self.prescriptions:
            if presc['status'] == 'active':
                presc_date = datetime.strptime(presc['date'], '%Y-%m-%d').date()
                if (datetime.now().date() - presc_date).days > 25:  # Older than 25 days
                    patient = self.db.get_patient_by_id(presc['patient_id'])
                    if patient:
                        alerts.append({
                            'title': "Expiring Prescription",
                            'details': f"{presc['medication']} for {patient['name']}",
                            'status': "Attention",
                            'color': "orange",
                            'action_text': "Renew Prescription",
                            'action': lambda _, p=presc['patient_id']: self.show_prescription_dialog(p)
                        })
        
        # 3. Patients needing follow-up
        for pid, patient in self.patients.items():
            last_appt = None
            for appt in sorted(self.all_appointments, key=lambda x: x['date'], reverse=True):
                if appt['patient_id'] == pid and appt['status'] == 'completed':
                    last_appt = appt
                    break
            
            if last_appt:
                last_date = datetime.strptime(last_appt['date'], '%Y-%m-%d').date()
                if (datetime.now().date() - last_date).days > 180:  # No visit in 6 months
                    alerts.append({
                        'title': "Needs Follow-up",
                        'details': f"{patient['name']} (Last visit: {last_appt['date']})",
                        'status': "Reminder",
                        'color': "blue",
                        'action_text': "Schedule Visit",
                        'action': lambda _, p=pid: self.schedule_follow_up(p)
                    })
        
        return alerts

    def setup_appointment_stats(self):
        """Setup appointment statistics section"""
        stats_widget = QWidget()
        stats_widget.setObjectName("chart-container")
        stats_layout = QVBoxLayout(stats_widget)
        
        stats_title = QLabel("Appointment Statistics")
        stats_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        # Calculate stats
        completed = len([a for a in self.all_appointments if a['status'] == 'completed'])
        cancelled = len([a for a in self.all_appointments if a['status'] == 'cancelled'])
        pending = len([a for a in self.all_appointments if a['status'] == 'pending'])
        total = len(self.all_appointments)
        
        # Create HTML content
        stats_html = f"""
        <div style='font-size: 14px; line-height: 1.6;'>
            <p><b>Total Appointments:</b> {total}</p>
            <p><b>Completed:</b> {completed} ({completed/total*100:.1f}%)</p>
            <p><b>Cancelled:</b> {cancelled} ({cancelled/total*100:.1f}%)</p>
            <p><b>Pending:</b> {pending} ({pending/total*100:.1f}%)</p>
        </div>
        """
        
        stats_text = QLabel()
        stats_text.setTextFormat(Qt.RichText)
        stats_text.setText(stats_html)
        
        stats_layout.addWidget(stats_title)
        stats_layout.addWidget(stats_text)
        stats_layout.addStretch()
        
        self.layout.addWidget(stats_widget)

    def show_add_appointment_dialog(self):
        """Show dialog to add new appointment"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Add New Appointment")
        dialog.setFixedSize(400, 300)
        
        layout = QVBoxLayout(dialog)
        
        # Patient selection
        patient_label = QLabel("Patient:")
        self.patient_combo = QComboBox()
        self.patient_combo.addItems([p['name'] for p in self.patients.values()])
        
        # Date and time
        date_label = QLabel("Date:")
        self.appt_date = QDateEdit()
        self.appt_date.setDate(QDate.currentDate())
        self.appt_date.setMinimumDate(QDate.currentDate())
        self.appt_date.setCalendarPopup(True)
        
        time_label = QLabel("Time:")
        self.appt_time = QTimeEdit()
        self.appt_time.setTime(QTime(9, 0))
        self.appt_time.setDisplayFormat("hh:mm AP")
        
        # Reason
        reason_label = QLabel("Reason:")
        self.appt_reason = QLineEdit()
        self.appt_reason.setPlaceholderText("e.g., Follow-up, Consultation")
        
        # Buttons
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Save Appointment")
        save_btn.setStyleSheet("background-color: #10b981; color: white;")
        save_btn.clicked.connect(lambda: self.save_appointment(dialog))
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("background-color: #ef4444; color: white;")
        cancel_btn.clicked.connect(dialog.reject)
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        
        # Add widgets to layout
        layout.addWidget(patient_label)
        layout.addWidget(self.patient_combo)
        layout.addWidget(date_label)
        layout.addWidget(self.appt_date)
        layout.addWidget(time_label)
        layout.addWidget(self.appt_time)
        layout.addWidget(reason_label)
        layout.addWidget(self.appt_reason)
        layout.addLayout(button_layout)
        
        dialog.exec_()

    def save_appointment(self, dialog):
        """Save new appointment to database"""
        patient_name = self.patient_combo.currentText()
        patient_id = next((pid for pid, p in self.patients.items() if p['name'] == patient_name), None)
        
        if not patient_id:
            QMessageBox.warning(self, "Error", "Please select a valid patient")
            return
            
        if not self.appt_reason.text():
            QMessageBox.warning(self, "Error", "Please enter a reason for the appointment")
            return
            
        appointment = {
            "patient_id": patient_id,
            "doctor_id": self.doctor_id,
            "date": self.appt_date.date().toString("yyyy-MM-dd"),
            "time": self.appt_time.time().toString("hh:mm"),
            "reason": self.appt_reason.text(),
            "status": "pending"
        }
        
        self.db.add_appointment(appointment)
        QMessageBox.information(self, "Success", "Appointment added successfully!")
        
        # Refresh data
        self.load_data()
        self.update_schedule_table()
        dialog.accept()

    def update_appointment_status(self, appointment_id, status):
        """Update appointment status in database"""
        if self.db.update_appointment_status(appointment_id, status):
            QMessageBox.information(self, "Success", f"Appointment marked as {status}!")
            self.load_data()
            self.update_schedule_table()
        else:
            QMessageBox.warning(self, "Error", "Failed to update appointment")

    def show_prescription_dialog(self, patient_id):
        """Show dialog to write prescription"""
        patient = self.db.get_patient_by_id(patient_id)
        if not patient:
            QMessageBox.warning(self, "Error", "Patient not found")
            return
            
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Prescription for {patient['name']}")
        dialog.setFixedSize(500, 400)
        
        layout = QVBoxLayout(dialog)
        
        # Medication fields
        med_label = QLabel("Medication:")
        self.med_input = QLineEdit()
        self.med_input.setPlaceholderText("e.g., Amoxicillin 500mg")
        
        dosage_label = QLabel("Dosage:")
        self.dosage_input = QLineEdit()
        self.dosage_input.setPlaceholderText("e.g., 1 tablet every 8 hours")
        
        duration_label = QLabel("Duration:")
        self.duration_input = QLineEdit()
        self.duration_input.setPlaceholderText("e.g., 7 days")
        
        instructions_label = QLabel("Instructions:")
        self.instructions_input = QTextEdit()
        self.instructions_input.setPlaceholderText("Special instructions...")
        self.instructions_input.setMaximumHeight(80)
        
        # Buttons
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Save Prescription")
        save_btn.setStyleSheet("background-color: #10b981; color: white;")
        save_btn.clicked.connect(lambda: self.save_prescription(dialog, patient_id))
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("background-color: #ef4444; color: white;")
        cancel_btn.clicked.connect(dialog.reject)
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        
        # Add widgets to layout
        layout.addWidget(med_label)
        layout.addWidget(self.med_input)
        layout.addWidget(dosage_label)
        layout.addWidget(self.dosage_input)
        layout.addWidget(duration_label)
        layout.addWidget(self.duration_input)
        layout.addWidget(instructions_label)
        layout.addWidget(self.instructions_input)
        layout.addLayout(button_layout)
        
        dialog.exec_()

    def save_prescription(self, dialog, patient_id):
        """Save prescription to database"""
        if not all([self.med_input.text(), self.dosage_input.text(), self.duration_input.text()]):
            QMessageBox.warning(self, "Error", "Please fill in all required fields")
            return
            
        prescription = {
            "patient_id": patient_id,
            "doctor_id": self.doctor_id,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "medication": self.med_input.text(),
            "dosage": self.dosage_input.text(),
            "duration": self.duration_input.text(),
            "instructions": self.instructions_input.toPlainText(),
            "status": "active"
        }
        
        self.db.add_prescription(prescription)
        QMessageBox.information(self, "Success", "Prescription saved successfully!")
        dialog.accept()

    def view_patient_report(self, patient_id):
        """View patient medical report"""
        patient = self.db.get_patient_by_id(patient_id)
        if not patient:
            QMessageBox.warning(self, "Error", "Patient not found")
            return
            
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Medical Report: {patient['name']}")
        dialog.setFixedSize(600, 500)
        
        layout = QVBoxLayout(dialog)
        
        # Patient info
        info_html = f"""
        <h3>{patient['name']}</h3>
        <p><b>ID:</b> {patient['id']}</p>
        <p><b>DOB:</b> {patient.get('date_of_birth', 'Unknown')}</p>
        <p><b>Blood Type:</b> {patient.get('blood_type', 'Unknown')}</p>
        <p><b>Insurance:</b> {patient.get('insurance', 'None')}</p>
        """
        
        info_label = QLabel(info_html)
        info_label.setTextFormat(Qt.RichText)
        
        # Medical records
        records_label = QLabel("Medical History:")
        records_text = QTextEdit()
        records_text.setReadOnly(True)
        
        records = self.db.get_patient_medical_records(patient_id)
        if records:
            records_html = "<ul>"
            for record in sorted(records, key=lambda x: x['date'], reverse=True):
                doctor = self.db.get_doctor_by_id(record['doctor_id'])
                records_html += f"""
                <li>
                    <b>{record['date']}</b> - {doctor['name'] if doctor else 'Unknown'}<br>
                    <b>Diagnosis:</b> {record['diagnosis']}<br>
                    <b>Treatment:</b> {record['treatment']}
                </li>
                """
            records_html += "</ul>"
        else:
            records_html = "<p>No medical records found</p>"
            
        records_text.setHtml(records_html)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dialog.accept)
        
        # Add widgets to layout
        layout.addWidget(info_label)
        layout.addWidget(records_label)
        layout.addWidget(records_text)
        layout.addWidget(close_btn)
        
        dialog.exec_()

    def schedule_follow_up(self, patient_id):
        """Schedule follow-up appointment"""
        patient = self.db.get_patient_by_id(patient_id)
        if not patient:
            QMessageBox.warning(self, "Error", "Patient not found")
            return
            
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Follow-up for {patient['name']}")
        dialog.setFixedSize(400, 300)
        
        layout = QVBoxLayout(dialog)
        
        # Date and time
        date_label = QLabel("Date:")
        follow_up_date = QDateEdit()
        follow_up_date.setDate(QDate.currentDate().addDays(7))
        follow_up_date.setMinimumDate(QDate.currentDate())
        
        time_label = QLabel("Time:")
        follow_up_time = QTimeEdit()
        follow_up_time.setTime(QTime(9, 0))
        
        # Reason
        reason_label = QLabel("Reason:")
        follow_up_reason = QLineEdit()
        follow_up_reason.setText("Follow-up appointment")
        
        # Buttons
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Schedule")
        save_btn.setStyleSheet("background-color: #10b981; color: white;")
        save_btn.clicked.connect(lambda: self.save_follow_up(
            dialog, patient_id, follow_up_date, follow_up_time, follow_up_reason
        ))
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("background-color: #ef4444; color: white;")
        cancel_btn.clicked.connect(dialog.reject)
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        
        # Add widgets to layout
        layout.addWidget(date_label)
        layout.addWidget(follow_up_date)
        layout.addWidget(time_label)
        layout.addWidget(follow_up_time)
        layout.addWidget(reason_label)
        layout.addWidget(follow_up_reason)
        layout.addLayout(button_layout)
        
        dialog.exec_()

    def save_follow_up(self, dialog, patient_id, date_edit, time_edit, reason_input):
        """Save follow-up appointment"""
        appointment = {
            "patient_id": patient_id,
            "doctor_id": self.doctor_id,
            "date": date_edit.date().toString("yyyy-MM-dd"),
            "time": time_edit.time().toString("hh:mm"),
            "reason": reason_input.text(),
            "status": "pending"
        }
        
        self.db.add_appointment(appointment)
        QMessageBox.information(self, "Success", "Follow-up appointment scheduled!")
        
        # Refresh data
        self.load_data()
        self.update_schedule_table()
        dialog.accept()