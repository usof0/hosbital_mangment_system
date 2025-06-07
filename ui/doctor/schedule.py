from .needs import *

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QHeaderView, QPushButton, QDateEdit
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QColor
import datetime as dt

LANGUAGES = {
    'en': {
        'page_title': 'My Schedule',
        'select_date': 'Select Date:',
        'refresh_button': 'Refresh',
        'table_headers': ['Time', 'Patient', 'Reason', 'Status'],
        'status': {
            'scheduled': 'Scheduled',
            'canceled': 'Canceled',
            'no_show': 'No-show',
            'completed': 'Completed'
        },
        'unknown_patient': 'Unknown'
    },
    'ru': {
        'page_title': 'Мое расписание',
        'select_date': 'Выберите дату:',
        'refresh_button': 'Обновить',
        'table_headers': ['Время', 'Пациент', 'Причина', 'Статус'],
        'status': {
            'scheduled': 'Запланировано',
            'canceled': 'Отменено',
            'no_show': 'Не явился',
            'completed': 'Завершено'
        },
        'unknown_patient': 'Неизвестно'
    }
}

class DoctorSchedulePage(QWidget):
    def __init__(self, user_data, db, lang='en'):
        super().__init__()
        self.user_data = user_data
        self.db = db
        self.lang = lang
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Page title
        title = QLabel(LANGUAGES[self.lang]['page_title'])
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 15px;")
        layout.addWidget(title)
        
        # Date selector
        date_layout = QHBoxLayout()
        date_layout.addWidget(QLabel(LANGUAGES[self.lang]['select_date']))
        
        self.date_edit = QDateEdit(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDisplayFormat("yyyy-MM-dd")
        date_layout.addWidget(self.date_edit)
        
        refresh_btn = QPushButton(LANGUAGES[self.lang]['refresh_button'])
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: white;
                padding: 6px 12px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
        """)
        refresh_btn.clicked.connect(self.load_appointments)
        date_layout.addWidget(refresh_btn)
        
        layout.addLayout(date_layout)
        
        # Appointments table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(LANGUAGES[self.lang]['table_headers'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        
        layout.addWidget(self.table)
        self.load_appointments()
        
    def load_appointments(self):
        qdate = self.date_edit.date()
        year = qdate.year()
        month = qdate.month()
        day = qdate.day()

        try:
            selected_date = dt.date(year, month, day)
        except ValueError as e:
            print(f"Invalid date: {e}")
            return

        all_appointments = self.db.get_doctor_appointments(self.user_data['id'])
        appointments = []

        for appt in all_appointments:
            # Handle different date formats (datetime.date vs string)
            appt_date = appt['date']
            if isinstance(appt_date, str):
                try:
                    appt_date = dt.datetime.strptime(appt_date, "%Y-%m-%d").date()
                except ValueError:
                    continue
                    
            if appt_date == selected_date:
                appointments.append(appt)

        self.table.setRowCount(len(appointments))
        
        for row, appt in enumerate(appointments):
            patient = self.db.get_patient_by_id(appt['patient_id'])
            
            # Time column
            time_str = appt.get('time', '')
            if isinstance(time_str, dt.time):
                time_str = time_str.strftime("%H:%M")
            self.table.setItem(row, 0, QTableWidgetItem(time_str))
            
            # Patient column
            patient_name = patient['name'] if patient else LANGUAGES[self.lang]['unknown_patient']
            self.table.setItem(row, 1, QTableWidgetItem(patient_name))
            
            # Reason column
            self.table.setItem(row, 2, QTableWidgetItem(appt.get('reason', '')))
            
            # Status column with translation and coloring
            status_key = appt['status']
            status_text = LANGUAGES[self.lang]['status'].get(status_key, status_key)
            status_item = QTableWidgetItem(status_text)
            
            # Set color based on status
            if status_key == 'completed':
                status_item.setForeground(QColor(Qt.darkGreen))
            elif status_key in ['canceled', 'no_show']:
                status_item.setForeground(QColor(Qt.red))
            elif status_key == 'scheduled':
                status_item.setForeground(QColor(Qt.darkBlue))
                
            self.table.setItem(row, 3, status_item)