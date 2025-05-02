from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QTableWidget, QTableWidgetItem, QPushButton,
                            QGridLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from datetime import datetime
from ..dashboard import Dashboard

class AdminDashboard(Dashboard):
    def __init__(self, user_data, db):
        super().__init__("admin", user_data, db)
        self.init_ui()
        
    def init_ui(self):
        super().init_ui()
        
        # Get data from database
        total_doctors = len(self.db.get_all_doctors())
        total_patients = len(self.db.get_all_patients())
        today_appointments = len([a for a in self.db.get_all_appointments() 
                                if a['date'] == datetime.now().strftime('%Y-%m-%d')])
        monthly_revenue = sum(b['amount'] for b in self.db.get_all_bills() 
                            if b['date'].startswith(datetime.now().strftime('%Y-%m')))
        
        # Stats cards
        cards_layout = QHBoxLayout()
        
        cards = [
            ("Total Doctors", str(total_doctors)),
            ("Total Patients", str(total_patients)),
            ("Today's Appointments", str(today_appointments)),
            ("Monthly Revenue", f"${monthly_revenue:,.2f}")
        ]
        
        for title, value, icon, color in [
            (cards[0][0], cards[0][1], "user-md", "blue"),
            (cards[1][0], cards[1][1], "procedures", "green"),
            (cards[2][0], cards[2][1], "calendar-check", "purple"),
            (cards[3][0], cards[3][1], "dollar-sign", "yellow")
        ]:
            card = self.create_card(title, value, icon, color)
            cards_layout.addWidget(card)
            
        self.layout.addLayout(cards_layout)
        
        # Main content
        content_layout = QHBoxLayout()
        
        # Recent activities
        activities_widget = QWidget()
        activities_widget.setObjectName("card")
        activities_layout = QVBoxLayout(activities_widget)
        
        activities_header = QHBoxLayout()
        activities_title = QLabel("Recent Activities")
        activities_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        view_all = QPushButton("View All")
        view_all.setStyleSheet("color: #3b82f6; text-decoration: underline;")
        
        activities_header.addWidget(activities_title)
        activities_header.addWidget(view_all)
        
        # Sample activities (in a real app, these would come from an activity log in the database)
        activities = [
            ("New patient registered - Michael Brown", "10 minutes ago", "user-plus", "blue"),
            ("Appointment scheduled with Dr. Johnson", "25 minutes ago", "calendar-plus", "green"),
            ("Payment received from Sarah Miller", "1 hour ago", "file-invoice", "purple"),
            ("System maintenance scheduled for tonight", "2 hours ago", "exclamation-triangle", "yellow")
        ]
        
        for activity, time, icon, color in activities:
            activity_widget = QWidget()
            activity_layout = QHBoxLayout(activity_widget)
            
            icon_label = QLabel()
            icon_label.setPixmap(QPixmap(f"assets/icons/{icon}.png").scaled(20, 20))
            icon_label.setStyleSheet(f"""
                background-color: {color}100;
                color: {color}600;
                padding: 8px;
                border-radius: 50%;
            """)
            
            text_widget = QWidget()
            text_layout = QVBoxLayout(text_widget)
            
            activity_label = QLabel(activity)
            activity_label.setStyleSheet("font-weight: 500;")
            
            time_label = QLabel(time)
            time_label.setStyleSheet("color: #6b7280; font-size: 12px;")
            
            text_layout.addWidget(activity_label)
            text_layout.addWidget(time_label)
            
            activity_layout.addWidget(icon_label)
            activity_layout.addWidget(text_widget)
            
            activities_layout.addWidget(activity_widget)
        
        activities_layout.addLayout(activities_header)
        activities_layout.addSpacing(10)
        
        # Quick actions
        quick_actions_widget = QWidget()
        quick_actions_widget.setObjectName("card")
        quick_actions_layout = QVBoxLayout(quick_actions_widget)
        
        quick_actions_title = QLabel("Quick Actions")
        quick_actions_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        actions_grid = QGridLayout()
        
        actions = [
            ("Add Doctor", "user-md", "blue", "manage-doctors"),
            ("Register Patient", "user-plus", "green", "manage-patients"),
            ("Generate Report", "chart-pie", "purple", "reports"),
            ("System Settings", "cog", "yellow", "settings")
        ]
        
        for i, (title, icon, color, page) in enumerate(actions):
            btn = QPushButton()
            btn.setProperty("page", page)
            btn_layout = QVBoxLayout(btn)
            
            icon_label = QLabel()
            icon_label.setPixmap(QPixmap(f"assets/icons/{icon}.png").scaled(32, 32))
            icon_label.setStyleSheet(f"color: {color};")
            icon_label.setAlignment(Qt.AlignCenter)
            
            text_label = QLabel(title)
            text_label.setStyleSheet("font-size: 12px; font-weight: medium;")
            text_label.setAlignment(Qt.AlignCenter)
            
            btn_layout.addWidget(icon_label)
            btn_layout.addWidget(text_label)
            
            btn.setStyleSheet("""
                QPushButton {
                    border: 1px solid #e5e7eb;
                    border-radius: 8px;
                    padding: 16px;
                }
                QPushButton:hover {
                    background-color: #f9fafb;
                }
            """)
            
            actions_grid.addWidget(btn, i // 2, i % 2)
            btn.clicked.connect(lambda _, p=page: self.parent().switch_page_by_name(p))
        
        quick_actions_layout.addWidget(quick_actions_title)
        quick_actions_layout.addLayout(actions_grid)
        
        # Add to content layout
        content_layout.addWidget(activities_widget, stretch=2)
        content_layout.addWidget(quick_actions_widget, stretch=1)
        
        self.layout.addLayout(content_layout)
        
        # Hospital statistics (placeholder)
        stats_widget = QWidget()
        stats_widget.setObjectName("chart-container")
        stats_layout = QVBoxLayout(stats_widget)
        
        stats_title = QLabel("Hospital Statistics")
        stats_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        stats_placeholder = QLabel("Chart would be displayed here")
        stats_placeholder.setAlignment(Qt.AlignCenter)
        
        stats_layout.addWidget(stats_title)
        stats_layout.addWidget(stats_placeholder)
        
        self.layout.addWidget(stats_widget)
        
        # Connect signals
        view_all.clicked.connect(lambda: self.parent().switch_page_by_name("reports"))