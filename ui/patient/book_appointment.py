
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QScrollArea, QWidget, QGroupBox, 
                            QFormLayout, QComboBox, QTextEdit, QDateEdit, QLabel, 
                            QPushButton, QHBoxLayout, QMessageBox)
from PyQt5.QtCore import Qt, QDate
from .needs import *
from datetime import datetime, timedelta

LANGUAGES = {
    'en': {
        'window_title': 'Book New Appointment',
        'select_doctor_group': 'Select Doctor',
        'filter_department': 'Filter by Department:',
        'all_departments': 'All Departments',
        'select_doctor': 'Select Doctor:',
        'doctor_info': 'Doctor Information:',
        'appt_datetime_group': 'Appointment Date & Time',
        'date_label': 'Date:',
        'time_label': 'Time:',
        'available_slots': 'Available time slots will appear here',
        'appt_details_group': 'Appointment Details',
        'reason_placeholder': 'Please describe the reason for your appointment...',
        'cancel_btn': 'Cancel',
        'book_btn': 'Book Appointment',
        'error_select_doctor': 'Please select a doctor',
        'error_reason': 'Please provide a reason for the appointment',
        'success_title': 'Appointment Booked',
        'success_message': 'Your appointment has been successfully booked!\n\nDoctor: Dr. {}\nDate: {}\nTime: {}',
        'error_title': 'Booking Failed',
        'error_message': 'Failed to book appointment:\n{}',
        'doctor_info_template': """
            <b>Name:</b> Dr. {}<br>
            <b>Department:</b> {}<br>
            <b>Specialization:</b> {}<br>
            <b>Contact:</b> {}<br>
            <b>Availability:</b> {}
        """,
        'loading_slots': 'Loading available time slots...',
        'slots_available': 'available time slots',
        'no_slots_available': 'No available time slots for the selected date.',
        'chose_doctor_first': 'Choose doctor first',
        'doctor_not_found': "Doctor not found",
        'error_loading_slots': 'Error loading slots',
    },
    'ru': {
        'window_title': 'Запись на прием',
        'select_doctor_group': 'Выбор врача',
        'filter_department': 'Отделение:',
        'all_departments': 'Все отделения',
        'select_doctor': 'Выберите врача:',
        'doctor_info': 'Информация о враче:',
        'appt_datetime_group': 'Дата и время приема',
        'date_label': 'Дата:',
        'time_label': 'Время:',
        'available_slots': 'Доступное время появится здесь',
        'appt_details_group': 'Детали приема',
        'reason_placeholder': 'Опишите причину визита...',
        'cancel_btn': 'Отмена',
        'book_btn': 'Записаться',
        'error_select_doctor': 'Пожалуйста, выберите врача',
        'error_reason': 'Пожалуйста, укажите причину визита',
        'success_title': 'Запись оформлена',
        'success_message': 'Вы успешно записаны на прием!\n\nВрач: Доктор {}\nДата: {}\nВремя: {}',
        'error_title': 'Ошибка записи',
        'error_message': 'Ошибка при записи:\n{}',
        'doctor_info_template': """
            <b>Имя:</b> Доктор {}<br>
            <b>Отделение:</b> {}<br>
            <b>Специализация:</b> {}<br>
            <b>Контакты:</b> {}<br>
            <b>График работы:</b> {}
        """,
        'loading_slots': 'Загрузка доступных временных слотов...',
        'slots_available': 'доступных временных слотов',
        'no_slots_available': 'Нет доступного времени на выбранную дату.',
        'chose_doctor_first': "Сначала выберите врача",
        'doctor_not_found': "Врач не найден",
        'error_loading_slots': "Ошибка загрузки слотов"
    }
}

