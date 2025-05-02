from .needs import *

class BookAppointmentDialog(QDialog):
    def __init__(self, user_data, db, parent=None):
        super().__init__(parent)
        self.user_data = user_data
        self.db = db
        self.doctors = self.db.get_all_doctors()
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Book New Appointment")
        self.setMinimumSize(700, 600)
        
        # Main layout with scroll area
        main_layout = QVBoxLayout(self)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        # Container widget
        container = QWidget()
        self.layout = QVBoxLayout(container)
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        self.setup_doctor_selection()
        self.setup_date_time()
        self.setup_reason()
        self.setup_buttons()
        
        scroll.setWidget(container)
        main_layout.addWidget(scroll)
        
    def setup_doctor_selection(self):
        """Setup doctor selection components"""
        group = QGroupBox("Select Doctor")
        group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
        """)
        
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)
        form.setSpacing(15)
        
        # Department filter
        self.dept_filter = QComboBox()
        self.dept_filter.addItem("All Departments", "all")
        departments = sorted(list({d['department'] for d in self.doctors}))
        for dept in departments:
            self.dept_filter.addItem(dept, dept)
        self.dept_filter.currentIndexChanged.connect(self.filter_doctors)
        
        # Doctor selection
        self.doctor_combo = QComboBox()
        self.populate_doctor_combo()
        
        # Doctor info display
        self.doctor_info = QTextEdit()
        self.doctor_info.setReadOnly(True)
        self.doctor_info.setMaximumHeight(100)
        self.doctor_info.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 3px;
                padding: 5px;
            }
        """)
        
        # Connect doctor selection change
        self.doctor_combo.currentIndexChanged.connect(self.update_doctor_info)
        
        form.addRow("Filter by Department:", self.dept_filter)
        form.addRow("Select Doctor:", self.doctor_combo)
        form.addRow("Doctor Information:", self.doctor_info)
        self.doctor_combo.currentIndexChanged.connect(self.update_doctor_info)

        self.update_doctor_info()
        
        group.setLayout(form)
        self.layout.addWidget(group)
        
    def populate_doctor_combo(self, department="all"):
        """Populate doctor combo box with filtered doctors"""
        self.doctor_combo.clear()
        
        if department == "all":
            doctors = self.doctors
        else:
            doctors = [d for d in self.doctors if d['department'] == department]
        
        for doctor in doctors:
            self.doctor_combo.addItem(
                f"Dr. {doctor['name']} ({doctor['specialization']})", 
                doctor['id']
            )
        
        # if doctors:
        #     self.update_doctor_info()
        
    def filter_doctors(self):
        """Filter doctors based on department selection"""
        department = self.dept_filter.currentData()
        self.populate_doctor_combo(department)
        
    def update_doctor_info(self):
        """Update doctor information display"""
        doctor_id = self.doctor_combo.currentData()
        if not doctor_id:
            self.doctor_info.clear()
            return
            
        doctor = next((d for d in self.doctors if d['id'] == doctor_id), None)
        if not doctor:
            return
            
        info = f"""
        <b>Name:</b> Dr. {doctor['name']}<br>
        <b>Department:</b> {doctor['department']}<br>
        <b>Specialization:</b> {doctor['specialization']}<br>
        <b>Contact:</b> {doctor.get('email', 'N/A')}<br>
        <b>Availability:</b> {doctor.get('availability', 'Mon-Fri, 9AM-5PM')}
        """
        self.doctor_info.setHtml(info)
        
    def setup_date_time(self):
        """Setup date and time selection components"""
        group = QGroupBox("Appointment Date & Time")
        group.setStyleSheet(group.styleSheet())
        
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)
        form.setSpacing(15)
        
        # Date selection
        self.appt_date = QDateEdit()
        self.appt_date.setDate(QDate.currentDate())
        self.appt_date.setMinimumDate(QDate.currentDate())
        self.appt_date.setCalendarPopup(True)
        self.appt_date.setStyleSheet("padding: 5px;")
        
        # Time selection
        self.appt_time = QTimeEdit()
        self.appt_time.setTime(QTime(9, 0))  # Default to 9:00 AM
        self.appt_time.setDisplayFormat("hh:mm AP")
        self.appt_time.setStyleSheet("padding: 5px;")
        
        # Available slots
        self.available_slots = QLabel("Available time slots will appear here")
        self.available_slots.setStyleSheet("font-style: italic; color: #7f8c8d;")
        
        form.addRow("Date:", self.appt_date)
        form.addRow("Time:", self.appt_time)
        form.addRow("Available Slots:", self.available_slots)
        
        group.setLayout(form)
        self.layout.addWidget(group)
        
    def setup_reason(self):
        """Setup appointment reason input"""
        group = QGroupBox("Appointment Details")
        group.setStyleSheet(group.styleSheet())
        
        layout = QVBoxLayout()
        
        self.appt_reason = QTextEdit()
        self.appt_reason.setPlaceholderText("Please describe the reason for your appointment...")
        self.appt_reason.setMaximumHeight(120)
        self.appt_reason.setStyleSheet("""
            QTextEdit {
                border: 1px solid #dee2e6;
                border-radius: 3px;
                padding: 5px;
            }
        """)
        
        layout.addWidget(self.appt_reason)
        group.setLayout(layout)
        self.layout.addWidget(group)
        
    def setup_buttons(self):
        """Setup action buttons"""
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        # Cancel button
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        
        # Book button
        book_btn = QPushButton("Book Appointment")
        book_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        book_btn.clicked.connect(self.book_appointment)
        
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(book_btn)
        
        self.layout.addLayout(btn_layout)
        
    def book_appointment(self):
        """Handle appointment booking"""
        # Validate inputs
        if not self.doctor_combo.currentData():
            QMessageBox.warning(self, "Error", "Please select a doctor")
            return
            
        if not self.appt_reason.toPlainText().strip():
            QMessageBox.warning(self, "Error", "Please provide a reason for the appointment")
            return
            
        # Prepare appointment data
        appointment = {
            "patient_id": self.user_data['id'],
            "doctor_id": self.doctor_combo.currentData(),
            "date": self.appt_date.date().toString("yyyy-MM-dd"),
            "time": self.appt_time.time().toString("hh:mm AP"),
            "reason": self.appt_reason.toPlainText(),
            "status": "pending",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        try:
            # Save to database
            self.db.add_appointment(appointment)
            
            # Show success message
            QMessageBox.information(
                self, 
                "Appointment Booked", 
                "Your appointment has been successfully booked!\n\n"
                f"Doctor: Dr. {next(d['name'] for d in self.doctors if d['id'] == appointment['doctor_id'])}\n"
                f"Date: {appointment['date']}\n"
                f"Time: {appointment['time']}"
            )
            
            # Close dialog with success
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Booking Failed",
                f"Failed to book appointment:\n{str(e)}"
            )