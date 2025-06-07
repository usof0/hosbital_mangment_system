from .needs import *
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import Qt, QDate
import csv
from datetime import datetime, timedelta

LANGUAGES = {
    'en': {
        'page_title': 'Reports',
        'export_button': 'Export to CSV',
        'generate_button': 'Generate Report',
        'filters_group': 'Report Filters',
        'report_type': 'Report Type',
        'report_types': [
            'Financial Summary',
            'Patient Statistics',
            'Doctor Performance',
            'Appointment Analysis',
            'Prescription Report'
        ],
        'date_range': 'Date Range',
        'date_ranges': [
            'Today',
            'This Week',
            'This Month',
            'This Quarter',
            'This Year',
            'Custom Range'
        ],
        'from_date': 'From',
        'to_date': 'To',
        'table_headers': {
            'financial': ['ID', 'Date', 'Patient', 'Amount', 'Status', 'Payment Method', 'Payment Date'],
            'patient': ['ID', 'Name', 'Age', 'Appointments', 'Last Visit'],
            'doctor': ['ID', 'Name', 'Specialization', 'Appointments', 'Completed', 'Cancelled', 'Completion Rate'],
            'appointment': ['ID', 'Date', 'Time', 'Patient', 'Doctor', 'Reason', 'Status', 'Duration'],
            'prescription': ['ID', 'Date', 'Patient', 'Doctor', 'Medication', 'Dosage', 'Status']
        },
        'messages': {
            'export_success': 'Report saved to {path}',
            'export_failed': 'Failed to save report: {error}',
            'no_data': 'No data to export',
            'report_error': 'Failed to generate report: {error}',
            'summary': {
                'patients': 'Total Patients: {total} | Active Patients: {active}',
                'doctors': 'Total Appointments: {total} | Avg Completion Rate: {rate:.1f}%',
                'prescriptions': 'Total Prescriptions: {total} | Top Medications: {meds}'
            }
        },
        'scheduled': 'scheduled',
        'completed': 'completed',
        'cancelled': 'cancelled',
        'no-show': 'no-show',
        'pending': 'pending',
        'paid': 'paid',
        'refunded': 'refunded',
        'active': 'active',

    },
    'ru': {
        'page_title': 'Отчеты',
        'export_button': 'Экспорт в CSV',
        'generate_button': 'Сформировать отчет',
        'filters_group': 'Фильтры отчетов',
        'report_type': 'Тип отчета',
        'report_types': [
            'Финансовая сводка',
            'Статистика пациентов',
            'Эффективность врачей',
            'Анализ записей',
            'Отчет по рецептам'
        ],
        'date_range': 'Период',
        'date_ranges': [
            'Сегодня',
            'Эта неделя',
            'Этот месяц',
            'Этот квартал',
            'Этот год',
            'Выбрать период'
        ],
        'from_date': 'С',
        'to_date': 'По',
        'table_headers': {
            'financial': ['ID', 'Дата', 'Пациент', 'Сумма', 'Статус', 'Метод оплаты', 'Дата оплаты'],
            'patient': ['ID', 'Имя', 'Возраст', 'Записи', 'Последний визит'],
            'doctor': ['ID', 'Имя', 'Специализация', 'Записи', 'Завершено', 'Отменено', 'Процент завершения'],
            'appointment': ['ID', 'Дата', 'Время', 'Пациент', 'Врач', 'Причина', 'Статус', 'Длительность'],
            'prescription': ['ID', 'Дата', 'Пациент', 'Врач', 'Лекарство', 'Дозировка', 'Статус']
        },
        'messages': {
            'export_success': 'Отчет сохранен в {path}',
            'export_failed': 'Ошибка сохранения отчета: {error}',
            'no_data': 'Нет данных для экспорта',
            'report_error': 'Ошибка формирования отчета: {error}',
            'summary': {
                'patients': 'Всего пациентов: {total} | Активных: {active}',
                'doctors': 'Всего записей: {total} | Средний процент завершения: {rate:.1f}%',
                'prescriptions': 'Всего рецептов: {total} | Популярные лекарства: {meds}'
            }
        },
        'scheduled': 'запланировано',
        'completed': 'завершено',
        'cancelled': 'отменено',
        'no-show': 'не явился',
        'pending': 'в ожидании',
        'paid': 'оплачено',
        'refunded': 'возвращено',
        'active': 'активно',

    }
}

