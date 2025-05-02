import json
import os
from typing import Dict, List, Optional, Union
from datetime import datetime

class HospitalDatabase:
    def __init__(self, db_file: str = 'database.json'):
        self.db_file = db_file
        self.data = self._load_data()
        
    def _load_data(self) -> Dict:
        """Load data from JSON file or create new if doesn't exist"""
        if not os.path.exists(self.db_file):
            # Initialize with empty database structure
            initial_data = {
                "users": {
                    "patients": [],
                    "doctors": [],
                    "admins": []
                },
                "appointments": [],
                "prescriptions": [],
                "medical_records": [],
                "billing": []
            }
            self._save_data(initial_data)
            return initial_data
        
        with open(self.db_file, 'r') as f:
            return json.load(f)
            
    def _save_data(self, data: Dict) -> None:
        """Save data to JSON file"""
        with open(self.db_file, 'w') as f:
            json.dump(data, f, indent=2)
            
    # User management methods
    def get_user(self, email: str, password: str, role: str) -> Optional[Dict]:
        """Get user by email, password and role"""
        role_key = f"{role}s"  # patient -> patients, doctor -> doctors
        users = self.data['users'].get(role_key, [])
        
        for user in users:
            if user['email'] == email and user['password'] == password:
                return user
        return None
        
    def get_patient_by_id(self, patient_id: int) -> Optional[Dict]:
        """Get patient by ID"""
        for patient in self.data['users']['patients']:
            if patient['id'] == patient_id:
                return patient
        return None
        
    def get_doctor_by_id(self, doctor_id: int) -> Optional[Dict]:
        """Get doctor by ID"""
        for doctor in self.data['users']['doctors']:
            if doctor['id'] == doctor_id:
                return doctor
        return None
        
    # Appointment methods
    def get_patient_appointments(self, patient_id: int) -> List[Dict]:
        """Get all appointments for a patient"""
        return [appt for appt in self.data['appointments'] 
                if appt['patient_id'] == patient_id]
                
    def get_doctor_appointments(self, doctor_id: int) -> List[Dict]:
        """Get all appointments for a doctor"""
        return [appt for appt in self.data['appointments'] 
                if appt['doctor_id'] == doctor_id]
                
    def get_todays_appointments(self, doctor_id: int, date: str = None) -> List[Dict]:
        """Get today's appointments for a doctor"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        return [appt for appt in self.data['appointments'] 
                if appt['doctor_id'] == doctor_id and appt['date'] == date]
                
    # Prescription methods
    def get_patient_prescriptions(self, patient_id: int) -> List[Dict]:
        """Get all prescriptions for a patient"""
        return [presc for presc in self.data['prescriptions'] 
                if presc['patient_id'] == patient_id]
                
    def get_active_prescriptions(self, patient_id: int) -> List[Dict]:
        """Get active prescriptions for a patient"""
        return [presc for presc in self.data['prescriptions'] 
                if presc['patient_id'] == patient_id and presc['status'] == 'active']
                
    # Medical records methods
    # def get_patient_medical_records(self, patient_id: int) -> List[Dict]:
    #     """Get all medical records for a patient"""
    #     return [record for record in self.data['medical_records'] 
    #             if record['patient_id'] == patient_id]
    def get_patient_medical_records(self, patient_id: int, 
                                from_date: str = None, 
                                to_date: str = None, 
                                doctor_id: int = None, 
                                diagnosis: str = None) -> List[Dict]:
        """Get filtered medical records for a patient"""
        records = [record for record in self.data['medical_records'] 
                if record['patient_id'] == patient_id]
        
        # Apply filters
        if from_date:
            records = [r for r in records if r['date'] >= from_date]
        if to_date:
            records = [r for r in records if r['date'] <= to_date]
        if doctor_id:
            records = [r for r in records if r['doctor_id'] == doctor_id]
        if diagnosis:
            records = [r for r in records if r['diagnosis'] == diagnosis]
        
        return records
                
    # Billing methods
    def get_patient_bills(self, patient_id: int, 
                        from_date: str = None, 
                        to_date: str = None, 
                        status: str = None) -> List[Dict]:
        """Get filtered bills for a patient"""
        bills = [bill for bill in self.data['billing'] 
                if bill['patient_id'] == patient_id]
        
        # Apply date filters if provided
        if from_date:
            bills = [b for b in bills if b['date'] >= from_date]
        if to_date:
            bills = [b for b in bills if b['date'] <= to_date]
        
        # Apply status filter if provided
        if status:
            bills = [b for b in bills if b['status'].lower() == status.lower()]
        
        return bills
    
    def get_all_bills(self) -> List[Dict]:
        return [bill for bill in self.data['billing']]
                
    # Admin methods
    def get_all_patients(self) -> List[Dict]:
        """Get all patients"""
        return self.data['users']['patients']
        
    def get_all_doctors(self) -> List[Dict]:
        """Get all doctors"""
        return self.data['users']['doctors']
        
    def get_all_appointments(self) -> List[Dict]:
        """Get all appointments"""
        return self.data['appointments']
        
    def get_all_prescriptions(self) -> List[Dict]:
        """Get all prescriptions"""
        return self.data['prescriptions']
        
    # Add new records
    def add_appointment(self, appointment: Dict) -> Dict:
        """Add new appointment"""
        appointment['id'] = len(self.data['appointments']) + 1
        self.data['appointments'].append(appointment)
        self._save_data(self.data)
        return appointment
        
    def add_prescription(self, prescription: Dict) -> Dict:
        """Add new prescription"""
        prescription['id'] = len(self.data['prescriptions']) + 1
        self.data['prescriptions'].append(prescription)
        self._save_data(self.data)
        return prescription
        
    def add_medical_record(self, record: Dict) -> Dict:
        """Add new medical record"""
        record['id'] = len(self.data['medical_records']) + 1
        self.data['medical_records'].append(record)
        self._save_data(self.data)
        return record
        
    def add_billing(self, bill: Dict) -> Dict:
        """Add new billing record"""
        bill['id'] = len(self.data['billing']) + 1
        self.data['billing'].append(bill)
        self._save_data(self.data)
        return bill
        
    # Update records
    def update_appointment_status(self, appointment_id: int, status: str) -> bool:
        """Update appointment status"""
        for appt in self.data['appointments']:
            if appt['id'] == appointment_id:
                appt['status'] = status
                self._save_data(self.data)
                return True
        return False
        
    def update_prescription_status(self, prescription_id: int, status: str) -> bool:
        """Update prescription status"""
        for presc in self.data['prescriptions']:
            if presc['id'] == prescription_id:
                presc['status'] = status
                self._save_data(self.data)
                return True
        return False
        
    def update_billing_status(self, bill_id: int, status: str) -> bool:
        """Update billing status"""
        for bill in self.data['billing']:
            if bill['id'] == bill_id:
                bill['status'] = status
                self._save_data(self.data)
                return True
        return False