from .doctor.needs import *
from .dashboard import Dashboard

LANGUAGES = {
    'en': {
        # Stats Cards
        'today_appts': "Today's Appointments",
        'active_patients': "Active Patients",
        'monthly_prescriptions': "Prescriptions This Month",
        'avg_consult_time': "Avg. Consultation Time",
        
        # Schedule Table
        'schedule_title': "Today's Schedule",
        'add_appt_btn': "Add Appointment",
        'view_schedule_btn': "View Full Schedule",
        'table_headers': ["Time", "Patient", "Reason", "Status", "Actions"],
        'complete_btn': "Complete",
        'cancel_btn': "Cancel",
        'prescribe_btn': "Prescribe",
        
        # Patient Alerts
        'alerts_title': "Patient Alerts",
        'view_patients_btn': "View All Patients",
        'critical_blood': "Critical Blood Type",
        'expiring_prescription': "Expiring Prescription",
        'followup_needed': "Needs Follow-up",
        'high_risk': "High Risk",
        'attention': "Attention",
        'reminder': "Reminder",
        'view_patient': "View Patient",
        'renew_prescription': "Renew Prescription",
        'schedule_visit': "Schedule Visit",
        
        # Appointment Stats
        'stats_title': "Appointment Statistics",
        'total_appts': "Total Appointments",
        'completed': "Completed",
        'cancelled': "Cancelled",
        'scheduled': "Scheduled",
        
        # Dialogs
        'add_appt_title': "Add New Appointment",
        'patient_label': "Patient:",
        'date_label': "Date:",
        'time_label': "Time:",
        'reason_label': "Reason:",
        'save_btn': "Save",
        'success_title': "Success",
        'appt_added': "Appointment added successfully!",
        'status_updated': "Appointment marked as {}!",
        'error_title': "Error",
        'select_patient': "Please select a valid patient",
        'enter_reason': "Please enter a reason for the appointment",
        'update_failed': "Failed to update appointment",
        
        # Prescription Dialog
        'prescription_title': "Prescription for {}",
        'med_label': "Medication:",
        'dosage_label': "Dosage:",
        'duration_label': "Duration:",
        'instructions_label': "Instructions:",
        'save_prescription': "Save Prescription",
        'fill_fields': "Please fill in all required fields",
        'prescription_saved': "Prescription saved successfully!",
        
        # Patient Report
        'report_title': "Medical Report: {}",
        'medical_history': "Medical History:",
        'no_records': "No medical records found",
        'close_btn': "Close",
        
        # Follow-up
        'followup_title': "Follow-up for {}",
        'schedule_btn': "Schedule",
        'followup_scheduled': "Follow-up appointment scheduled!",

        'patient_not_found': "Patient not found",
        'med_placeholder': "e.g., Amoxicillin 500mg",
        'dosage_placeholder': "e.g., 1 tablet every 8 hours",
        'duration_placeholder': "e.g., 7 days",
        'instructions_placeholder': "Special instructions...",
        'id_label': "ID",
        'dob_label': "Date of Birth",
        'blood_type_label': "Blood Type",
        'insurance_label': "Insurance",
        'none': "None",
        'unknown': "Unknown",
        'diagnosis_label': "Diagnosis",
        'treatment_label': "Treatment",
        'followup_reason': "Follow-up appointment",

        'scheduled': 'Scheduled',
        'canceled': 'Canceled',
        'no_show': 'No-show',
        'completed': 'Completed',
    },
    'ru': {
        # Stats Cards
        'today_appts': "Записи на сегодня",
        'active_patients': "Активные пациенты",
        'monthly_prescriptions': "Рецепты за месяц",
        'avg_consult_time': "Среднее время приема",
        
        # Schedule Table
        'schedule_title': "Расписание на сегодня",
        'add_appt_btn': "Добавить запись",
        'view_schedule_btn': "Полное расписание",
        'table_headers': ["Время", "Пациент", "Причина", "Статус", "Действия"],
        'complete_btn': "Завершить",
        'cancel_btn': "Отменить",
        'prescribe_btn': "Выписать",
        
        # Patient Alerts
        'alerts_title': "Оповещения",
        'view_patients_btn': "Все пациенты",
        'critical_blood': "Критическая группа крови",
        'expiring_prescription': "Истекает рецепт",
        'followup_needed': "Требуется осмотр",
        'high_risk': "Высокий риск",
        'attention': "Внимание",
        'reminder': "Напоминание",
        'view_patient': "Карта пациента",
        'renew_prescription': "Продлить рецепт",
        'schedule_visit': "Записать на прием",
        
        # Appointment Stats
        'stats_title': "Статистика записей",
        'total_appts': "Всего записей",
        'completed': "Завершено",
        'cancelled': "Отменено",
        'scheduled': "Запланировано",
        
        # Dialogs
        'add_appt_title': "Новая запись",
        'patient_label': "Пациент:",
        'date_label': "Дата:",
        'time_label': "Время:",
        'reason_label': "Причина:",
        'save_btn': "Сохранить",
        'success_title': "Успешно",
        'appt_added': "Запись успешно добавлена!",
        'status_updated': "Статус записи изменен на {}!",
        'error_title': "Ошибка",
        'select_patient': "Выберите пациента",
        'enter_reason': "Укажите причину визита",
        'update_failed': "Ошибка обновления записи",
        
        # Prescription Dialog
        'prescription_title': "Рецепт для {}",
        'med_label': "Лекарство:",
        'dosage_label': "Дозировка:",
        'duration_label': "Продолжительность:",
        'instructions_label': "Инструкции:",
        'save_prescription': "Сохранить рецепт",
        'fill_fields': "Заполните все обязательные поля",
        'prescription_saved': "Рецепт сохранен!",
        
        # Patient Report
        'report_title': "Медкарта: {}",
        'medical_history': "История болезни:",
        'no_records': "Записей не найдено",
        'close_btn': "Закрыть",
        
        # Follow-up
        'followup_title': "Повторный осмотр для {}",
        'schedule_btn': "Записать",
        'followup_scheduled': "Повторный осмотр запланирован!",

        'patient_not_found': "Пациент не найден",
        'med_placeholder': "напр., Амоксициллин 500мг",
        'dosage_placeholder': "напр., 1 таблетка каждые 8 часов",
        'duration_placeholder': "напр., 7 дней",
        'instructions_placeholder': "Особые указания...",
        'id_label': "ID",
        'dob_label': "Дата рождения",
        'blood_type_label': "Группа крови",
        'insurance_label': "Страховка",
        'none': "Нет",
        'unknown': "Неизвестно",
        'diagnosis_label': "Диагноз",
        'treatment_label': "Лечение",
        'followup_reason': "Повторный осмотр",

        'scheduled': 'Запланировано',
        'canceled': 'Отменено',
        'no_show': 'Неявка',
        'completed': 'Завершено'
    }
}