class ReportsPage(QWidget):
    def __init__(self, user_data, db, lang='en'):
        super().__init__()
        self.user_data = user_data
        self.db = db
        self.lang = lang
        self.init_ui()
        
    def init_ui(self):
        self.setup_main_layout()
        self.setup_header()
        self.setup_report_filters()
        self.setup_report_results()
        
    def setup_main_layout(self):
        self.layout = QVBoxLayout(self)
        
    def setup_header(self):
        header = QHBoxLayout()
        
        title = QLabel(LANGUAGES[self.lang]['page_title'])
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        
        export_btn = QPushButton(LANGUAGES[self.lang]['export_button'])
        export_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        export_btn.clicked.connect(self.export_to_csv)
        
        generate_btn = QPushButton(LANGUAGES[self.lang]['generate_button'])
        generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
        """)
        generate_btn.clicked.connect(self.generate_report)
        
        header.addWidget(title)
        header.addStretch()
        header.addWidget(export_btn)
        header.addWidget(generate_btn)
        
        self.layout.addLayout(header)
        
    def setup_report_filters(self):
        group = QGroupBox(LANGUAGES[self.lang]['filters_group'])
        group.setStyleSheet(group.styleSheet())
        
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)
        
        lang = LANGUAGES[self.lang]
        
        self.report_type = QComboBox()
        self.report_type.addItems(lang['report_types'])
        
        self.date_range = QComboBox()
        self.date_range.addItems(lang['date_ranges'])
        
        self.custom_from = QDateEdit()
        self.custom_from.setDisplayFormat("yyyy-MM-dd")
        self.custom_from.setCalendarPopup(True)
        self.custom_from.setDate(QDate.currentDate().addMonths(-1))
        
        self.custom_to = QDateEdit()
        self.custom_to.setDisplayFormat("yyyy-MM-dd")
        self.custom_to.setCalendarPopup(True)
        self.custom_to.setDate(QDate.currentDate())
        
        # Only show custom date range when selected
        self.custom_from.hide()
        self.custom_to.hide()
        self.date_range.currentTextChanged.connect(self.toggle_custom_dates)
        
        form.addRow(lang['report_type'] + ":", self.report_type)
        form.addRow(lang['date_range'] + ":", self.date_range)
        form.addRow(lang['from_date'] + ":", self.custom_from)
        form.addRow(lang['to_date'] + ":", self.custom_to)
        
        group.setLayout(form)
        self.layout.addWidget(group)
        
    def toggle_custom_dates(self, text):
        custom_range_text = LANGUAGES[self.lang]['date_ranges'][5]  # "Custom Range" or "Выбрать период"
        if text == custom_range_text:
            self.custom_from.show()
            self.custom_to.show()
        else:
            self.custom_from.hide()
            self.custom_to.hide()
        
    def setup_report_results(self):
        self.results_table = QTableWidget()
        self.results_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.results_table.setSortingEnabled(True)
        
        self.summary_label = QLabel()
        self.summary_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.summary_label.setAlignment(Qt.AlignRight)
        
        self.layout.addWidget(self.results_table)
        self.layout.addWidget(self.summary_label)
        
    def generate_report(self):
        report_type_index = self.report_type.currentIndex()
        report_types = LANGUAGES[self.lang]['report_types']
        report_type = report_types[report_type_index]
        
        date_range_index = self.date_range.currentIndex()
        date_range = LANGUAGES[self.lang]['date_ranges'][date_range_index]
        
        try:
            if report_type == report_types[0]:  # Financial Summary
                self.generate_financial_report(date_range)
            elif report_type == report_types[1]:  # Patient Statistics
                self.generate_patient_report(date_range)
            elif report_type == report_types[2]:  # Doctor Performance
                self.generate_doctor_report(date_range)
            elif report_type == report_types[3]:  # Appointment Analysis
                self.generate_appointment_report(date_range)
            elif report_type == report_types[4]:  # Prescription Report
                self.generate_prescription_report(date_range)
                
        except Exception as e:
            QMessageBox.critical(
                self, 
                LANGUAGES[self.lang]['messages']['report_error'].split(':')[0],
                LANGUAGES[self.lang]['messages']['report_error'].format(error=str(e))
            )
    
    def get_dates(self, date_range):
        today = QDate.currentDate()
        lang = LANGUAGES[self.lang]['date_ranges']
        
        if date_range == lang[0]:  # Today
            date_str = today.toString("yyyy-MM-dd")
            return (date_str, date_str)
        elif date_range == lang[1]:  # This Week
            start = today.addDays(-today.dayOfWeek() + 1)
            return (start.toString("yyyy-MM-dd"), today.toString("yyyy-MM-dd"))
        elif date_range == lang[2]:  # This Month
            start = QDate(today.year(), today.month(), 1)
            return (start.toString("yyyy-MM-dd"), today.toString("yyyy-MM-dd"))
        elif date_range == lang[3]:  # This Quarter
            quarter = (today.month() - 1) // 3 + 1
            start_month = (quarter - 1) * 3 + 1
            start = QDate(today.year(), start_month, 1)
            return (start.toString("yyyy-MM-dd"), today.toString("yyyy-MM-dd"))
        elif date_range == lang[4]:  # This Year
            start = QDate(today.year(), 1, 1)
            return (start.toString("yyyy-MM-dd"), today.toString("yyyy-MM-dd"))
        elif date_range == lang[5]:  # Custom Range
            return (
                self.custom_from.date().toString("yyyy-MM-dd"),
                self.custom_to.date().toString("yyyy-MM-dd")
            )
        return (None, None)
    
    def generate_financial_report(self, date_range):
        from_date, to_date = self.get_dates(date_range)
        
        bills = self.db.get_billing_with_details({
            'date_from': from_date,
            'date_to': to_date
        })
        
        headers = LANGUAGES[self.lang]['table_headers']['financial']
        self.results_table.setColumnCount(len(headers))
        self.results_table.setHorizontalHeaderLabels(headers)
        self.results_table.setRowCount(len(bills))
        
        for row_idx, bill in enumerate(bills):
            items = [
                QTableWidgetItem(str(bill['id'])),
                QTableWidgetItem(str(bill.get('date', ''))),
                QTableWidgetItem(bill['patient_name']),
                QTableWidgetItem(f"${float(bill['amount']):.2f}"),
                QTableWidgetItem(LANGUAGES[self.lang][bill['status']].capitalize()),
                QTableWidgetItem(bill.get('payment_method', '')),
                QTableWidgetItem(str(bill.get('payment_date', '')))
            ]
            
            for col_idx, item in enumerate(items):
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.results_table.setItem(row_idx, col_idx, item)
    
    def generate_patient_report(self, date_range):
        from_date, to_date = self.get_dates(date_range)
        patients = self.db.get_all_patients()
        appointments = self.db.get_all_appointments()

        patient_stats = []

        for patient in patients:
            patient_appointments = []
            for appt in appointments:
                if appt['patient_id'] == patient['id']:
                    try:
                        # Get appointment date
                        appt_date = appt['date']

                        # Normalize appt_date to datetime.date
                        if isinstance(appt_date, str):
                            appt_date = datetime.strptime(appt_date, "%Y-%m-%d").date()
                        elif isinstance(appt_date, datetime):
                            appt_date = appt_date.date()

                        # Normalize from_date and to_date if needed
                        fd = from_date
                        td = to_date

                        # Optional: convert from_date/to_date from string to date if passed as string
                        if isinstance(fd, str):
                            fd = datetime.strptime(fd, "%Y-%m-%d").date()
                        if isinstance(td, str):
                            td = datetime.strptime(td, "%Y-%m-%d").date()

                        # Now all dates are datetime.date objects - safe to compare
                        include = True
                        if fd is not None and appt_date < fd:
                            include = False
                        if td is not None and appt_date > td:
                            include = False

                        if include:
                            patient_appointments.append(appt)

                    except Exception as e:
                        print("Error parsing appointment date:", e)
                        continue

            # Handle last visit
            if patient_appointments:
                last_visit_date = max(a['date'] for a in patient_appointments)

                if isinstance(last_visit_date, str):
                    last_visit_date = datetime.strptime(last_visit_date, "%Y-%m-%d").date()
                elif isinstance(last_visit_date, datetime):
                    last_visit_date = last_visit_date.date()

                last_visit = last_visit_date.strftime("%Y-%m-%d")
            else:
                last_visit = LANGUAGES[self.lang]['messages']['summary']['patients'].split('|')[0].split(':')[0] + 'Never'

            patient_stats.append({
                'id': patient['id'],
                'name': patient['name'],
                'appointments': len(patient_appointments),
                'last_visit': last_visit
            })

        headers = LANGUAGES[self.lang]['table_headers']['patient']
        self.results_table.setColumnCount(len(headers))
        self.results_table.setHorizontalHeaderLabels(headers)
        self.results_table.setRowCount(len(patient_stats))
        
        for row_idx, stat in enumerate(patient_stats):
            age = self.calculate_age(patient['date_of_birth']) if 'date_of_birth' in patient else ""
            
            items = [
                QTableWidgetItem(str(stat['id'])),
                QTableWidgetItem(stat['name']),
                QTableWidgetItem(age),
                QTableWidgetItem(str(stat['appointments'])),
                QTableWidgetItem(stat['last_visit'])
            ]
            
            for col_idx, item in enumerate(items):
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.results_table.setItem(row_idx, col_idx, item)
        
        total_patients = len(patients)
        active_patients = len([p for p in patient_stats if p['appointments'] > 0])
        
        self.summary_label.setText(
            LANGUAGES[self.lang]['messages']['summary']['patients'].format(
                total=total_patients,
                active=active_patients
            )
        )
    
    def calculate_age(self, dob):
        try:
            if isinstance(dob, str):
                dob_date = QDate.fromString(dob, "yyyy-MM-dd")
            else:
                dob_date = QDate(dob.year, dob.month, dob.day)
            return str(QDate.currentDate().year() - dob_date.year())
        except:
            return "N/A"
    
    def generate_doctor_report(self, date_range):
        from_date, to_date = self.get_dates(date_range)
        doctors = self.db.get_all_doctors()
        appointments = self.db.get_all_appointments()
        
        doctor_stats = []
        for doctor in doctors:
            doctor_appointments = []
            for appt in appointments:
                if appt['doctor_id'] == doctor['id']:
                    try:
                        appt_date = appt['date'] if isinstance(appt['date'], str) else appt['date'].strftime("%Y-%m-%d")
                        if (from_date is None or appt_date >= from_date) and \
                           (to_date is None or appt_date <= to_date):
                            doctor_appointments.append(appt)
                    except:
                        continue
            
            completed = len([a for a in doctor_appointments if a['status'] == 'completed'])
            cancelled = len([a for a in doctor_appointments if a['status'] == 'cancelled'])
            
            rate = completed / len(doctor_appointments) * 100 if doctor_appointments else 0
            doctor_stats.append({
                'id': doctor['id'],
                'name': doctor['name'],
                'specialization': doctor['specialization'],
                'appointments': len(doctor_appointments),
                'completed': completed,
                'cancelled': cancelled,
                'completion_rate': f"{rate:.1f}%"
            })
        
        headers = LANGUAGES[self.lang]['table_headers']['doctor']
        self.results_table.setColumnCount(len(headers))
        self.results_table.setHorizontalHeaderLabels(headers)
        self.results_table.setRowCount(len(doctor_stats))
        
        for row_idx, stat in enumerate(doctor_stats):
            items = [
                QTableWidgetItem(str(stat['id'])),
                QTableWidgetItem(stat['name']),
                QTableWidgetItem(stat['specialization']),
                QTableWidgetItem(str(stat['appointments'])),
                QTableWidgetItem(str(stat['completed'])),
                QTableWidgetItem(str(stat['cancelled'])),
                QTableWidgetItem(stat['completion_rate'])
            ]
            
            for col_idx, item in enumerate(items):
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.results_table.setItem(row_idx, col_idx, item)
        
        total_appointments = sum(d['appointments'] for d in doctor_stats)
        avg_completion = sum(float(d['completion_rate'].strip('%')) for d in doctor_stats) / len(doctors) if doctors else 0
        
        self.summary_label.setText(
            LANGUAGES[self.lang]['messages']['summary']['doctors'].format(
                total=total_appointments,
                rate=avg_completion
            )
        )
    
    def generate_appointment_report(self, date_range):
        from_date, to_date = self.get_dates(date_range)
        filters = {}
        if from_date:
            filters['date_from'] = from_date
        if to_date:
            filters['date_to'] = to_date
            
        appointments = self.db.get_appointments_with_details(filters)
        
        headers = LANGUAGES[self.lang]['table_headers']['appointment']
        self.results_table.setColumnCount(len(headers))
        self.results_table.setHorizontalHeaderLabels(headers)
        self.results_table.setRowCount(len(appointments))
        
        for row_idx, appt in enumerate(appointments):
            items = [
                QTableWidgetItem(str(appt['id'])),
                QTableWidgetItem(str(appt.get('date', ''))),
                QTableWidgetItem(str(appt.get('time', ''))),
                QTableWidgetItem(appt['patient_name']),
                QTableWidgetItem(appt['doctor_name']),
                QTableWidgetItem(appt.get('reason', '')),
                QTableWidgetItem(LANGUAGES[self.lang][appt['status']].capitalize()),
                QTableWidgetItem("30 min")
            ]
            
            for col_idx, item in enumerate(items):
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.results_table.setItem(row_idx, col_idx, item)
    
    def generate_prescription_report(self, date_range):
        from_date, to_date = self.get_dates(date_range)
        prescriptions = self.db.get_all_prescriptions()
        
        filtered_prescriptions = []
        for rx in prescriptions:
            try:
                rx_date = rx['date'] if isinstance(rx['date'], str) else rx['date'].strftime("%Y-%m-%d")
                if (from_date is None or rx_date >= from_date) and \
                   (to_date is None or rx_date <= to_date):
                    filtered_prescriptions.append(rx)
            except:
                continue
        
        med_counts = {}
        for p in filtered_prescriptions:
            med = p['medication']
            med_counts[med] = med_counts.get(med, 0) + 1
        
        headers = LANGUAGES[self.lang]['table_headers']['prescription']
        self.results_table.setColumnCount(len(headers))
        self.results_table.setHorizontalHeaderLabels(headers)
        self.results_table.setRowCount(len(filtered_prescriptions))
        
        for row_idx, rx in enumerate(filtered_prescriptions):
            items = [
                QTableWidgetItem(str(rx['id'])),
                QTableWidgetItem(str(rx['date'])),
                QTableWidgetItem(rx['patient_name']),
                QTableWidgetItem(rx['doctor_name']),
                QTableWidgetItem(rx['medication']),
                QTableWidgetItem(rx['dosage']),
                QTableWidgetItem(LANGUAGES[self.lang][rx['status']].capitalize())
            ]
            
            for col_idx, item in enumerate(items):
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.results_table.setItem(row_idx, col_idx, item)
        
        top_meds = sorted(med_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        med_summary = " | ".join(f"{med}: {count}" for med, count in top_meds)
        
        self.summary_label.setText(
            LANGUAGES[self.lang]['messages']['summary']['prescriptions'].format(
                total=len(filtered_prescriptions),
                meds=med_summary
            )
        )
    
    def export_to_csv(self):
        if self.results_table.rowCount() == 0:
            QMessageBox.warning(
                self,
                LANGUAGES[self.lang]['messages']['no_data'].split(':')[0],
                LANGUAGES[self.lang]['messages']['no_data']
            )
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            LANGUAGES[self.lang]['export_button'].replace("to CSV", ""),
            "", 
            "CSV Files (*.csv)"
        )
            
        if not file_path:
            return
            
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write headers
                headers = []
                for col in range(self.results_table.columnCount()):
                    headers.append(self.results_table.horizontalHeaderItem(col).text())
                writer.writerow(headers)
                
                # Write data
                for row in range(self.results_table.rowCount()):
                    row_data = []
                    for col in range(self.results_table.columnCount()):
                        item = self.results_table.item(row, col)
                        row_data.append(item.text() if item else "")
                    writer.writerow(row_data)
                    
            QMessageBox.information(
                self,
                LANGUAGES[self.lang]['messages']['export_success'].split(':')[0],
                LANGUAGES[self.lang]['messages']['export_success'].format(path=file_path)
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                LANGUAGES[self.lang]['messages']['export_failed'].split(':')[0],
                LANGUAGES[self.lang]['messages']['export_failed'].format(error=str(e))
            )