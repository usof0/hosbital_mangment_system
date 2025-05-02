from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QDialog,
                            QTableWidget, QTableWidgetItem, QPushButton,
                            QLineEdit, QTextEdit, QDateEdit, QTimeEdit,
                            QMessageBox, QHeaderView, QFormLayout, QGroupBox, QFrame, QScrollArea)
from PyQt5.QtCore import Qt, QDate, QTime
from datetime import datetime
from PyQt5.QtGui import QPixmap





###################################################### Patient Pages #######################################33




# class PatientMedicalRecordsPage(QWidget):
#     def __init__(self, user_data, db):
#         super().__init__()
#         self.user_data = user_data
#         self.db = db
#         self.init_ui()
        
#     def init_ui(self):
#         layout = QVBoxLayout(self)
        
#         # Header
#         header = QHBoxLayout()
#         title = QLabel("My Medical Records")
#         title.setStyleSheet("font-size: 18px; font-weight: bold;")
        
#         self.refresh_btn = QPushButton("Refresh")
#         self.refresh_btn.clicked.connect(self.load_records)
        
#         header.addWidget(title)
#         header.addStretch()
#         header.addWidget(self.refresh_btn)
        
#         # Records table
#         self.records_table = QTableWidget()
#         self.records_table.setColumnCount(5)
#         self.records_table.setHorizontalHeaderLabels(
#             ["Date", "Doctor", "Diagnosis", "Treatment", "Notes"]
#         )
#         self.records_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
#         self.records_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
#         layout.addLayout(header)
#         layout.addWidget(self.records_table)
        
#         self.load_records()
        
#     def load_records(self):
#         records = self.db.get_patient_medical_records(self.user_data['id'])
#         self.records_table.setRowCount(len(records))
        
#         for row_idx, record in enumerate(records):
#             doctor = self.db.get_doctor_by_id(record['doctor_id'])
            
#             items = [
#                 QTableWidgetItem(record['date']),
#                 QTableWidgetItem(doctor['name'] if doctor else "Unknown"),
#                 QTableWidgetItem(record['diagnosis']),
#                 QTableWidgetItem(record['treatment']),
#                 QTableWidgetItem(record.get('notes', ''))
#             ]
            
#             for col_idx, item in enumerate(items):
#                 item.setFlags(item.flags() & ~Qt.ItemIsEditable)
#                 self.records_table.setItem(row_idx, col_idx, item)
        
        # self.records_table.resizeColumnsToContents()



# from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
#                             QComboBox, QDateEdit, QTimeEdit, QTextEdit, QFormLayout, 
#                             QGroupBox, QScrollArea, QFrame, QMessageBox)
# from PyQt5.QtCore import Qt, QDate, QTime
# from datetime import datetime



# from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
#                             QTableWidget, QTableWidgetItem, QPushButton,
#                             QHeaderView, QTextEdit, QComboBox, QDateEdit,
#                             QMessageBox, QGroupBox, QScrollArea, QFrame)
# from PyQt5.QtCore import Qt, QDate