class DoctorDashboard(Dashboard):
    def __init__(self, user_data, db, lang='en'):
        self.user_data = user_data
        self.db = db
        self.lang = lang
        self.doctor_id = user_data['id']
        self.today = datetime.now().strftime('%Y-%m-%d')
        super().__init__("doctor", user_data, db) 
        
    def init_ui(self):
        if self.layout():
            QWidget().setLayout(self.layout())
            
        super().init_ui()
        self.load_data()
        self.setup_ui_components()

    def load_data(self):
        """Load all necessary data from database"""
        self.appointments = self.db.get_todays_appointments(self.doctor_id, self.today)
        self.all_appointments = self.db.get_doctor_appointments(self.doctor_id)
        self.patients = self.get_unique_patients()
        self.prescriptions = [p for p in self.db.get_all_prescriptions() 
                             if p['doctor_id'] == self.doctor_id]

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

        active_patients = len(self.patients)
        today_appts = len(self.appointments)
        monthly_prescriptions = len([p for p in self.prescriptions 
                                   if p['date'].strftime('%Y-%m') == self.today[:7]])
        
        stats = [
            (LANGUAGES[self.lang]['today_appts'], str(today_appts), "appointment", "blue"),
            (LANGUAGES[self.lang]['active_patients'], str(active_patients), "user-injured", "green"),
            (LANGUAGES[self.lang]['monthly_prescriptions'], str(monthly_prescriptions), "prescription", "purple"),
            (LANGUAGES[self.lang]['avg_consult_time'], "30 min", "clock", "yellow")
        ]
        
        for title, value, icon, color in stats:
            card = self.create_card(title, value, icon, color)
            cards_layout.addWidget(card)
            
        self.layout.addLayout(cards_layout)

    def setup_schedule_table(self):
        """Setup today's schedule table"""
        content_layout = QHBoxLayout()
        
        schedule_widget = QWidget()
        schedule_widget.setObjectName("card")
        schedule_layout = QVBoxLayout(schedule_widget)

        header = QHBoxLayout()
        schedule_title = QLabel(LANGUAGES[self.lang]['schedule_title'])
        schedule_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        self.add_appt_btn = QPushButton(LANGUAGES[self.lang]['add_appt_btn'])
        self.add_appt_btn.setStyleSheet("""
            background-color: #10b981; 
            color: white;
            padding: 8px;
            border-radius: 4px;
        """)
        self.add_appt_btn.clicked.connect(self.show_add_appointment_dialog)
        
        view_all_btn = QPushButton(LANGUAGES[self.lang]['view_schedule_btn'])
        view_all_btn.setStyleSheet("""
            background-color: #3b82f6; 
            border: none;
            padding: 8px;
        """)
        view_all_btn.clicked.connect(lambda: self.switch_page("schedule"))

        header.addWidget(schedule_title)
        header.addWidget(self.add_appt_btn)
        header.addWidget(view_all_btn)

        self.schedule_table = QTableWidget()
        self.schedule_table.setColumnCount(5)
        self.schedule_table.setHorizontalHeaderLabels(LANGUAGES[self.lang]['table_headers'])
        self.schedule_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.schedule_table.verticalHeader().setVisible(False)
        self.schedule_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        self.update_schedule_table()

        schedule_layout.addLayout(header)
        schedule_layout.addWidget(self.schedule_table)

        alerts_widget = self.create_patient_alerts_widget()
        content_layout.addWidget(schedule_widget, stretch=2)
        content_layout.addWidget(alerts_widget, stretch=1)

        self.layout.addLayout(content_layout)

    def update_schedule_table(self):
        """Update the schedule table with current data"""
        self.schedule_table.setRowCount(len(self.appointments))
        
        for row_idx, appt in enumerate(self.appointments):
            patient = self.db.get_patient_by_id(appt['patient_id'])
            time_str = appt['time'].strftime("%H:%M") if hasattr(appt['time'], 'strftime') else str(appt['time'])

            time_item = QTableWidgetItem(time_str)
            patient_item = QTableWidgetItem(patient['name'] if patient else LANGUAGES[self.lang]['unknown'])
            reason_item = QTableWidgetItem(appt['reason'])
            status_item = QTableWidgetItem(LANGUAGES[self.lang][appt['status']])

            if appt['status'] == 'completed':
                status_item.setForeground(Qt.darkGreen)
            elif appt['status'] == 'scheduled':
                status_item.setForeground(Qt.darkYellow)
            elif appt['status'] == 'cancelled':
                status_item.setForeground(Qt.red)

            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(0, 0, 0, 0)
            action_layout.setSpacing(5)
            
            complete_btn = QPushButton(LANGUAGES[self.lang]['complete_btn'])
            complete_btn.setStyleSheet("""
                background-color: #10b981; 
                color: white; 
                padding: 2px 5px;
                border-radius: 3px;
            """)
            complete_btn.clicked.connect(lambda _, a=appt: self.update_appointment_status(a['id'], 'completed'))

            prescribe_btn = QPushButton(LANGUAGES[self.lang]['prescribe_btn'])
            prescribe_btn.setStyleSheet("""
                background-color: #3b82f6; 
                color: white; 
                padding: 2px 5px;
                border-radius: 3px;
            """)
            prescribe_btn.clicked.connect(lambda _, a=appt: self.show_prescription_dialog(a['patient_id']))

            action_layout.addWidget(complete_btn)
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
        
        alerts_title = QLabel(LANGUAGES[self.lang]['alerts_title'])
        alerts_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        alerts = self.generate_patient_alerts()
        for alert in alerts[:3]:
            alert_widget = QWidget()
            alert_widget.setStyleSheet(f"""
                border-left: 4px solid {alert['color']};
                padding-left: 8px;
                margin-bottom: 8px;
            """)
            
            alert_layout = QVBoxLayout(alert_widget)
            
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
            
            details = QLabel(alert['details'])
            details.setStyleSheet("color: #6b7280; font-size: 12px;")
            
            alert_layout.addLayout(header)
            alert_layout.addWidget(details)
            
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
        
        view_all_btn = QPushButton(LANGUAGES[self.lang]['view_patients_btn'])
        view_all_btn.setStyleSheet("""
            color: #ffffff;
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
        
        for pid, patient in self.patients.items():
            if patient.get('blood_type') in ['O-', 'AB-']:
                alerts.append({
                    'title': LANGUAGES[self.lang]['critical_blood'],
                    'details': f"{patient['name']} ({LANGUAGES[self.lang]['blood_type_label']}: {patient.get('blood_type', LANGUAGES[self.lang]['unknown'])})",
                    'status': LANGUAGES[self.lang]['high_risk'],
                    'color': "red",
                    'action_text': LANGUAGES[self.lang]['view_patient'],
                    'action': lambda _, p=pid: self.view_patient_report(p)
                })
        
        for presc in self.prescriptions:
            if presc['status'] == 'active':
                if (datetime.now().date() - presc['date']).days > 25:
                    patient = self.db.get_patient_by_id(presc['patient_id'])
                    if patient:
                        alerts.append({
                            'title': LANGUAGES[self.lang]['expiring_prescription'],
                            'details': f"{presc['medication']} {LANGUAGES[self.lang]['for']} {patient['name']}",
                            'status': LANGUAGES[self.lang]['attention'],
                            'color': "orange",
                            'action_text': LANGUAGES[self.lang]['renew_prescription'],
                            'action': lambda _, p=presc['patient_id']: self.show_prescription_dialog(p)
                        })
        
        for pid, patient in self.patients.items():
            last_appt = None
            for appt in sorted(self.all_appointments, key=lambda x: x['date'], reverse=True):
                if appt['patient_id'] == pid and appt['status'] == 'completed':
                    last_appt = appt
                    break
            
            if last_appt:
                last_date = last_appt['date']
                if (datetime.now().date() - last_date).days > 180:
                    alerts.append({
                        'title': LANGUAGES[self.lang]['followup_needed'],
                        'details': f"{patient['name']} ({LANGUAGES[self.lang]['last_visit']}: {last_appt['date']})",
                        'status': LANGUAGES[self.lang]['reminder'],
                        'color': "blue",
                        'action_text': LANGUAGES[self.lang]['schedule_visit'],
                        'action': lambda _, p=pid: self.schedule_follow_up(p)
                    })
        
        return alerts

    def setup_appointment_stats(self):
        """Setup appointment statistics section"""
        stats_widget = QWidget()
        stats_widget.setObjectName("chart-container")
        stats_layout = QVBoxLayout(stats_widget)
        
        stats_title = QLabel(LANGUAGES[self.lang]['stats_title'])
        stats_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        completed = len([a for a in self.all_appointments if a['status'] == 'completed'])
        cancelled = len([a for a in self.all_appointments if a['status'] == 'cancelled'])
        scheduled = len([a for a in self.all_appointments if a['status'] == 'scheduled'])
        total = len(self.all_appointments)
        
        stats_html = f"""
        <div style='font-size: 14px; line-height: 1.6;'>
            <p><b>{LANGUAGES[self.lang]['total_appts']}:</b> {total}</p>
            <p><b>{LANGUAGES[self.lang]['completed']}:</b> {completed} ({completed/total*100:.1f}%)</p>
            <p><b>{LANGUAGES[self.lang]['cancelled']}:</b> {cancelled} ({cancelled/total*100:.1f}%)</p>
            <p><b>{LANGUAGES[self.lang]['scheduled']}:</b> {scheduled} ({scheduled/total*100:.1f}%)</p>
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
        dialog.setWindowTitle(LANGUAGES[self.lang]['add_appt_title'])
        dialog.setFixedSize(400, 300)
        
        layout = QVBoxLayout(dialog)
        
        patient_label = QLabel(LANGUAGES[self.lang]['patient_label'])
        self.patient_combo = QComboBox()
        self.patient_combo.addItems([p['name'] for p in self.patients.values()])
        
        date_label = QLabel(LANGUAGES[self.lang]['date_label'])
        self.appt_date = QDateEdit()
        self.appt_date.setDate(QDate.currentDate())
        self.appt_date.setMinimumDate(QDate.currentDate())
        self.appt_date.setCalendarPopup(True)
        
        time_label = QLabel(LANGUAGES[self.lang]['time_label'])
        self.appt_time = QTimeEdit()
        self.appt_time.setTime(QTime(9, 0))
        self.appt_time.setDisplayFormat("hh:mm AP")
        
        reason_label = QLabel(LANGUAGES[self.lang]['reason_label'])
        self.appt_reason = QLineEdit()
        self.appt_reason.setPlaceholderText(LANGUAGES[self.lang]['reason_label'])
        
        button_layout = QHBoxLayout()
        save_btn = QPushButton(LANGUAGES[self.lang]['save_btn'])
        save_btn.setStyleSheet("background-color: #10b981; color: white;")
        save_btn.clicked.connect(lambda: self.save_appointment(dialog))
        
        cancel_btn = QPushButton(LANGUAGES[self.lang]['cancel_btn'])
        cancel_btn.setStyleSheet("background-color: #ef4444; color: white;")
        cancel_btn.clicked.connect(dialog.reject)
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        
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
            QMessageBox.warning(self, LANGUAGES[self.lang]['error_title'], 
                              LANGUAGES[self.lang]['select_patient'])
            return
            
        if not self.appt_reason.text():
            QMessageBox.warning(self, LANGUAGES[self.lang]['error_title'], 
                              LANGUAGES[self.lang]['enter_reason'])
            return
            
        appointment = {
            "patient_id": patient_id,
            "doctor_id": self.doctor_id,
            "date": self.appt_date.date().toString("yyyy-MM-dd"),
            "time": self.appt_time.time().toString("hh:mm"),
            "reason": self.appt_reason.text(),
            "status": "scheduled"
        }
        
        self.db.add_appointment(appointment)
        QMessageBox.information(self, LANGUAGES[self.lang]['success_title'], 
                              LANGUAGES[self.lang]['appt_added'])
        
        self.load_data()
        self.update_schedule_table()
        dialog.accept()

    def update_appointment_status(self, appointment_id, status):
        """Update appointment status in database"""
        if self.db.update_appointment_status(appointment_id, status):
            QMessageBox.information(self, LANGUAGES[self.lang]['success_title'], 
                                  LANGUAGES[self.lang]['status_updated'].format(status))
            self.load_data()
            self.update_schedule_table()
        else:
            QMessageBox.warning(self, LANGUAGES[self.lang]['error_title'], 
                              LANGUAGES[self.lang]['update_failed'])
        
    def show_prescription_dialog(self, patient_id):
        """Show dialog to write prescription"""
        patient = self.db.get_patient_by_id(patient_id)
        if not patient:
            QMessageBox.warning(self, 
                              LANGUAGES[self.lang]['error_title'], 
                              LANGUAGES[self.lang]['patient_not_found'])
            return
            
        dialog = QDialog(self)
        dialog.setWindowTitle(LANGUAGES[self.lang]['prescription_title'].format(patient['name']))
        dialog.setFixedSize(500, 400)
        
        layout = QVBoxLayout(dialog)
        
        med_label = QLabel(LANGUAGES[self.lang]['med_label'])
        self.med_input = QLineEdit()
        self.med_input.setPlaceholderText(LANGUAGES[self.lang]['med_placeholder'])
        
        dosage_label = QLabel(LANGUAGES[self.lang]['dosage_label'])
        self.dosage_input = QLineEdit()
        self.dosage_input.setPlaceholderText(LANGUAGES[self.lang]['dosage_placeholder'])
        
        duration_label = QLabel(LANGUAGES[self.lang]['duration_label'])
        self.duration_input = QLineEdit()
        self.duration_input.setPlaceholderText(LANGUAGES[self.lang]['duration_placeholder'])
        
        instructions_label = QLabel(LANGUAGES[self.lang]['instructions_label'])
        self.instructions_input = QTextEdit()
        self.instructions_input.setPlaceholderText(LANGUAGES[self.lang]['instructions_placeholder'])
        self.instructions_input.setMaximumHeight(80)
        
        button_layout = QHBoxLayout()
        save_btn = QPushButton(LANGUAGES[self.lang]['save_prescription'])
        save_btn.setStyleSheet("background-color: #10b981; color: white;")
        save_btn.clicked.connect(lambda: self.save_prescription(dialog, patient_id))
        
        cancel_btn = QPushButton(LANGUAGES[self.lang]['cancel_btn'])
        cancel_btn.setStyleSheet("background-color: #ef4444; color: white;")
        cancel_btn.clicked.connect(dialog.reject)
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        
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
            QMessageBox.warning(self, 
                              LANGUAGES[self.lang]['error_title'], 
                              LANGUAGES[self.lang]['fill_fields'])
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
        QMessageBox.information(self, 
                              LANGUAGES[self.lang]['success_title'], 
                              LANGUAGES[self.lang]['prescription_saved'])
        dialog.accept()

    def view_patient_report(self, patient_id):
        """View patient medical report"""
        patient = self.db.get_patient_by_id(patient_id)
        if not patient:
            QMessageBox.warning(self, 
                              LANGUAGES[self.lang]['error_title'], 
                              LANGUAGES[self.lang]['patient_not_found'])
            return
            
        dialog = QDialog(self)
        dialog.setWindowTitle(LANGUAGES[self.lang]['report_title'].format(patient['name']))
        dialog.setFixedSize(600, 500)
        
        layout = QVBoxLayout(dialog)
        
        info_html = f"""
        <h3>{patient['name']}</h3>
        <p><b>{LANGUAGES[self.lang]['id_label']}:</b> {patient['id']}</p>
        <p><b>{LANGUAGES[self.lang]['dob_label']}:</b> {patient.get('date_of_birth', LANGUAGES[self.lang]['unknown'])}</p>
        <p><b>{LANGUAGES[self.lang]['blood_type_label']}:</b> {patient.get('blood_type', LANGUAGES[self.lang]['unknown'])}</p>
        <p><b>{LANGUAGES[self.lang]['insurance_label']}:</b> {patient.get('insurance', LANGUAGES[self.lang]['none'])}</p>
        """
        
        info_label = QLabel(info_html)
        info_label.setTextFormat(Qt.RichText)
        
        records_label = QLabel(LANGUAGES[self.lang]['medical_history'])
        records_text = QTextEdit()
        records_text.setReadOnly(True)
        
        records = self.db.get_patient_medical_records(patient_id)
        if records:
            records_html = "<ul>"
            for record in sorted(records, key=lambda x: x['date'], reverse=True):
                doctor = self.db.get_doctor_by_id(record['doctor_id'])
                records_html += f"""
                <li>
                    <b>{record['date']}</b> - {doctor['name'] if doctor else LANGUAGES[self.lang]['unknown']}<br>
                    <b>{LANGUAGES[self.lang]['diagnosis_label']}:</b> {record['diagnosis']}<br>
                    <b>{LANGUAGES[self.lang]['treatment_label']}:</b> {record['treatment']}
                </li>
                """
            records_html += "</ul>"
        else:
            records_html = f"<p>{LANGUAGES[self.lang]['no_records']}</p>"
            
        records_text.setHtml(records_html)
        
        close_btn = QPushButton(LANGUAGES[self.lang]['close_btn'])
        close_btn.clicked.connect(dialog.accept)
        
        layout.addWidget(info_label)
        layout.addWidget(records_label)
        layout.addWidget(records_text)
        layout.addWidget(close_btn)
        
        dialog.exec_()

    def schedule_follow_up(self, patient_id):
        """Schedule follow-up appointment"""
        patient = self.db.get_patient_by_id(patient_id)
        if not patient:
            QMessageBox.warning(self, 
                              LANGUAGES[self.lang]['error_title'], 
                              LANGUAGES[self.lang]['patient_not_found'])
            return
            
        dialog = QDialog(self)
        dialog.setWindowTitle(LANGUAGES[self.lang]['followup_title'].format(patient['name']))
        dialog.setFixedSize(400, 300)
        
        layout = QVBoxLayout(dialog)
        
        date_label = QLabel(LANGUAGES[self.lang]['date_label'])
        follow_up_date = QDateEdit()
        follow_up_date.setDate(QDate.currentDate().addDays(7))
        follow_up_date.setMinimumDate(QDate.currentDate())
        
        time_label = QLabel(LANGUAGES[self.lang]['time_label'])
        follow_up_time = QTimeEdit()
        follow_up_time.setTime(QTime(9, 0))
        
        reason_label = QLabel(LANGUAGES[self.lang]['reason_label'])
        follow_up_reason = QLineEdit()
        follow_up_reason.setText(LANGUAGES[self.lang]['followup_reason'])
        
        button_layout = QHBoxLayout()
        save_btn = QPushButton(LANGUAGES[self.lang]['schedule_btn'])
        save_btn.setStyleSheet("background-color: #10b981; color: white;")
        save_btn.clicked.connect(lambda: self.save_follow_up(
            dialog, patient_id, follow_up_date, follow_up_time, follow_up_reason
        ))
        
        cancel_btn = QPushButton(LANGUAGES[self.lang]['cancel_btn'])
        cancel_btn.setStyleSheet("background-color: #ef4444; color: white;")
        cancel_btn.clicked.connect(dialog.reject)
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        
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
            "status": "scheduled"
        }
        
        self.db.add_appointment(appointment)
        QMessageBox.information(self, 
                              LANGUAGES[self.lang]['success_title'], 
                              LANGUAGES[self.lang]['followup_scheduled'])
        
        self.load_data()
        self.update_schedule_table()
        dialog.accept()

