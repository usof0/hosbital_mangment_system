from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QScrollArea, QGridLayout, QDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from datetime import datetime
from datetime import datetime
from typing import Dict

from .dashboard import Dashboard
from .admin import AddNewAccountDialog


ACTIVITY_META = {
    "doctor": ("user-plus", "blue"),
    "patient": ("user-plus", "blue"),
    "appointment": ("calendar-plus", "green"),
    "payment": ("file-invoice", "purple"),
    "system": ("exclamation-triangle", "yellow")
}

DASHBOARD_TRANSLATIONS = {
    'en': {
        'titles': {
            'activities': 'Recent Activities',
            'quick_actions': 'Quick Actions',
            'stats': 'Hospital Statistics',
            'chart_placeholder': 'Chart would be displayed here',
            'no_activities': 'No recent activities.'
        },
        'stats_cards': {
            'doctors': 'Total Doctors',
            'patients': 'Total Patients',
            'appointments': "Today's Appointments",
            'revenue': 'Monthly Revenue'
        },
        'quick_actions': {
            'add_doctor': 'Add Doctor',
            'add_patient': 'Register Patient',
            'add_admin': 'Add Admin'
        },
        'activity_messages': {
            'new_doctor': 'New doctor registered - {name}',
            'new_patient': 'New patient registered - {name}',
            'new_appointment': 'Appointment scheduled with Dr. {last_name}',
            'new_payment': 'Payment received from {name}',
            'system_maintenance': 'System maintenance scheduled for tonight'
        },
        'time_ago': {
            'just_now': 'Just now',
            'minutes': '{minutes} minute{s} ago',
            'hours': '{hours} hour{s} ago',
            'days': '{days} day{s} ago'
        }
    },
    'ru': {
        'titles': {
            'activities': 'Последние действия',
            'quick_actions': 'Быстрые действия',
            'stats': 'Статистика больницы',
            'chart_placeholder': 'Здесь будет отображаться график',
            'no_activities': 'Нет последних действий'
        },
        'stats_cards': {
            'doctors': 'Всего врачей',
            'patients': 'Всего пациентов',
            'appointments': 'Записи на сегодня',
            'revenue': 'Доход за месяц'
        },
        'quick_actions': {
            'add_doctor': 'Добавить врача',
            'add_patient': 'Зарегистрировать пациента',
            'add_admin': 'Добавить администратора'
        },
        'activity_messages': {
            'new_doctor': 'Новый врач зарегистрирован - {name}',
            'new_patient': 'Новый пациент зарегистрирован - {name}',
            'new_appointment': 'Запись на прием к Dr. {last_name}',
            'new_payment': 'Оплата получена от {name}',
            'system_maintenance': 'Запланировано техническое обслуживание'
        },
        'time_ago': {
            'just_now': 'Только что',
            'minutes': '{minutes} минут{s} назад',
            'hours': '{hours} час{s} назад',
            'days': '{days} день{s} назад'
        }
    }
}

