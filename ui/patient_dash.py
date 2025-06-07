from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QTableWidget, QTableWidgetItem, QPushButton,
                            QTextEdit, QMessageBox, QHeaderView, QDialog)
from PyQt5.QtCore import Qt
from .dashboard import Dashboard
from .patient import BookAppointmentDialog
from datetime import datetime


LANGUAGES = {
    'en': {
        'stats_upcoming': 'Upcoming Appointments',
        'stats_prescriptions': 'Active Prescriptions',
        'stats_records': 'Medical Records',
        'stats_bills': 'Pending Bills',
        'appointments_title': 'Upcoming Appointments',
        'book_appt_btn': 'Book Appointment',
        'view_all_btn': 'View All',
        'appt_table_headers': ["Date", "Time", "Doctor", "Department", "Status"],
        'prescriptions_title': 'Recent Prescriptions',
        'prescribed_by': 'Prescribed by Dr. {} on {}',
        'dosage_label': '<b>Dosage:</b> {}',
        'instructions_label': '<b>Instructions:</b> {}',
        'refill_btn': 'Request Refill',
        'view_all_presc_btn': 'View All Prescriptions',
        'health_title': 'Health Summary',
        'recent_history': '<h3>Recent Medical History</h3><ul>',
        'diagnosis_label': '<b>Diagnosis:</b> {}',
        'treatment_label': '<b>Treatment:</b> {}',
        'no_records': '<p>No medical records found</p>',
        'vital_stats': '<h3>Vital Statistics</h3>',
        'blood_pressure': '<b>Blood Pressure:</b>',
        'heart_rate': '<b>Heart Rate:</b>',
        'blood_type': '<b>Blood Type:</b>',
        'last_checkup': '<b>Last Checkup:</b>',
        'view_records_btn': 'View Full Medical Records',
        'refill_confirm_title': 'Confirm Refill Request',
        'refill_confirm_text': 'Request refill for:\n\nMedication: {}\nDosage: {}\n\nThis request will be sent to your doctor for approval.',
        'refill_success_title': 'Request Sent',
        'refill_success_text': 'Your refill request has been sent to your doctor.\nYou will be notified when it\'s approved.',

        'scheduled': 'Scheduled',
        'canceled': 'Canceled',
        'no_show': 'No-show',
        'completed': 'Completed'
    },
    'ru': {
        'stats_upcoming': 'Предстоящие приемы',
        'stats_prescriptions': 'Активные рецепты',
        'stats_records': 'Медицинские записи',
        'stats_bills': 'Ожидающие счета',
        'appointments_title': 'Предстоящие приемы',
        'book_appt_btn': 'Записаться на прием',
        'view_all_btn': 'Просмотреть все',
        'appt_table_headers': ["Дата", "Время", "Врач", "Отделение", "Статус"],
        'prescriptions_title': 'Последние рецепты',
        'prescribed_by': 'Выписал(а) доктор {} от {}',
        'dosage_label': '<b>Дозировка:</b> {}',
        'instructions_label': '<b>Инструкции:</b> {}',
        'refill_btn': 'Запросить повторный',
        'view_all_presc_btn': 'Все рецепты',
        'health_title': 'Медицинская сводка',
        'recent_history': '<h3>Недавняя история</h3><ul>',
        'diagnosis_label': '<b>Диагноз:</b> {}',
        'treatment_label': '<b>Лечение:</b> {}',
        'no_records': '<p>Медицинских записей не найдено</p>',
        'vital_stats': '<h3>Основные показатели</h3>',
        'blood_pressure': '<b>Давление:</b>',
        'heart_rate': '<b>Пульс:</b>',
        'blood_type': '<b>Группа крови:</b>',
        'last_checkup': '<b>Последний осмотр:</b>',
        'view_records_btn': 'Полные медицинские записи',
        'refill_confirm_title': 'Подтверждение запроса',
        'refill_confirm_text': 'Запросить повторный рецепт:\n\nПрепарат: {}\nДозировка: {}\n\nЗапрос будет отправлен вашему врачу на подтверждение.',
        'refill_success_title': 'Запрос отправлен',
        'refill_success_text': 'Ваш запрос на повторный рецепт отправлен врачу.\nВы получите уведомление, когда он будет подтвержден.',
        'scheduled': 'Запланировано',
        'canceled': 'Отменено',
        'no_show': 'Неявка',
        'completed': 'Завершено'
    }
}


