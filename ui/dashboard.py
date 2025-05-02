# ui/dashboard.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


class Dashboard(QWidget):
    def __init__(self, role, user_data, db):
        super().__init__()
        self.role = role
        self.user_data = user_data
        self.db = db  # Store the database reference
        self.init_ui()
        
    def init_ui(self):
        self.layout = QVBoxLayout(self)
        
        # Header
        # # header_w
        header = QHBoxLayout()
        title = QLabel(f"{self.role.capitalize()} Dashboard")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        header.addWidget(title)
        
        self.layout.addLayout(header)
        
    def create_card(self, title, value, icon, color):
        card = QWidget()
        card.setObjectName("card")
        card.setStyleSheet(f"""
            QWidget#card {{
                background: white;
                border-radius: 8px;
                padding: 16px;
                margin: 4px;
            }}
        """)
        
        layout = QHBoxLayout(card)
        
        # Icon
        icon_label = QLabel()
        try:
            icon_label.setPixmap(QPixmap(f"assets/icons/{icon}.png").scaled(40, 40))
        except:
            # Fallback if icon not found
            icon_label.setText(icon)
        icon_label.setStyleSheet(f"""
            background-color: {color};
            padding: 8px;
            border-radius: 50%;
            min-width: 40px;
            max-width: 40px;
            min-height: 40px;
            max-height: 40px;
            font-weight: bold;
        """)
        
        # Text
        text_widget = QWidget()
        text_layout = QVBoxLayout(text_widget)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #6b7280;")
        
        value_label = QLabel(value)
        value_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        
        text_layout.addWidget(title_label)
        text_layout.addWidget(value_label)
        
        layout.addWidget(icon_label)
        layout.addWidget(text_widget)
        
        return card
    
    def switch_page(self, page_name):
        """Switch to another page in the main window"""
        if hasattr(self, 'main_window'):
            self.main_window.switch_page_by_name(page_name)