class AdminDashboard(Dashboard):
    def __init__(self, user_data, db, lang='en'):
        super().__init__("admin", user_data, db, lang)
        self.activities = []
        
    def init_ui(self):
        if self.layout():
            QWidget().setLayout(self.layout())

        super().init_ui()
        self.load_activities()
        self.setup_ui_components()

    def load_activities(self):
        def get_time_ago(timestamp: datetime) -> str:
            """Convert a datetime object to a human-readable relative time string."""
            now = datetime.now()
            diff_seconds = int((now - timestamp).total_seconds())
            translations = DASHBOARD_TRANSLATIONS[self.lang]['time_ago']

            if diff_seconds < 60:
                return translations['just_now']
            elif diff_seconds < 3600:  # less than 1 hour
                minutes = diff_seconds // 60
                plural = '' if self.lang == 'ru' and minutes % 10 == 1 and minutes % 100 != 11 else 's'
                return translations['minutes'].format(minutes=minutes, s=plural)
            elif diff_seconds < 86400:  # less than 1 day
                hours = diff_seconds // 3600
                plural = '' if self.lang == 'ru' and hours % 10 == 1 and hours % 100 != 11 else 's'
                return translations['hours'].format(hours=hours, s=plural)
            else:
                days = diff_seconds // 86400
                plural = '' if self.lang == 'ru' and days % 10 == 1 and days % 100 != 11 else 's'
                return translations['days'].format(days=days, s=plural)

        def combine_date_time(record: Dict[str, any]) -> datetime:
            """Combine DATE and TIME fields into a single datetime object."""
            return datetime.combine(record['creation_date'], record['creation_time'])

        # Fetch data from database
        self.new_doctors = self.db.get_last_doctors()
        self.new_patients = self.db.get_last_patients()
        self.new_appointments = self.db.get_last_appointments()
        self.new_bills = self.db.get_last_bills()

        temp_activities = []
        messages = DASHBOARD_TRANSLATIONS[self.lang]['activity_messages']

        # Process doctors
        for doctor in self.new_doctors:
            created_at = combine_date_time(doctor)
            time_ago = get_time_ago(created_at)
            icon, color = ACTIVITY_META["doctor"]
            temp_activities.append((
                created_at,
                (messages['new_doctor'].format(name=doctor['name']), time_ago, icon, color)
            ))

        # Process patients
        for patient in self.new_patients:
            created_at = combine_date_time(patient)
            time_ago = get_time_ago(created_at)
            icon, color = ACTIVITY_META["patient"]
            temp_activities.append((
                created_at,
                (messages['new_patient'].format(name=patient['name']), time_ago, icon, color)
            ))

        # Process appointments
        for appointment in self.new_appointments:
            created_at = combine_date_time(appointment)
            time_ago = get_time_ago(created_at)
            doctor_last_name = appointment['doctor_name'].split()[-1]
            icon, color = ACTIVITY_META["appointment"]
            temp_activities.append((
                created_at,
                (messages['new_appointment'].format(last_name=doctor_last_name), time_ago, icon, color)
            ))

        # Process bills
        for bill in self.new_bills:
            created_at = combine_date_time(bill)
            time_ago = get_time_ago(created_at)
            icon, color = ACTIVITY_META["payment"]
            temp_activities.append((
                created_at,
                (messages['new_payment'].format(name=bill['patient_name']), time_ago, icon, color)
            ))

        # Optional: Add hardcoded system notifications
        system_message = (
            datetime.now(),  # dummy timestamp for sorting
            (messages['system_maintenance'], get_time_ago(datetime.now()), *ACTIVITY_META["system"])
        )
        temp_activities.append(system_message)

        # Sort activities by most recent (descending order)
        temp_activities.sort(key=lambda x: x[0], reverse=True)

        # Extract only the formatted activity tuples
        self.activities = [activity[1] for activity in temp_activities]

    def open_dialog(self, action):
        if action == 'add-patient':
            patient_dialog = AddNewAccountDialog('patient', self.db, self, self.lang)
            if patient_dialog.exec_() == QDialog.Accepted:
                # Refresh your patient list or do other updates
                pass

        elif action == 'add-doctor':
            doctor_dialog = AddNewAccountDialog('doctor', self.db, self, self.lang)
            if doctor_dialog.exec_() == QDialog.Accepted:
                # Refresh your doctor list or do other updates
                pass
        elif action == 'add-admin':
            admin_dialog = AddNewAccountDialog('admin', self.db, self, self.lang)
            if admin_dialog.exec_() == QDialog.Accepted:
                # Refresh your admin list or do other updates
                pass
        else:
            pass

    def setup_ui_components(self):
        """Setup all UI components"""
        self.setup_stats_cards()
        self.setup_main_content()

    def setup_stats_cards(self):
        cards_layout = QHBoxLayout()

        total_doctors = len(self.db.get_all_doctors())
        total_patients = len(self.db.get_all_patients())
        today_appointments = len([a for a in self.db.get_all_appointments() 
                                if a['date'] == datetime.now().strftime('%Y-%m-%d')])
        monthly_revenue = sum(b['amount'] for b in self.db.get_all_bills() 
                            if b['date'].year == (datetime.now().year))

        stats = [
            (DASHBOARD_TRANSLATIONS[self.lang]['stats_cards']['doctors'], 
            str(total_doctors), "medical-team", "blue"),
            (DASHBOARD_TRANSLATIONS[self.lang]['stats_cards']['patients'], 
            str(total_patients), "patients", "green"),
            (DASHBOARD_TRANSLATIONS[self.lang]['stats_cards']['appointments'], 
            str(today_appointments), "appointment", "purple"),
            (DASHBOARD_TRANSLATIONS[self.lang]['stats_cards']['revenue'], 
            f"${monthly_revenue:,.2f}" if self.lang == 'en' else f"{monthly_revenue:,.2f}₽", 
            "file-invoice-dollar", "yellow")
        ]
        
        for title, value, icon, color in stats:
            card = self.create_card(title, value, icon, color)
            cards_layout.addWidget(card)
            
        self.layout.addLayout(cards_layout)
        
    def setup_main_content(self):
        # Main content
        content_layout = QHBoxLayout()

        # Recent activities widget
        activities_widget = QWidget()
        activities_widget.setObjectName("card")
        activities_layout = QVBoxLayout(activities_widget)

        # Header layout
        activities_header = QHBoxLayout()
        activities_title = QLabel(DASHBOARD_TRANSLATIONS[self.lang]['titles']['activities'])
        activities_title.setStyleSheet("font-size: 16px; font-weight: bold;")

        activities_header.addWidget(activities_title)

        # Scroll area for activities
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # Container for activity widgets
        self.activities_container = QWidget()
        self.activities_layout = QVBoxLayout(self.activities_container)
        self.activities_layout.setAlignment(Qt.AlignTop)
        self.activities_layout.setSpacing(10)
        self.activities_layout.setContentsMargins(10, 10, 10, 10)

        # Populate activities
        if self.activities:
            for activity, time, icon, color in self.activities:
                activity_widget = QWidget()
                activity_widget.setStyleSheet("padding: 8px;")
                activity_layout = QHBoxLayout(activity_widget)
                activity_layout.setContentsMargins(0, 0, 0, 0)
                activity_layout.setSpacing(10)

                icon_label = QLabel()
                icon_label.setPixmap(QPixmap(f"assets/icons/{icon}.png").scaled(20, 20))
                icon_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

                text_widget = QWidget()
                text_layout = QVBoxLayout(text_widget)
                text_layout.setContentsMargins(0, 0, 0, 0)
                text_layout.setSpacing(4)

                activity_label = QLabel(activity)
                activity_label.setStyleSheet("font-weight: 500;")
                activity_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

                time_label = QLabel(time)
                time_label.setStyleSheet("color: #6b7280; font-size: 12px;")
                time_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

                text_layout.addWidget(activity_label)
                text_layout.addWidget(time_label)

                activity_layout.addWidget(icon_label)
                activity_layout.addWidget(text_widget, stretch=1)

                self.activities_layout.addWidget(activity_widget)
        else:
            empty_label = QLabel(DASHBOARD_TRANSLATIONS[self.lang]['titles']['no_activities'])
            empty_label.setAlignment(Qt.AlignCenter)
            empty_label.setStyleSheet("color: #9ca3af;")
            self.activities_layout.addWidget(empty_label)

        # Finalize scroll area
        scroll_area.setWidget(self.activities_container)

        # Add header and scroll area to layout
        activities_layout.addLayout(activities_header)
        activities_layout.addWidget(scroll_area)

        # Quick actions
        quick_actions_widget = QWidget()
        quick_actions_widget.setObjectName("card")
        quick_actions_layout = QVBoxLayout(quick_actions_widget)

        quick_actions_title = QLabel(DASHBOARD_TRANSLATIONS[self.lang]['titles']['quick_actions'])
        quick_actions_title.setStyleSheet("font-size: 16px; font-weight: bold;")

        actions_grid = QGridLayout()

        actions = [
            (DASHBOARD_TRANSLATIONS[self.lang]['quick_actions']['add_doctor'], 
             "user-plus", "blue", "add-doctor"),
            (DASHBOARD_TRANSLATIONS[self.lang]['quick_actions']['add_patient'], 
             "user-plus", "green", "add-patient"),
            (DASHBOARD_TRANSLATIONS[self.lang]['quick_actions']['add_admin'], 
             "admin", "purple", "add-admin"),
        ]

        for i, (title, icon, color, dialog) in enumerate(actions):
            btn = QPushButton()
            btn.setProperty("dialog", dialog)
            btn_layout = QHBoxLayout(btn)
            btn_layout.setContentsMargins(10, 10, 10, 10)
            btn_layout.setSpacing(10)

            icon_label = QLabel()
            icon_label.setPixmap(QPixmap(f"assets/icons/{icon}.png").scaled(24, 24))
            icon_label.setStyleSheet(f"color: {color};")

            text_label = QLabel(title)
            text_label.setStyleSheet("font-size: 14px; font-weight: 500;")

            btn_layout.addWidget(icon_label, alignment=Qt.AlignVCenter)
            btn_layout.addWidget(text_label, alignment=Qt.AlignVCenter)

            btn.setStyleSheet("""
                QPushButton {
                    border: 1px solid #e5e7eb;
                    border-radius: 8px;
                    padding: 8px;
                    text-align: left;
                    min-height: 60px;
                }
                QPushButton:hover {
                    background-color: #f9fafb;
                }
            """)

            actions_grid.addWidget(btn, i, 0)
            btn.clicked.connect(lambda _, a=dialog: self.open_dialog(a))

        quick_actions_layout.addWidget(quick_actions_title)
        quick_actions_layout.addLayout(actions_grid)

        # Add to content layout
        content_layout.addWidget(activities_widget, stretch=2)
        content_layout.addWidget(quick_actions_widget, stretch=1)

        self.layout.addLayout(content_layout)

        # Hospital statistics (placeholder)
        stats_widget = QWidget()
        stats_widget.setObjectName("chart-container")

        self.layout.addWidget(stats_widget)