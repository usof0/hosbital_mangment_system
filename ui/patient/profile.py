from .needs import *

class PatientProfilePage(QWidget):
    def __init__(self, user_data, db):
        super().__init__()
        self.user_data = user_data
        self.db = db
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Header
        # title = QLabel("My Profile")
        # title.setStyleSheet("font-size: 18px; font-weight: bold;")
        # Header
        header = QHBoxLayout()
        avatar = QLabel()
        avatar.setPixmap(QPixmap("assets/icons/user.png").scaled(80, 80))

        info = QVBoxLayout()
        name = QLabel(self.user_data['name'])
        name.setStyleSheet("font-size: 18px; font-weight: bold;")
        role = QLabel("Patient")
        role.setStyleSheet("font-size: 14px; color: #666;")
        
        info.addWidget(name)
        info.addWidget(role)
        header.addWidget(avatar)
        header.addLayout(info)
        layout.addLayout(header)
        
        # Form layout
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)
        
        # Personal Info
        self.name_input = QLineEdit(self.user_data.get('name', ''))
        self.dob_input = QDateEdit()
        self.dob_input.setDisplayFormat("yyyy-MM-dd")
        if 'dob' in self.user_data:
            self.dob_input.setDate(QDate.fromString(self.user_data['dob'], "yyyy-MM-dd"))
        
        self.gender_input = QComboBox()
        self.gender_input.addItems(["Male", "Female", "Other"])
        if 'gender' in self.user_data:
            index = self.gender_input.findText(self.user_data['gender'])
            if index >= 0:
                self.gender_input.setCurrentIndex(index)
        
        self.blood_type_input = QComboBox()
        self.blood_type_input.addItems(["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", "Unknown"])
        if 'blood_type' in self.user_data:
            index = self.blood_type_input.findText(self.user_data['blood_type'])
            if index >= 0:
                self.blood_type_input.setCurrentIndex(index)
        
        # Contact Info
        self.email_input = QLineEdit(self.user_data.get('email', ''))
        self.phone_input = QLineEdit(self.user_data.get('phone', ''))
        self.address_input = QTextEdit()
        self.address_input.setPlainText(self.user_data.get('address', ''))
        self.address_input.setMaximumHeight(80)
        
        # Add to form
        form.addRow(QLabel("<b>Personal Information</b>"))
        form.addRow("Full Name:", self.name_input)
        form.addRow("Date of Birth:", self.dob_input)
        form.addRow("Gender:", self.gender_input)
        form.addRow("Blood Type:", self.blood_type_input)
        
        form.addRow(QLabel("<b>Contact Information</b>"))
        form.addRow("Email:", self.email_input)
        form.addRow("Phone:", self.phone_input)
        form.addRow("Address:", self.address_input)
        
        # Save button
        save_btn = QPushButton("Save Changes")
        save_btn.setStyleSheet("background-color: #10b981; color: white;")
        save_btn.clicked.connect(self.save_profile)
        
        layout.addLayout(form)
        layout.addWidget(save_btn, alignment=Qt.AlignRight)
        
    def save_profile(self):
        updated_data = {
            'name': self.name_input.text(),
            'dob': self.dob_input.date().toString("yyyy-MM-dd"),
            'gender': self.gender_input.currentText(),
            'blood_type': self.blood_type_input.currentText(),
            'email': self.email_input.text(),
            'phone': self.phone_input.text(),
            'address': self.address_input.toPlainText()
        }
        
        try:
            self.db.update_patient(self.user_data['id'], updated_data)
            QMessageBox.information(self, "Success", "Profile updated successfully")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update profile: {str(e)}")
