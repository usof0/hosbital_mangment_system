from .needs import *

class DoctorProfilePage(QWidget):
    def __init__(self, user_data, db):
        super().__init__()
        self.user_data = user_data
        self.db = db
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Header
        header = QHBoxLayout()
        avatar = QLabel()
        avatar.setPixmap(QPixmap("assets/icons/doctor.png").scaled(80, 80))
        
        info = QVBoxLayout()
        name = QLabel(self.user_data['name'])
        name.setStyleSheet("font-size: 18px; font-weight: bold;")
        role = QLabel("Doctor")
        role.setStyleSheet("font-size: 14px; color: #666;")
        
        info.addWidget(name)
        info.addWidget(role)
        header.addWidget(avatar)
        header.addLayout(info)
        layout.addLayout(header)
        
        # Profile form
        form = QFormLayout()
        
        self.specialization_input = QLineEdit(self.user_data.get('specialization', ''))
        self.department_input = QLineEdit(self.user_data.get('department', ''))
        self.email_input = QLineEdit(self.user_data.get('email', ''))
        self.phone_input = QLineEdit(self.user_data.get('phone', ''))
        
        form.addRow("Specialization:", self.specialization_input)
        form.addRow("Department:", self.department_input)
        form.addRow("Email:", self.email_input)
        form.addRow("Phone:", self.phone_input)
        
        layout.addLayout(form)
        
        # Save button
        save_btn = QPushButton("Save Profile")
        save_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px;")
        save_btn.clicked.connect(self.save_profile)
        layout.addWidget(save_btn, alignment=Qt.AlignRight)

    def save_profile(self):
        self.user_data.update({
            'specialization': self.specialization_input.text(),
            'department': self.department_input.text(),
            'email': self.email_input.text(),
            'phone': self.phone_input.text()
        })
        
        # Update in database
        for i, doctor in enumerate(self.db.data['users']['doctors']):
            if doctor['id'] == self.user_data['id']:
                self.db.data['users']['doctors'][i] = self.user_data
                break
                
        self.db._save_data(self.db.data)
        QMessageBox.information(self, "Success", "Profile updated successfully!")