from .needs import *

LANGUAGES = {
    'en': {
        'page_title': 'My Patients',
        'table_headers': ['Name', 'Last Visit', 'Condition', 'Actions'],
        'view_button': 'View',
        'patient_info': {
            'title': 'Patient: {name}',
            'name': '<b>Name:</b> {name}',
            'dob': '<b>DOB:</b> {dob}',
            'blood_type': '<b>Blood Type:</b> {blood_type}',
            'last_visit': '<b>Last Visit:</b> {last_visit}',
            'unknown': 'Unknown',
            'never': 'Never'
        },
        'medical_records': {
            'no_records': 'No records'
        }
    },
    'ru': {
        'page_title': 'Мои пациенты',
        'table_headers': ['Имя', 'Последний визит', 'Диагноз', 'Действия'],
        'view_button': 'Просмотр',
        'patient_info': {
            'title': 'Пациент: {name}',
            'name': '<b>Имя:</b> {name}',
            'dob': '<b>Дата рождения:</b> {dob}',
            'blood_type': '<b>Группа крови:</b> {blood_type}',
            'last_visit': '<b>Последний визит:</b> {last_visit}',
            'unknown': 'Неизвестно',
            'never': 'Никогда'
        },
        'medical_records': {
            'no_records': 'Нет записей'
        }
    }
}

class MyPatientsPage(QWidget):
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
        
        # Patient table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(LANGUAGES[self.lang]['table_headers'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        
        layout.addWidget(self.table)
        self.load_patients()
        
    def load_patients(self):
        # Get unique patient IDs for this doctor
        patient_ids = {a['patient_id'] for a in self.db.get_doctor_appointments(self.user_data['id'])}
        patients = [self.db.get_patient_by_id(pid) for pid in patient_ids if pid]
        
        self.table.setRowCount(len(patients))
        
        for row, patient in enumerate(patients):
            # Patient name
            self.table.setItem(row, 0, QTableWidgetItem(patient['name']))
            
            # Last visit date
            last_appt = max(
                (a['date'] for a in self.db.get_patient_appointments(patient['id'])
                if a['doctor_id'] == self.user_data['id']),
                default=LANGUAGES[self.lang]['patient_info']['never']
            )
            
            last_appt_str = (
                last_appt.strftime("%Y-%m-%d") 
                if hasattr(last_appt, 'strftime') 
                else str(last_appt)
            )
            self.table.setItem(row, 1, QTableWidgetItem(last_appt_str))
            
            # Medical condition
            records = self.db.get_patient_medical_records(patient['id'])
            condition = (
                records[-1]['diagnosis'] 
                if records 
                else LANGUAGES[self.lang]['medical_records']['no_records']
            )
            self.table.setItem(row, 2, QTableWidgetItem(condition))
            
            # View button
            btn = QPushButton(LANGUAGES[self.lang]['view_button'])
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #3b82f6;
                    color: white;
                    padding: 5px 10px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #2563eb;
                }
            """)
            btn.clicked.connect(lambda _, p=patient: self.view_patient(p))
            self.table.setCellWidget(row, 3, btn)
    
    def view_patient(self, patient):
        dialog = QDialog(self)
        dialog.setWindowTitle(
            LANGUAGES[self.lang]['patient_info']['title'].format(name=patient['name'])
        )
        dialog.setFixedSize(400, 300)
        
        layout = QVBoxLayout(dialog)
        
        # Format patient information
        info_text = """
        {name}<br>
        {dob}<br>
        {blood_type}<br>
        {last_visit}
        """.format(
            name=LANGUAGES[self.lang]['patient_info']['name'].format(name=patient['name']),
            dob=LANGUAGES[self.lang]['patient_info']['dob'].format(
                dob=patient.get('date_of_birth', LANGUAGES[self.lang]['patient_info']['unknown'])
            ),
            blood_type=LANGUAGES[self.lang]['patient_info']['blood_type'].format(
                blood_type=patient.get('blood_type', LANGUAGES[self.lang]['patient_info']['unknown'])
            ),
            last_visit=LANGUAGES[self.lang]['patient_info']['last_visit'].format(
                last_visit=patient.get('last_visit', LANGUAGES[self.lang]['patient_info']['never'])
            )
        )
        
        info = QLabel(info_text)
        info.setTextFormat(Qt.RichText)
        info.setMargin(10)
        
        layout.addWidget(info)
        dialog.exec_()