class BookAppointmentDialog(QDialog):
    def __init__(self, user_data, db, lang='en', parent=None):
        super().__init__(parent=None)
        self.user_data = user_data
        self.db = db
        self.lang = lang if lang in LANGUAGES else 'en'
        self.doctors = self.db.get_all_doctors()
        self.setup_ui()
        
    def tr(self, text_key):
        """Helper method to get translated text"""
        return LANGUAGES[self.lang].get(text_key, text_key)
     
    def setup_ui(self):
        self.setWindowTitle(self.tr('window_title'))
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
        group = QGroupBox(self.tr('select_doctor_group'))
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
        self.dept_filter.addItem(self.tr('all_departments'), "all")
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
        
        form.addRow(self.tr('filter_department'), self.dept_filter)
        form.addRow(self.tr('select_doctor'), self.doctor_combo)
        form.addRow(self.tr('doctor_info'), self.doctor_info)
        
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
            
        info = self.tr('doctor_info_template').format(
            doctor['name'],
            doctor['department'],
            doctor['specialization'],
            doctor.get('email', 'N/A'),
            doctor.get('availability', 'Mon-Fri, 9AM-5PM')
        )
        self.doctor_info.setHtml(info)

    def setup_date_time(self):
        """Setup date and time selection components"""
        group = QGroupBox(self.tr('appt_datetime_group'))
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
        
        # Time selection ComboBox
        self.time_combo = QComboBox()
        self.time_combo.setStyleSheet("padding: 5px;")
        
        # Available slots label
        self.available_slots = QLabel(self.tr('loading_slots'))
        self.available_slots.setWordWrap(True)

        # Connect signals
        self.appt_date.dateChanged.connect(self.update_available_times)
        self.doctor_combo.currentIndexChanged.connect(self.update_available_times)

        form.addRow(self.tr('date_label'), self.appt_date)
        form.addRow(self.tr('time_label'), self.time_combo)
        form.addRow(self.tr('available_slots'), self.available_slots)
        
        group.setLayout(form)
        self.layout.addWidget(group)

        self.update_available_times()

    def update_available_times(self):
        """Update available time slots based on selected doctor's working hours"""
        try:
            self.time_combo.clear()
            self.available_slots.setText(self.tr('loading_slots'))
            QApplication.processEvents()  # Force UI update
            
            doctor_id = self.doctor_combo.currentData()
            selected_date = self.appt_date.date().toPyDate()
            current_datetime = datetime.now()
            is_today = selected_date == current_datetime.date()
            
            if not doctor_id:
                self.time_combo.addItem(self.tr("chose_doctor_first"))
                self.available_slots.setText("")
                return

            doctor = self.db.get_doctor_by_id(doctor_id)
            if not doctor:
                raise ValueError(self.tr('doctor_not_found'))
                
            from_time = doctor['from_time']
            until_time = doctor['until_time']
            
            if isinstance(from_time, str):
                from_time = datetime.strptime(from_time, "%H:%M:%S").time()
            if isinstance(until_time, str):
                until_time = datetime.strptime(until_time, "%H:%M:%S").time()
            
            booked_times = self.db.get_booked_times(
                doctor_id, 
                selected_date.strftime("%Y-%m-%d")
            )
            
            available_slots = []
            current_time = datetime.combine(selected_date, from_time)
            end_time = datetime.combine(selected_date, until_time)
            
            # If today, start from current time + 30 minutes (rounded up)
            if is_today:
                # Round up to next 30 minute interval
                minutes_to_add = (30 - (current_datetime.minute % 30)) % 30
                if minutes_to_add == 0:
                    minutes_to_add = 30  # If exactly on the half hour, go to next
                current_time = current_datetime + timedelta(minutes=minutes_to_add)
                current_time = current_time.replace(second=0, microsecond=0)
                # Make sure we don't start before doctor's working hours
                if current_time.time() < from_time:
                    current_time = datetime.combine(selected_date, from_time)
            
            while current_time < end_time:
                time_str = current_time.time().strftime("%H:%M")
                if time_str not in booked_times:
                    display_time = current_time.strftime("%I:%M %p")
                    available_slots.append((display_time, time_str))
                current_time += timedelta(minutes=30)
            
            self.time_combo.clear()
            if available_slots:
                for display_time, time_value in available_slots:
                    self.time_combo.addItem(display_time, time_value)
                self.available_slots.setText(
                    f"{len(available_slots)} {self.tr('slots_available')}"
                )
            else:
                self.time_combo.addItem(self.tr('no_slots_available'))
                self.available_slots.setText("")
                
        except Exception as e:
            print(f"Error updating time slots: {str(e)}")
            self.time_combo.clear()
            self.time_combo.addItem(self.tr('error_loading_slots'))
            self.available_slots.setText(f"Error: {str(e)}")

    def setup_reason(self):
        """Setup appointment reason input"""
        group = QGroupBox(self.tr('appt_details_group'))
        group.setStyleSheet(group.styleSheet())
        
        layout = QVBoxLayout()
        
        self.appt_reason = QTextEdit()
        self.appt_reason.setPlaceholderText(self.tr('reason_placeholder'))
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
        cancel_btn = QPushButton(self.tr('cancel_btn'))
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
        book_btn = QPushButton(self.tr('book_btn'))
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
            QMessageBox.warning(
                self, 
                self.tr('error_title'), 
                self.tr('error_select_doctor')
            )
            return
            
        if not self.appt_reason.toPlainText().strip():
            QMessageBox.warning(
                self, 
                self.tr('error_title'), 
                self.tr('error_reason')
            )
            return
            
        # Prepare appointment data
        appointment = {
            "patient_id": self.user_data['id'],
            "doctor_id": self.doctor_combo.currentData(),
            "date": self.appt_date.date().toString("yyyy-MM-dd"),
            "time": self.time_combo.currentText(),
            "reason": self.appt_reason.toPlainText(),
            "status": "scheduled",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        try:
            # Save to database
            self.db.add_appointment(appointment)
            
            # Show success message
            doctor_name = next(d['name'] for d in self.doctors if d['id'] == appointment['doctor_id'])
            QMessageBox.information(
                self, 
                self.tr('success_title'), 
                self.tr('success_message').format(
                    doctor_name,
                    appointment['date'],
                    appointment['time']
                )
            )
            
            # Close dialog with success
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(
                self,
                self.tr('error_title'),
                self.tr('error_message').format(str(e))
            )