from .needs import *

LANGUAGES = {
    'en': {
        'page_title': 'My Medical Records',
        'refresh_btn': 'Refresh Records',
        'filter_group': 'Filter Records',
        'from_label': 'From:',
        'to_label': 'To:',
        'doctor_label': 'Doctor:',
        'diagnosis_label': 'Diagnosis:',
        'apply_filters': 'Apply Filters',
        'all_doctors': 'All Doctors',
        'all_diagnoses': 'All Diagnoses',
        'table_headers': ["Date", "Doctor", "Diagnosis", "Treatment", "Actions"],
        'view_details': 'View Details',
        'details_group': 'Record Details',
        'export_btn': 'Export Record',
        'error_title': 'Error',
        'load_error': 'Failed to load records: {}',
        'export_error': 'No record selected to export',
        'details_template': """
            <h2>Medical Record - {date}</h2>
            <table border='0' cellspacing='5' cellpadding='5'>
                <tr><td width='120'><b>Doctor:</b></td><td>{doctor}</td></tr>
                <tr><td><b>Department:</b></td><td>{department}</td></tr>
                <tr><td><b>Date:</b></td><td>{date}</td></tr>
                <tr><td><b>Diagnosis:</b></td><td>{diagnosis}</td></tr>
                <tr><td><b>Treatment:</b></td><td>{treatment}</td></tr>
            </table>
            <h3>Notes</h3>
            <p>{notes}</p>
        """,
        'unknown_doctor': 'Unknown',
        'no_department': 'N/A',
        'no_notes': 'No additional notes'
    },
    'ru': {
        'page_title': 'Медицинские записи',
        'refresh_btn': 'Обновить записи',
        'filter_group': 'Фильтр записей',
        'from_label': 'От:',
        'to_label': 'До:',
        'doctor_label': 'Врач:',
        'diagnosis_label': 'Диагноз:',
        'apply_filters': 'Применить фильтры',
        'all_doctors': 'Все врачи',
        'all_diagnoses': 'Все диагнозы',
        'table_headers': ["Дата", "Врач", "Диагноз", "Лечение", "Действия"],
        'view_details': 'Подробнее',
        'details_group': 'Детали записи',
        'export_btn': 'Экспорт записи',
        'error_title': 'Ошибка',
        'load_error': 'Ошибка загрузки записей: {}',
        'export_error': 'Не выбрана запись для экспорта',
        'details_template': """
            <h2>Медицинская запись - {date}</h2>
            <table border='0' cellspacing='5' cellpadding='5'>
                <tr><td width='120'><b>Врач:</b></td><td>{doctor}</td></tr>
                <tr><td><b>Отделение:</b></td><td>{department}</td></tr>
                <tr><td><b>Дата:</b></td><td>{date}</td></tr>
                <tr><td><b>Диагноз:</b></td><td>{diagnosis}</td></tr>
                <tr><td><b>Лечение:</b></td><td>{treatment}</td></tr>
            </table>
            <h3>Примечания</h3>
            <p>{notes}</p>
        """,
        'unknown_doctor': 'Неизвестно',
        'no_department': 'Н/Д',
        'no_notes': 'Нет дополнительных примечаний'
    }
}

