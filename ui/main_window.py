from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QStackedWidget, QMenu, QAction, QMessageBox)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap

from .dashboard import Dashboard
from .doctor_dash import DoctorDashboard
from .patient_dash import PatientDashboard
from .admin.admin_dash import AdminDashboard
from .doctor import (
                    DoctorProfilePage,
                    DoctorSchedulePage,
                    MyPatientsPage,
                    WritePrescriptionPage,
                    )
from .patient import (
                    PatientProfilePage,
                    PatientAppointmentsPage,
                    PatientMedicalRecordsPage,
                    PatientPrescriptionsPage,
                    PatientBillingPage,
                    )


class MainWindow(QMainWindow):
    def __init__(self, user_data, role, db):
        super().__init__()
        self.user_data = user_data
        self.role = role
        self.db = db
        
        self.setWindowTitle("MediCare Hospital Management System")
        self.setMinimumSize(1200, 800)
        
        # Initialize core components
        self.content_stack = QStackedWidget()
        self.sidebar = QWidget()
        self.page_title = QLabel("Dashboard")
        
        self.init_ui()
        
    def init_ui(self):
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        main_layout = QHBoxLayout(main_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Initialize sidebar
        self.init_sidebar()
        
        # Content area
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(0)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Top bar
        self.init_top_bar(content_layout)
        
        # Initialize pages
        self.init_pages()
        
        # Add widgets to content layout
        content_layout.addWidget(self.content_stack)
        
        # Add sidebar and content to main layout
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(content_widget)
        
        # Connect signals
        self.connect_signals()

    def init_sidebar(self):
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(250)
        
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setSpacing(0)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        
        # Sidebar header
        sidebar_header = QWidget()
        sidebar_header.setStyleSheet("background: #111827; padding: 16px;")
        
        header_layout = QHBoxLayout(sidebar_header)
        
        logo = QLabel()
        logo.setPixmap(QPixmap("assets/icons/hospital.png").scaled(24, 24))
        
        title = QLabel("MediCare")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
        
        header_layout.addWidget(logo)
        header_layout.addWidget(title)
        
        # User profile
        user_widget = QWidget()
        user_widget.setStyleSheet("padding: 16px; border-bottom: 1px solid #374151;")
        
        user_layout = QHBoxLayout(user_widget)
        
        avatar = QLabel()
        avatar.setPixmap(QPixmap(self.user_data.get('avatar', 'assets/icons/user.png')).scaled(40, 40))
        avatar.setStyleSheet("border-radius: 20px;")
        
        user_info = QWidget()
        user_info_layout = QVBoxLayout(user_info)
        
        name = QLabel(self.user_data['name'])
        name.setStyleSheet("font-weight: 500; color: white;")
        
        role = QLabel(self.role.capitalize())
        role.setStyleSheet("color: #9ca3af; font-size: 12px;")
        
        user_info_layout.addWidget(name)
        user_info_layout.addWidget(role)
        
        user_layout.addWidget(avatar)
        user_layout.addWidget(user_info)
        
        # Navigation
        nav_widget = QWidget()
        nav_widget.setStyleSheet("padding: 16px;")
        
        nav_layout = QVBoxLayout(nav_widget)
        
        # Common nav items
        dashboard_btn = QPushButton("Dashboard")
        dashboard_btn.setObjectName("nav-item")
        dashboard_btn.setProperty("page", "dashboard")
        
        profile_btn = QPushButton("Profile")
        profile_btn.setObjectName("nav-item")
        profile_btn.setProperty("page", "profile")
        
        logout_btn = QPushButton("Logout")
        logout_btn.setObjectName("nav-item")
        
        # Role-specific nav items
        if self.role == "patient":
            appointments_btn = QPushButton("Appointments")
            appointments_btn.setObjectName("nav-item")
            appointments_btn.setProperty("page", "appointments")
            
            prescriptions_btn = QPushButton("Prescriptions")
            prescriptions_btn.setObjectName("nav-item")
            prescriptions_btn.setProperty("page", "prescriptions")
            
            records_btn = QPushButton("Medical Records")
            records_btn.setObjectName("nav-item")
            records_btn.setProperty("page", "medical-records")
            
            billing_btn = QPushButton("Billing")
            billing_btn.setObjectName("nav-item")
            billing_btn.setProperty("page", "billing")

            # book_appointment_btn = QPushButton("Book Appointment")
            # book_appointment_btn.setObjectName("nav-item")
            # book_appointment_btn.setProperty("page", "book-appointment")

            nav_layout.addWidget(dashboard_btn)
            nav_layout.addWidget(appointments_btn)
            nav_layout.addWidget(prescriptions_btn)
            nav_layout.addWidget(records_btn)
            nav_layout.addWidget(billing_btn)
            # nav_layout.addWidget(book_appointment_btn)
            
        elif self.role == "doctor":
            schedule_btn = QPushButton("Schedule")
            schedule_btn.setObjectName("nav-item")
            schedule_btn.setProperty("page", "schedule")
            
            patients_btn = QPushButton("My Patients")
            patients_btn.setObjectName("nav-item")
            patients_btn.setProperty("page", "my-patients")
            
            write_pres_btn = QPushButton("Write Prescription")
            write_pres_btn.setObjectName("nav-item")
            write_pres_btn.setProperty("page", "write-prescription")
            
            nav_layout.addWidget(dashboard_btn)
            nav_layout.addWidget(schedule_btn)
            nav_layout.addWidget(patients_btn)
            nav_layout.addWidget(write_pres_btn)
            
        elif self.role == "admin":
            manage_doctors_btn = QPushButton("Manage Doctors")
            manage_doctors_btn.setObjectName("nav-item")
            manage_doctors_btn.setProperty("page", "manage-doctors")
            
            manage_patients_btn = QPushButton("Manage Patients")
            manage_patients_btn.setObjectName("nav-item")
            manage_patients_btn.setProperty("page", "manage-patients")
            
            reports_btn = QPushButton("Reports")
            reports_btn.setObjectName("nav-item")
            reports_btn.setProperty("page", "reports")
            
            settings_btn = QPushButton("Settings")
            settings_btn.setObjectName("nav-item")
            settings_btn.setProperty("page", "settings")
            
            nav_layout.addWidget(dashboard_btn)
            nav_layout.addWidget(manage_doctors_btn)
            nav_layout.addWidget(manage_patients_btn)
            nav_layout.addWidget(reports_btn)
            nav_layout.addWidget(settings_btn)
        
        # Add common bottom items
        nav_layout.addStretch()
        nav_layout.addWidget(profile_btn)
        nav_layout.addWidget(logout_btn)
        
        # Add widgets to sidebar
        sidebar_layout.addWidget(sidebar_header)
        sidebar_layout.addWidget(user_widget)
        sidebar_layout.addWidget(nav_widget)

    def init_top_bar(self, parent_layout):
        top_bar = QWidget()
        top_bar.setStyleSheet("background: white; padding: 16px; border-bottom: 1px solid #e5e7eb;")
        
        top_bar_layout = QHBoxLayout(top_bar)
        
        # Sidebar toggle (for mobile)
        sidebar_toggle = QPushButton()
        sidebar_toggle.setIcon(QIcon("assets/icons/menu.png"))
        sidebar_toggle.setIconSize(QSize(24, 24))
        sidebar_toggle.setFlat(True)
        
        # Page title
        self.page_title = QLabel("Dashboard")
        self.page_title.setStyleSheet("font-size: 18px; font-weight: 600;")
        
        # Right side buttons
        right_buttons = QWidget()
        right_layout = QHBoxLayout(right_buttons)
        
        # Notification button
        notification_btn = QPushButton()
        notification_btn.setIcon(QIcon("assets/icons/bell.png"))
        notification_btn.setIconSize(QSize(20, 20))
        notification_btn.setFlat(True)
        
        # User menu
        user_menu_btn = QPushButton()
        user_menu_btn.setIcon(QIcon(self.user_data.get('avatar', 'assets/icons/user-patient.png')))
        user_menu_btn.setIconSize(QSize(32, 32))
        user_menu_btn.setFlat(True)
        user_menu_btn.setText(self.user_data['name'])
        user_menu_btn.setStyleSheet("text-align: left; padding-left: 8px;")
        
        # Create user menu
        self.user_menu = QMenu()
        profile_action = QAction("Profile", self)
        settings_action = QAction("Settings", self)
        logout_action = QAction("Logout", self)
        
        self.user_menu.addAction(profile_action)
        self.user_menu.addAction(settings_action)
        self.user_menu.addSeparator()
        self.user_menu.addAction(logout_action)
        
        user_menu_btn.setMenu(self.user_menu)
        
        right_layout.addWidget(notification_btn)
        right_layout.addWidget(user_menu_btn)
        
        # Add to top bar
        top_bar_layout.addWidget(sidebar_toggle)
        top_bar_layout.addWidget(self.page_title)
        top_bar_layout.addWidget(right_buttons)
        
        parent_layout.addWidget(top_bar)

    def init_pages(self):
        # Add dashboard
        if self.role == "patient":
            self.dashboard = PatientDashboard(self.user_data, self.db)
        elif self.role == "doctor":
            self.dashboard = DoctorDashboard(self.user_data, self.db)
            self.dashboard.main_window = self
        else:
            self.dashboard = AdminDashboard(self.user_data, self.db)
        
        self.content_stack.addWidget(self.dashboard)
        
        # Initialize only the pages we need
        self.other_pages = {}
        
        if self.role == "doctor":
            profile_page = DoctorProfilePage(self.user_data, self.db)
            self.other_pages["profile"] = profile_page
            self.content_stack.addWidget(profile_page)
            
            schedule_page = DoctorSchedulePage(self.user_data, self.db)
            self.other_pages["schedule"] = schedule_page
            self.content_stack.addWidget(schedule_page)
            
            patients_page = MyPatientsPage(self.user_data, self.db)
            self.other_pages["my-patients"] = patients_page
            self.content_stack.addWidget(patients_page)
            
            prescription_page = WritePrescriptionPage(self.user_data, self.db)
            self.other_pages["write-prescription"] = prescription_page
            self.content_stack.addWidget(prescription_page)
        
        elif self.role == "patient":
            profile_page = PatientProfilePage(self.user_data, self.db)
            self.other_pages["profile"] = profile_page
            self.content_stack.addWidget(profile_page)

            appointments_page = PatientAppointmentsPage(self.user_data, self.db)
            self.other_pages["appointments"] = appointments_page
            self.content_stack.addWidget(appointments_page)

            prescriptions_page = PatientPrescriptionsPage(self.user_data, self.db)
            self.other_pages["prescriptions"] = prescriptions_page
            self.content_stack.addWidget(prescriptions_page)

            patient_records_page = PatientMedicalRecordsPage(self.user_data, self.db)
            self.other_pages["medical-records"] = patient_records_page
            self.content_stack.addWidget(patient_records_page)

            billing_page = PatientBillingPage(self.user_data, self.db)
            self.other_pages["billing"] = billing_page
            self.content_stack.addWidget(billing_page)

    def connect_signals(self):
        # Find sidebar toggle button and connect
        for child in self.findChildren(QPushButton):
            if child.icon() and child.icon().name() == "menu.png":
                child.clicked.connect(self.toggle_sidebar)
                break
                
        # Connect logout buttons
        for child in self.sidebar.findChildren(QPushButton):
            if child.text() == "Logout":
                child.clicked.connect(self.logout)
                
        # Connect menu actions
        for action in self.user_menu.actions():
            if action.text() == "Logout":
                action.triggered.connect(self.logout)
            elif action.text() == "Profile":
                action.triggered.connect(lambda: self.switch_page_by_name("profile"))
            elif action.text() == "Settings":
                action.triggered.connect(lambda: self.switch_page_by_name("settings"))
                
        # Connect nav buttons to switch pages
        for btn in self.sidebar.findChildren(QPushButton):
            if btn.property("page"):
                btn.clicked.connect(self.switch_page)
                
        # Set dashboard as active
        dashboard_btn = self.sidebar.findChild(QPushButton, "nav-item")
        if dashboard_btn:
            dashboard_btn.setProperty("active", True)
            dashboard_btn.style().unpolish(dashboard_btn)
            dashboard_btn.style().polish(dashboard_btn)

    def toggle_sidebar(self):
        self.sidebar.setVisible(not self.sidebar.isVisible())
            
    def switch_page(self):
        sender = self.sender()
        page = sender.property("page")
        self.switch_page_by_name(page)
            
    def switch_page_by_name(self, page_name):
        if page_name == "dashboard":
            self.content_stack.setCurrentWidget(self.dashboard)
        elif page_name in self.other_pages:
            self.content_stack.setCurrentWidget(self.other_pages[page_name])
        else:
            QMessageBox.warning(self, "Page Not Available", 
                              "This page is not implemented yet")
            return
        
        self.page_title.setText(page_name.replace("-", " ").title())
        
        # Update active nav item
        for btn in self.sidebar.findChildren(QPushButton):
            btn.setProperty("active", btn.property("page") == page_name)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
        
    def logout(self):
        reply = QMessageBox.question(
            self, 'Logout', 
            'Are you sure you want to logout?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            from ui.login_window import LoginWindow
            self.login_window = LoginWindow()
            self.login_window.show()
            self.close()