class PatientDashboard(Dashboard):
    def __init__(self, user_data, db, lang='en'):
        super().__init__("patient", user_data, db, lang)
        # self.lang = lang
        
    def init_ui(self):
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
            (LANGUAGES[self.lang]['stats_upcoming'], 
             str(len([a for a in self.appointments if a['status'] != 'completed'])), 
             "appointment", "blue"),
            (LANGUAGES[self.lang]['stats_prescriptions'], 
             str(len([p for p in self.prescriptions if p['status'] == 'active'])), 
             "prescription", "green"),
            (LANGUAGES[self.lang]['stats_records'], 
             str(len(self.medical_records)), 
             "file-medical", "purple"),
            (LANGUAGES[self.lang]['stats_bills'], 
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
        
        appointments_widget = QWidget()
        appointments_widget.setObjectName("card")
        appointments_layout = QVBoxLayout(appointments_widget)
        
        header_widget = QWidget()
        header = QHBoxLayout(header_widget)
        appointments_title = QLabel(LANGUAGES[self.lang]['appointments_title'])
        appointments_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        self.book_appt_btn = QPushButton(LANGUAGES[self.lang]['book_appt_btn'])
        self.book_appt_btn.setStyleSheet("background-color: #10b981; color: white;")
        self.book_appt_btn.clicked.connect(self.show_book_appointment_dialog)
        
        header.addWidget(appointments_title)
        header.addWidget(self.book_appt_btn)
        
        # Table setup
        self.appointments_table = QTableWidget()
        self.appointments_table.setColumnCount(5)
        self.appointments_table.setHorizontalHeaderLabels(LANGUAGES[self.lang]['appt_table_headers'])
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
        try:
            appointments = self.db.get_patient_appointments(self.user_data['id'])
            upcoming_appts = [appt for appt in appointments 
                            if appt['status'] == 'scheduled' and 
                            appt['date'] >= datetime.now().date()]
            
            self.appointments_table.setRowCount(len(upcoming_appts))
            
            for row, appt in enumerate(upcoming_appts):
                date_str = appt['date'].strftime("%Y-%m-%d") if hasattr(appt['date'], 'strftime') else str(appt['date'])
                time_str = appt['time'].strftime("%H:%M") if hasattr(appt['time'], 'strftime') else str(appt['time'])
                
                self.appointments_table.setItem(row, 0, QTableWidgetItem(date_str))
                self.appointments_table.setItem(row, 1, QTableWidgetItem(time_str))
                self.appointments_table.setItem(row, 2, QTableWidgetItem(appt['reason']))
                self.appointments_table.setItem(row, 3, QTableWidgetItem(LANGUAGES[self.lang][appt['status']]))
                
                doctor = self.db.get_doctor_by_id(appt['doctor_id'])
                doctor_name = doctor['name'] if doctor else "Unknown"
                self.appointments_table.setItem(row, 4, QTableWidgetItem(doctor_name))
                
        except Exception as e:
            print(f"Error updating appointments table: {e}")
            QMessageBox.warning(self, "Error", f"Failed to load appointments: {str(e)}")

    def create_prescriptions_widget(self):
        """Create the prescriptions widget"""
        prescriptions_widget = QWidget()
        prescriptions_widget.setObjectName("card")
        prescriptions_layout = QVBoxLayout(prescriptions_widget)
        
        prescriptions_title = QLabel(LANGUAGES[self.lang]['prescriptions_title'])
        prescriptions_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        active_prescriptions = sorted(
            [p for p in self.prescriptions if p['status'] == 'active'],
            key=lambda x: x['date'],
            reverse=True
        )[:3]
        
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
            
            header_widget = QWidget()
            header = QHBoxLayout(header_widget)
            name = QLabel(presc['medication'])
            name.setStyleSheet("font-weight: bold;")
            
            status_label = QLabel(presc['status'].capitalize())
            status_label.setStyleSheet(f"""
                background-color: {color}80;
                color: white;
                padding: 2px 4px;
                border-radius: 4px;
                font-size: 12px;
            """)
            
            header.addWidget(name)
            header.addWidget(status_label)
            
            date_str = presc['date'].strftime("%Y-%m-%d") if hasattr(presc['date'], 'strftime') else str(presc['date'])
            details = QLabel(LANGUAGES[self.lang]['prescribed_by'].format(
                doctor['name'] if doctor else "Unknown", 
                date_str
            ))
            details.setStyleSheet("color: #6b7280; font-size: 12px;")
            
            dosage = QLabel(LANGUAGES[self.lang]['dosage_label'].format(presc['dosage']))
            dosage.setTextFormat(Qt.RichText)
            
            instructions = QLabel(LANGUAGES[self.lang]['instructions_label'].format(presc.get('instructions', 'None')))
            instructions.setTextFormat(Qt.RichText)
            instructions.setWordWrap(True)
            
            # refill_btn = QPushButton(LANGUAGES[self.lang]['refill_btn'])
            # refill_btn.setStyleSheet("""
            #     background-color: #3b82f6;
            #     border: none;
            #     text-align: left;
            #     padding: 0;
            # """)
            # refill_btn.clicked.connect(lambda _, p=presc: self.request_prescription_refill(p['id']))
            
            pres_layout.addWidget(header_widget)
            pres_layout.addWidget(details)
            pres_layout.addWidget(dosage)
            pres_layout.addWidget(instructions)
            # pres_layout.addWidget(refill_btn)
            
            prescriptions_layout.addWidget(prescription)
            
        view_all_btn = QPushButton(LANGUAGES[self.lang]['view_all_presc_btn'])
        # view_all_btn.setStyleSheet("background-color: #ffffff; text-decoration: underline;")
        view_all_btn.clicked.connect(lambda: self.switch_page("prescriptions"))
        
        prescriptions_layout.addWidget(prescriptions_title)
        prescriptions_layout.addSpacing(10)
        prescriptions_layout.addWidget(view_all_btn, alignment=Qt.AlignRight)
        
        return prescriptions_widget
        
    def setup_health_summary(self):
        """Setup health summary section"""
        health_widget = QWidget()
        health_widget.setObjectName("chart-container")
        health_layout = QVBoxLayout(health_widget)
        
        health_title = QLabel(LANGUAGES[self.lang]['health_title'])
        health_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        summary_text = QTextEdit()
        summary_text.setReadOnly(True)
        
        if self.medical_records:
            summary_html = LANGUAGES[self.lang]['recent_history']
            for record in sorted(self.medical_records, 
                               key=lambda x: x['date'], 
                               reverse=True)[:3]:
                doctor = self.db.get_doctor_by_id(record['doctor_id'])
                date_str = record['date'].strftime("%Y-%m-%d") if hasattr(record['date'], 'strftime') else str(record['date'])
                summary_html += f"""
                <li>
                    <b>{date_str}</b> - {doctor['name'] if doctor else 'Unknown'}<br>
                    {LANGUAGES[self.lang]['diagnosis_label'].format(record['diagnosis'])}<br>
                    {LANGUAGES[self.lang]['treatment_label'].format(record['treatment'])}
                </li>
                """
            summary_html += "</ul>"
        else:
            summary_html = LANGUAGES[self.lang]['no_records']
            
        summary_html += LANGUAGES[self.lang]['vital_stats']
        summary_html += """
        <table border='0' cellspacing='10'>
            <tr><td>{blood_pressure}</td><td>120/80 mmHg</td></tr>
            <tr><td>{heart_rate}</td><td>72 bpm</td></tr>
            <tr><td>{blood_type}</td><td>{blood_type_value}</td></tr>
            <tr><td>{last_checkup}</td><td>{last_checkup_value}</td></tr>
        </table>
        """.format(
            blood_pressure=LANGUAGES[self.lang]['blood_pressure'],
            heart_rate=LANGUAGES[self.lang]['heart_rate'],
            blood_type=LANGUAGES[self.lang]['blood_type'],
            blood_type_value=self.user_data.get('blood_type', 'Unknown'),
            last_checkup=LANGUAGES[self.lang]['last_checkup'],
            last_checkup_value=max([r['date'].strftime("%Y-%m-%d") if hasattr(r['date'], 'strftime') else str(r['date']) 
                                  for r in self.medical_records], default="Never")
        )
        
        summary_text.setHtml(summary_html)
        
        view_records_btn = QPushButton(LANGUAGES[self.lang]['view_records_btn'])
        view_records_btn.setStyleSheet("background-color: #ffffff; text-decoration: underline;")
        view_records_btn.clicked.connect(lambda: self.switch_page("medical-records"))
        
        health_layout.addWidget(health_title)
        health_layout.addWidget(summary_text)
        health_layout.addWidget(view_records_btn, alignment=Qt.AlignRight)
        
        self.layout.addWidget(health_widget)
        
    def show_book_appointment_dialog(self):
        """Show dialog to book new appointment"""
        dialog = BookAppointmentDialog(self.user_data, self.db, self.lang)
        if dialog.exec_() == QDialog.Accepted:
            self.load_data()
            self.update_appointments_table()
            dialog.close()
            self.update_appointments_table()
        
    def request_prescription_refill(self, prescription_id):
        """Request refill for a prescription"""
        prescription = next((p for p in self.prescriptions if p['id'] == prescription_id), None)
        if not prescription:
            QMessageBox.warning(self, "Error", "Prescription not found")
            return
            
        reply = QMessageBox.question(
            self, LANGUAGES[self.lang]['refill_confirm_title'],
            LANGUAGES[self.lang]['refill_confirm_text'].format(
                prescription['medication'],
                prescription['dosage']
            ),
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            QMessageBox.information(
                self, 
                LANGUAGES[self.lang]['refill_success_title'],
                LANGUAGES[self.lang]['refill_success_text']
            )

        