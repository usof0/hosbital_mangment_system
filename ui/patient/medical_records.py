from .needs import *

class PatientMedicalRecordsPage(QWidget):
    def __init__(self, user_data, db):
        super().__init__()
        self.user_data = user_data
        self.db = db
        self.init_ui()
        
    def init_ui(self):
        self.setup_main_layout()
        self.setup_header()
        self.setup_filters()
        self.setup_records_table()
        self.setup_record_details()
        self.load_records()
        
    def setup_main_layout(self):
        """Setup the main layout with scroll area"""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Create scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        # Container widget for scroll area
        container = QWidget()
        self.layout = QVBoxLayout(container)
        self.layout.setSpacing(20)
        
        scroll.setWidget(container)
        self.main_layout.addWidget(scroll)
        
    def setup_header(self):
        """Setup the page header"""
        header = QHBoxLayout()
        
        title = QLabel("My Medical Records")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
        """)
        
        self.refresh_btn = QPushButton("Refresh Records")
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.refresh_btn.clicked.connect(self.load_records)
        
        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.refresh_btn)
        
        self.layout.addLayout(header)
        
    def setup_filters(self):
        """Setup filter controls"""
        group = QGroupBox("Filter Records")
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
        
        filter_layout = QHBoxLayout()
        
        # Date range filters
        self.from_date = QDateEdit()
        self.from_date.setDisplayFormat("yyyy-MM-dd")
        self.from_date.setCalendarPopup(True)
        self.from_date.setDate(QDate.currentDate().addMonths(-6))
        
        self.to_date = QDateEdit()
        self.to_date.setDisplayFormat("yyyy-MM-dd")
        self.to_date.setCalendarPopup(True)
        self.to_date.setDate(QDate.currentDate())
        
        # Doctor filter
        self.doctor_filter = QComboBox()
        self.doctor_filter.addItem("All Doctors", "all")
        
        # Diagnosis filter
        self.diagnosis_filter = QComboBox()
        self.diagnosis_filter.addItem("All Diagnoses", "all")
        
        # Filter button
        filter_btn = QPushButton("Apply Filters")
        filter_btn.setStyleSheet("""
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
        filter_btn.clicked.connect(self.load_records)
        
        filter_layout.addWidget(QLabel("From:"))
        filter_layout.addWidget(self.from_date)
        filter_layout.addWidget(QLabel("To:"))
        filter_layout.addWidget(self.to_date)
        filter_layout.addWidget(QLabel("Doctor:"))
        filter_layout.addWidget(self.doctor_filter)
        filter_layout.addWidget(QLabel("Diagnosis:"))
        filter_layout.addWidget(self.diagnosis_filter)
        filter_layout.addWidget(filter_btn)
        
        group.setLayout(filter_layout)
        self.layout.addWidget(group)
        
    def setup_records_table(self):
        """Setup the medical records table"""
        self.records_table = QTableWidget()
        self.records_table.setColumnCount(5)
        self.records_table.setHorizontalHeaderLabels(
            ["Date", "Doctor", "Diagnosis", "Treatment", "Actions"]
        )
        self.records_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.records_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.records_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.records_table.setSelectionMode(QTableWidget.SingleSelection)
        self.records_table.cellClicked.connect(self.show_record_details)
        
        self.layout.addWidget(self.records_table)
        
    def setup_record_details(self):
        """Setup the record details section"""
        self.details_group = QGroupBox("Record Details")
        self.details_group.setStyleSheet("""
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
        
        details_layout = QVBoxLayout()
        
        self.details_view = QTextEdit()
        self.details_view.setReadOnly(True)
        self.details_view.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 3px;
                padding: 10px;
            }
        """)
        
        # Add export button
        export_btn = QPushButton("Export Record")
        export_btn.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
        """)
        export_btn.clicked.connect(self.export_record)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(export_btn)
        
        details_layout.addWidget(self.details_view)
        details_layout.addLayout(btn_layout)
        self.details_group.setLayout(details_layout)
        
        self.layout.addWidget(self.details_group)
        self.details_group.hide()  # Hide until a record is selected
        
    def load_records(self):
        """Load records based on current filters"""
        try:
            # Get filter values
            from_date = self.from_date.date().toString("yyyy-MM-dd")
            to_date = self.to_date.date().toString("yyyy-MM-dd")
            doctor_id = self.doctor_filter.currentData()
            diagnosis = self.diagnosis_filter.currentData()
            
            # Get records from database
            records = self.db.get_patient_medical_records(
                self.user_data['id'],
                from_date=from_date,
                to_date=to_date,
                doctor_id=doctor_id if doctor_id != "all" else None,
                diagnosis=diagnosis if diagnosis != "all" else None
            )
            
            # Update filters dropdowns
            self.update_filter_options(records)
            
            # Populate table
            self.records_table.setRowCount(len(records))
            
            for row_idx, record in enumerate(records):
                doctor = self.db.get_doctor_by_id(record['doctor_id'])
                
                items = [
                    QTableWidgetItem(record['date']),
                    QTableWidgetItem(doctor['name'] if doctor else "Unknown"),
                    QTableWidgetItem(record['diagnosis']),
                    QTableWidgetItem(record['treatment']),
                ]
                
                # View button
                view_btn = QPushButton("View Details")
                view_btn.setStyleSheet("""
                    QPushButton {
                        color: #3498db;
                        text-decoration: underline;
                        border: none;
                        padding: 5px;
                    }
                    QPushButton:hover {
                        color: #2980b9;
                    }
                """)
                view_btn.clicked.connect(lambda _, r=record: self.show_record_details(r))
                
                for col_idx, item in enumerate(items):
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self.records_table.setItem(row_idx, col_idx, item)
                
                self.records_table.setCellWidget(row_idx, 4, view_btn)
                        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load records: {str(e)}")
    
    def update_filter_options(self, records):
        """Update filter dropdowns based on available records"""
        # Store current selections
        current_doctor = self.doctor_filter.currentData()
        current_diagnosis = self.diagnosis_filter.currentData()
        
        # Clear and repopulate doctor filter
        self.doctor_filter.clear()
        self.doctor_filter.addItem("All Doctors", "all")
        
        # Get unique doctors from records
        doctor_ids = {r['doctor_id'] for r in records}
        doctors = [self.db.get_doctor_by_id(did) for did in doctor_ids]
        doctors = [d for d in doctors if d is not None]
        
        for doctor in sorted(doctors, key=lambda d: d['name']):
            self.doctor_filter.addItem(doctor['name'], doctor['id'])
        
        # Restore previous selection if still available
        if current_doctor != "all":
            index = self.doctor_filter.findData(current_doctor)
            if index >= 0:
                self.doctor_filter.setCurrentIndex(index)
        
        # Clear and repopulate diagnosis filter
        self.diagnosis_filter.clear()
        self.diagnosis_filter.addItem("All Diagnoses", "all")
        
        # Get unique diagnoses from records
        diagnoses = sorted(list({r['diagnosis'] for r in records if r['diagnosis']}))
        
        for diagnosis in diagnoses:
            self.diagnosis_filter.addItem(diagnosis, diagnosis)
        
        # Restore previous selection if still available
        if current_diagnosis != "all":
            index = self.diagnosis_filter.findData(current_diagnosis)
            if index >= 0:
                self.diagnosis_filter.setCurrentIndex(index)
    
    def show_record_details(self, record=None):
        """Show detailed view of selected record"""
        # if record is None:
        #     selected_row = self.records_table.currentRow()
        #     if selected_row < 0:
        #         return
        #     record_id = self.records_table.item(selected_row, 0).data(Qt.UserRole)
        #     record = next((r for r in self.db.get_patient_medical_records(self.user_data['id']) 
        #                  if r['id'] == record_id), None)
        #     if not record:
        #         return
        if record is None:
            selected_row = self.records_table.currentRow()
            if selected_row < 0:
                return
            record_id = self.records_table.item(selected_row, 0).data(Qt.UserRole)

            # Get all medical records
            all_records = self.db.get_patient_medical_records(self.user_data['id'])

            # Ensure we are working with proper dict objects
            record = None
            for r in all_records:
                if isinstance(r, dict) and r.get('id') == record_id:
                    record = r
                    break

            if not record:
                QMessageBox.warning(self, "Error", "Selected record not found")
                return
        selected_col = self.records_table.currentColumn()
        if selected_col != 4:
            return
        
        doctor = self.db.get_doctor_by_id(record['doctor_id'])
        
        details_html = f"""
        <h2>Medical Record - {record['date']}</h2>
        <table border='0' cellspacing='5' cellpadding='5'>
            <tr><td width='120'><b>Doctor:</b></td><td>{doctor['name'] if doctor else 'Unknown'}</td></tr>
            <tr><td><b>Department:</b></td><td>{doctor['department'] if doctor else 'N/A'}</td></tr>
            <tr><td><b>Date:</b></td><td>{record['date']}</td></tr>
            <tr><td><b>Diagnosis:</b></td><td>{record['diagnosis']}</td></tr>
            <tr><td><b>Treatment:</b></td><td>{record['treatment']}</td></tr>
            
        </table>
        <h3>Notes</h3>
        <p>{record.get('notes', 'No additional notes')}</p>
        """
        # <tr><td><b>Prescriptions:</b></td><td>{record.get('prescriptions', 'None')}</td></tr>
        
        self.details_view.setHtml(details_html)
        self.details_group.show()
        
    def export_record(self):
        """Export current record to PDF or text file"""
        # In a real implementation, this would generate a PDF or text file
        selected_row = self.records_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Error", "No record selected to export")
            return
            
        record_id = self.records_table.item(selected_row, 0).data(Qt.UserRole)
        QMessageBox.information(
            self, 
            "Export Record", 
            f"Would export record {record_id} in a real implementation"
        )