class PatientMedicalRecordsPage(QWidget):
    def __init__(self, user_data, db, lang='en'):
        super().__init__()
        self.user_data = user_data
        self.db = db
        self.lang = lang
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
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        container = QWidget()
        self.layout = QVBoxLayout(container)
        self.layout.setSpacing(20)
        
        scroll.setWidget(container)
        self.main_layout.addWidget(scroll)
        
    def setup_header(self):
        """Setup the page header"""
        header = QHBoxLayout()
        
        title = QLabel(LANGUAGES[self.lang]['page_title'])
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
        """)
        
        self.refresh_btn = QPushButton(LANGUAGES[self.lang]['refresh_btn'])
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
        group = QGroupBox(LANGUAGES[self.lang]['filter_group'])
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
        self.doctor_filter.addItem(LANGUAGES[self.lang]['all_doctors'], "all")
        
        # Diagnosis filter
        self.diagnosis_filter = QComboBox()
        self.diagnosis_filter.addItem(LANGUAGES[self.lang]['all_diagnoses'], "all")
        
        # Filter button
        filter_btn = QPushButton(LANGUAGES[self.lang]['apply_filters'])
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
        
        filter_layout.addWidget(QLabel(LANGUAGES[self.lang]['from_label']))
        filter_layout.addWidget(self.from_date)
        filter_layout.addWidget(QLabel(LANGUAGES[self.lang]['to_label']))
        filter_layout.addWidget(self.to_date)
        filter_layout.addWidget(QLabel(LANGUAGES[self.lang]['doctor_label']))
        filter_layout.addWidget(self.doctor_filter)
        filter_layout.addWidget(QLabel(LANGUAGES[self.lang]['diagnosis_label']))
        filter_layout.addWidget(self.diagnosis_filter)
        filter_layout.addWidget(filter_btn)
        
        group.setLayout(filter_layout)
        self.layout.addWidget(group)
        
    def setup_records_table(self):
        """Setup the medical records table"""
        self.records_table = QTableWidget()
        self.records_table.setColumnCount(5)
        self.records_table.setHorizontalHeaderLabels(
            LANGUAGES[self.lang]['table_headers']
        )
        self.records_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.records_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.records_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.records_table.setSelectionMode(QTableWidget.SingleSelection)
        self.records_table.cellClicked.connect(self.show_record_details)
        
        self.layout.addWidget(self.records_table)
        
    def setup_record_details(self):
        """Setup the record details section"""
        self.details_group = QGroupBox(LANGUAGES[self.lang]['details_group'])
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
        export_btn = QPushButton(LANGUAGES[self.lang]['export_btn'])
        export_btn.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
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
        self.details_group.hide()
        
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
                date_str = record['date'].strftime("%Y-%m-%d") if hasattr(record['date'], 'strftime') else str(record['date'])

                items = [
                    QTableWidgetItem(date_str),
                    QTableWidgetItem(doctor['name'] if doctor else LANGUAGES[self.lang]['unknown_doctor']),
                    QTableWidgetItem(record['diagnosis']),
                    QTableWidgetItem(record['treatment']),
                ]
                
                # View button
                view_btn = QPushButton(LANGUAGES[self.lang]['view_details'])
                view_btn.setStyleSheet("""
                    QPushButton {
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
            QMessageBox.critical(
                self, 
                LANGUAGES[self.lang]['error_title'], 
                LANGUAGES[self.lang]['load_error'].format(str(e))
            )
    
    def update_filter_options(self, records):
        """Update filter dropdowns based on available records"""
        current_doctor = self.doctor_filter.currentData()
        current_diagnosis = self.diagnosis_filter.currentData()
        
        # Clear and repopulate doctor filter
        self.doctor_filter.clear()
        self.doctor_filter.addItem(LANGUAGES[self.lang]['all_doctors'], "all")
        
        doctor_ids = {r['doctor_id'] for r in records}
        doctors = [self.db.get_doctor_by_id(did) for did in doctor_ids]
        doctors = [d for d in doctors if d is not None]
        
        for doctor in sorted(doctors, key=lambda d: d['name']):
            self.doctor_filter.addItem(doctor['name'], doctor['id'])
        
        if current_doctor != "all":
            index = self.doctor_filter.findData(current_doctor)
            if index >= 0:
                self.doctor_filter.setCurrentIndex(index)
        
        # Clear and repopulate diagnosis filter
        self.diagnosis_filter.clear()
        self.diagnosis_filter.addItem(LANGUAGES[self.lang]['all_diagnoses'], "all")
        
        diagnoses = sorted(list({r['diagnosis'] for r in records if r['diagnosis']}))
        
        for diagnosis in diagnoses:
            self.diagnosis_filter.addItem(diagnosis, diagnosis)
        
        if current_diagnosis != "all":
            index = self.diagnosis_filter.findData(current_diagnosis)
            if index >= 0:
                self.diagnosis_filter.setCurrentIndex(index)
    
    def show_record_details(self, record=None):
        """Show detailed view of selected record"""
        if record is None:
            selected_row = self.records_table.currentRow()
            if selected_row < 0:
                return
            record_id = self.records_table.item(selected_row, 0).data(Qt.UserRole)
            all_records = self.db.get_patient_medical_records(self.user_data['id'])
            record = next((r for r in all_records if isinstance(r, dict) and r.get('id') == record_id), None)
            if not record:
                QMessageBox.warning(self, LANGUAGES[self.lang]['error_title'], "Selected record not found")
                return
        
        selected_col = self.records_table.currentColumn()
        if selected_col != 4:
            return
        
        doctor = self.db.get_doctor_by_id(record['doctor_id'])
        
        details_html = LANGUAGES[self.lang]['details_template'].format(
            date=record['date'],
            doctor=doctor['name'] if doctor else LANGUAGES[self.lang]['unknown_doctor'],
            department=doctor['department'] if doctor else LANGUAGES[self.lang]['no_department'],
            diagnosis=record['diagnosis'],
            treatment=record['treatment'],
            notes=record.get('notes', LANGUAGES[self.lang]['no_notes'])
        )
        
        self.details_view.setHtml(details_html)
        self.details_group.show()
        
    def export_record(self):
        """Export current record to PDF or text file"""
        selected_row = self.records_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(
                self, 
                LANGUAGES[self.lang]['error_title'], 
                LANGUAGES[self.lang]['export_error']
            )
            return
            
        record_id = self.records_table.item(selected_row, 0).data(Qt.UserRole)
        QMessageBox.information(
            self, 
            LANGUAGES[self.lang]['export_btn'], 
            f"Would export record {record_id} in a real implementation"
        )