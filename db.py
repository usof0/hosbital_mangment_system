import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from typing import Dict, List, Optional, Union
from datetime import datetime
import os
from typing import List, Dict

from dotenv import load_dotenv

CREATE_TABLES = """
    -- Create users table
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        name VARCHAR(255) NOT NULL,
        phone VARCHAR(50),
        role VARCHAR(20) NOT NULL,
        is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
        deleted_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT users_email_key UNIQUE (email),
        CONSTRAINT users_role_check CHECK (role IN ('patient', 'doctor', 'admin'))
    );

    -- Create patients table
    CREATE TABLE patients (
        user_id INTEGER PRIMARY KEY,
        address TEXT,
        date_of_birth DATE,
        blood_type VARCHAR(10),
        insurance VARCHAR(100),
        is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
        deleted_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT patients_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT
    );

    -- Create doctors table
    CREATE TABLE doctors (
        user_id INTEGER PRIMARY KEY,
        specialization VARCHAR(100),
        department VARCHAR(100),
        from_time TIME WITHOUT TIME ZONE,
        until_time TIME WITHOUT TIME ZONE,
        is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
        deleted_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT doctors_user_id_fkey1 FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT
    );

    -- Create admins table
    CREATE TABLE admins (
        user_id INTEGER PRIMARY KEY,
        role_detail VARCHAR(100),
        is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
        deleted_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT admins_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT
    );

    -- Create appointments table
    CREATE TABLE appointments (
        id SERIAL PRIMARY KEY,
        patient_id INTEGER NOT NULL,
        doctor_id INTEGER NOT NULL,
        date DATE NOT NULL,
        time TIME WITHOUT TIME ZONE NOT NULL,
        reason TEXT,
        status VARCHAR(20) NOT NULL DEFAULT 'scheduled',
        created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
        deleted_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT appointments_status_check CHECK (status IN ('scheduled', 'completed', 'cancelled', 'no-show')),
        CONSTRAINT appointments_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES doctors(user_id) ON DELETE RESTRICT,
        CONSTRAINT appointments_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES patients(user_id) ON DELETE RESTRICT
    );

    -- Create indexes for appointments
    CREATE INDEX idx_appointments_date ON appointments(date) WHERE is_deleted = FALSE;
    CREATE INDEX idx_appointments_doctor ON appointments(doctor_id) WHERE is_deleted = FALSE;
    CREATE INDEX idx_appointments_patient ON appointments(patient_id) WHERE is_deleted = FALSE;

    -- Create billing table
    CREATE TABLE billing (
        id SERIAL PRIMARY KEY,
        patient_id INTEGER NOT NULL,
        appointment_id INTEGER,
        amount NUMERIC(10,2) NOT NULL,
        date DATE NOT NULL,
        status VARCHAR(20) NOT NULL,
        payment_method VARCHAR(50),
        payment_date TIMESTAMP WITHOUT TIME ZONE,
        is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
        deleted_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT billing_status_check CHECK (status IN ('pending', 'paid', 'cancelled', 'refunded')),
        CONSTRAINT billing_appointment_id_fkey FOREIGN KEY (appointment_id) REFERENCES appointments(id) ON DELETE RESTRICT,
        CONSTRAINT billing_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES patients(user_id) ON DELETE RESTRICT
    );

    -- Create index for billing
    CREATE INDEX idx_billing_patient ON billing(patient_id) WHERE is_deleted = FALSE;

    -- Create prescriptions table
    CREATE TABLE prescriptions (
        id SERIAL PRIMARY KEY,
        patient_id INTEGER NOT NULL,
        doctor_id INTEGER NOT NULL,
        date DATE NOT NULL,
        medication TEXT NOT NULL,
        dosage TEXT NOT NULL,
        status VARCHAR(20) NOT NULL,
        notes TEXT,
        is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
        deleted_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT prescriptions_status_check CHECK (status IN ('active', 'completed', 'cancelled')),
        CONSTRAINT prescriptions_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES doctors(user_id) ON DELETE RESTRICT,
        CONSTRAINT prescriptions_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES patients(user_id) ON DELETE RESTRICT
    );

    -- Create index for prescriptions
    CREATE INDEX idx_prescriptions_patient ON prescriptions(patient_id) WHERE is_deleted = FALSE;

    -- Create medical_records table
    CREATE TABLE medical_records (
        id SERIAL PRIMARY KEY,
        patient_id INTEGER NOT NULL,
        doctor_id INTEGER NOT NULL,
        date DATE NOT NULL,
        diagnosis TEXT NOT NULL,
        treatment TEXT,
        notes TEXT,
        is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
        deleted_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT medical_records_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES doctors(user_id) ON DELETE RESTRICT,
        CONSTRAINT medical_records_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES patients(user_id) ON DELETE RESTRICT
    );

    -- Create index for medical_records
    CREATE INDEX idx_medical_records_patient ON medical_records(patient_id) WHERE is_deleted = FALSE;

    -- Create trigger function for billing after appointment completion
    CREATE OR REPLACE FUNCTION create_billing_on_completed_appointment()
    RETURNS TRIGGER AS $$
    BEGIN
        IF NEW.status = 'completed' AND OLD.status != 'completed' THEN
            INSERT INTO billing (patient_id, appointment_id, amount, date, status)
            VALUES (NEW.patient_id, NEW.id, 100.00, NEW.date, 'pending');
            -- Note: You might want to calculate the actual amount dynamically
        END IF;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    -- Create trigger for appointments
    CREATE TRIGGER trigger_create_billing_after_completion
    AFTER UPDATE ON appointments
    FOR EACH ROW
    EXECUTE FUNCTION create_billing_on_completed_appointment();

"""

load_dotenv()  

class HospitalDatabase:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                dbname=os.getenv('DB_NAME', 'hospital_db'),
                user=os.getenv('DB_USER', 'postgres'),
                password=os.getenv('DB_PASSWORD', 'postgres'),
                host=os.getenv('DB_HOST', 'localhost'),
                port=os.getenv('DB_PORT', '5432')
            )
            # Set isolation level to handle errors gracefully
            self.conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED)
            self._initialize_db()
            self.mark_missed_appointments()
        except Exception as e:
            print(f"Error initializing database: {e}")
            raise

    def _initialize_db(self):
        """Initialize database tables if they don't exist"""
        with self.conn.cursor() as cursor:
            try:
                # Check if tables exist (using users table as indicator)
                cursor.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = 'users'
                    );
                """)
                if not cursor.fetchone()[0]:
                    self._create_tables()
            except Exception as e:
                print(f"Error checking database initialization: {e}")
                self.conn.rollback()
                raise

    def _create_tables(self):
        """Create all necessary tables with soft delete"""
        with self.conn.cursor() as cursor:
            try:
                cursor.execute(CREATE_TABLES)
                self.conn.commit()
            except Exception as e:
                print(f"Error creating tables: {e}")
                self.conn.rollback()
                raise

    def __del__(self):
        """Close database connection when object is destroyed"""
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()

    def mark_missed_appointments(self):
        """Mark past scheduled appointments as 'no-show'."""
        try:
            with self.conn.cursor() as cursor:
                query = """
                    UPDATE appointments
                    SET status = 'no-show'
                    WHERE date < CURRENT_DATE
                    AND status = 'scheduled'
                    AND is_deleted = FALSE;
                """
                cursor.execute(query)
                self.conn.commit()
        except Exception as e:
            print(f"Error marking missed appointments: {e}")

    def verify_password(self, user_id, current_pass):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                query = """
                    SELECT password
                    FROM users
                    WHERE id = %s
                """
                cursor.execute(query, (user_id,))
                result = cursor.fetchone()
                if result:
                    return result['password'] == current_pass
                else:
                    return False
            except Exception as e:
                print(f"Error getting password: {e}")
                return False

    # User management methods
    def get_user(self, email: str, password: str) -> Optional[Dict]:
        """Get user by email, password and role"""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                query = """
                    SELECT u.*, 
                           p.address, p.date_of_birth, p.blood_type, p.insurance,
                           d.specialization, d.department, d.from_time, d.until_time,
                           a.role_detail
                    FROM users u
                    LEFT JOIN patients p ON u.id = p.user_id AND u.role = 'patient' AND p.is_deleted = FALSE
                    LEFT JOIN doctors d ON u.id = d.user_id AND u.role = 'doctor' AND d.is_deleted = FALSE
                    LEFT JOIN admins a ON u.id = a.user_id AND u.role = 'admin' AND a.is_deleted = FALSE
                    WHERE u.email = %s AND u.password = %s
                    AND u.is_deleted = FALSE
                """
                cursor.execute(query, (email, password))
                return cursor.fetchone()
            except Exception as e:
                print(f"Error getting user: {e}")
                return None

    def get_patient_by_id(self, patient_id: int, include_deleted: bool = False) -> Optional[Dict]:
        """Get patient by ID"""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                deleted_clause = "" if include_deleted else "AND u.is_deleted = FALSE AND p.is_deleted = FALSE"
                query = f"""
                    SELECT u.*, p.address, p.date_of_birth, p.blood_type, p.insurance
                    FROM users u
                    JOIN patients p ON u.id = p.user_id
                    WHERE u.id = %s AND u.role = 'patient'
                    {deleted_clause}
                """
                cursor.execute(query, (patient_id,))
                return cursor.fetchone()
            except Exception as e:
                print(f"Error getting patient by ID: {e}")
                return None

    def get_patient_by_email(self, patient_email: str, include_deleted: bool = False) -> Optional[Dict]:
        """Get patient by email"""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                deleted_clause = "" if include_deleted else "AND u.is_deleted = FALSE AND p.is_deleted = FALSE"
                query = f"""
                    SELECT u.*, p.address, p.date_of_birth, p.blood_type, p.insurance
                    FROM users u
                    JOIN patients p ON u.id = p.user_id
                    WHERE u.email = %s AND u.role = 'patient'
                    {deleted_clause}
                """
                cursor.execute(query, (patient_email,))
                return cursor.fetchone()
            except Exception as e:
                print(f"Error getting patient by email: {e}")
                return None

    def get_doctor_by_id(self, doctor_id: int, include_deleted: bool = False) -> Optional[Dict]:
        """Get doctor by ID"""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                deleted_clause = "" if include_deleted else "AND u.is_deleted = FALSE AND d.is_deleted = FALSE"
                query = f"""
                    SELECT u.*, d.specialization, d.department, d.from_time, d.until_time
                    FROM users u
                    JOIN doctors d ON u.id = d.user_id
                    WHERE u.id = %s AND u.role = 'doctor'
                    {deleted_clause}
                """
                cursor.execute(query, (doctor_id,))
                return cursor.fetchone()
            except Exception as e:
                print(f"Error getting doctor by ID: {e}")
                return None

    def get_doctor_by_email(self, doctor_email: str, include_deleted: bool = False) -> Optional[Dict]:
        """Get doctor by email"""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                deleted_clause = "" if include_deleted else "AND u.is_deleted = FALSE AND d.is_deleted = FALSE"
                query = f"""
                    SELECT u.*, d.specialization, d.department, d.from_time, d.until_time
                    FROM users u
                    JOIN doctors d ON u.id = d.user_id
                    WHERE u.email = %s AND u.role = 'doctor'
                    {deleted_clause}
                """
                cursor.execute(query, (doctor_email,))
                return cursor.fetchone()
            except Exception as e:
                print(f"Error getting doctor by email: {e}")
                return None

    def get_patient_appointments(self, patient_id: int) -> List[Dict]:
        """Get all appointments for a patient"""
        appointments = List[dict]
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                query = """
                    SELECT a.*, u.name as doctor_name
                    FROM appointments a
                    JOIN doctors d ON a.doctor_id = d.user_id
                    JOIN users u ON d.user_id = u.id
                    WHERE a.patient_id = %s AND a.is_deleted = FALSE
                    ORDER BY a.date DESC, a.time DESC
                """
                cursor.execute(query, (patient_id,))
                appointments = cursor.fetchall()
                
                # Convert dates to datetime.date objects if they're strings
                for appt in appointments:
                    if isinstance(appt['date'], str):
                        appt['date'] = datetime.strptime(appt['date'], "%Y-%m-%d").date()
                    if isinstance(appt['time'], str):
                        try:
                            appt['time'] = datetime.strptime(appt['time'], "%H:%M:%S").time()
                        except ValueError:
                            appt['time'] = datetime.strptime(appt['time'], "%H:%M").time()
                return appointments
                
            except Exception as e:
                print(f"Error getting patient appointments: {e}")
                return appointments

    def get_doctor_appointments(self, doctor_id: int, include_deleted: bool = False) -> List[Dict]:
        """Get all appointments for a doctor"""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                deleted_clause = "" if include_deleted else "AND a.is_deleted = FALSE"
                query = f"""
                    SELECT a.*, u.name as patient_name
                    FROM appointments a
                    JOIN patients p ON a.patient_id = p.user_id AND p.is_deleted = FALSE
                    JOIN users u ON p.user_id = u.id AND u.is_deleted = FALSE
                    WHERE a.doctor_id = %s
                    {deleted_clause}
                    ORDER BY a.date DESC, a.time DESC
                """
                cursor.execute(query, (doctor_id,))
                return cursor.fetchall()
            except Exception as e:
                print(f"Error getting doctor appointments: {e}")
                return []

    def get_todays_appointments(self, doctor_id: int, date: str = None, include_deleted: bool = False) -> List[Dict]:
        """Get today's appointments for a doctor"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
            
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                deleted_clause = "" if include_deleted else "AND a.is_deleted = FALSE"
                query = f"""
                    SELECT a.*, u.name as patient_name
                    FROM appointments a
                    JOIN patients p ON a.patient_id = p.user_id AND p.is_deleted = FALSE
                    JOIN users u ON p.user_id = u.id AND u.is_deleted = FALSE
                    WHERE a.doctor_id = %s AND a.date = %s
                    {deleted_clause}
                    ORDER BY a.time ASC
                """
                cursor.execute(query, (doctor_id, date))
                return cursor.fetchall()
            except Exception as e:
                print(f"Error getting today's appointments: {e}")
                return []

    # Prescription methods
    def get_patient_prescriptions(self, patient_id: int, include_deleted: bool = False) -> List[Dict]:
        """Get all prescriptions for a patient"""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                deleted_clause = "" if include_deleted else "AND p.is_deleted = FALSE"
                query = f"""
                    SELECT p.*, u.name as doctor_name
                    FROM prescriptions p
                    JOIN doctors d ON p.doctor_id = d.user_id AND d.is_deleted = FALSE
                    JOIN users u ON d.user_id = u.id AND u.is_deleted = FALSE
                    WHERE p.patient_id = %s
                    {deleted_clause}
                    ORDER BY p.date DESC
                """
                cursor.execute(query, (patient_id,))
                return cursor.fetchall()
            except Exception as e:
                print(f"Error getting patient prescriptions: {e}")
                return []

    def get_active_prescriptions(self, patient_id: int, include_deleted: bool = False) -> List[Dict]:
        """Get active prescriptions for a patient"""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                deleted_clause = "" if include_deleted else "AND p.is_deleted = FALSE"
                query = f"""
                    SELECT p.*, u.name as doctor_name
                    FROM prescriptions p
                    JOIN doctors d ON p.doctor_id = d.user_id AND d.is_deleted = FALSE
                    JOIN users u ON d.user_id = u.id AND u.is_deleted = FALSE
                    WHERE p.patient_id = %s AND p.status = 'active'
                    {deleted_clause}
                    ORDER BY p.date DESC
                """
                cursor.execute(query, (patient_id,))
                return cursor.fetchall()
            except Exception as e:
                print(f"Error getting active prescriptions: {e}")
                return []

    # Medical records methods
    def get_patient_medical_records(self, patient_id: int, 
                                 from_date: str = None, 
                                 to_date: str = None, 
                                 doctor_id: int = None, 
                                 diagnosis: str = None,
                                 include_deleted: bool = False) -> List[Dict]:
        """Get filtered medical records for a patient"""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                deleted_clause = "" if include_deleted else "AND mr.is_deleted = FALSE"
                query = f"""
                    SELECT mr.*, u.name as doctor_name
                    FROM medical_records mr
                    JOIN doctors d ON mr.doctor_id = d.user_id AND d.is_deleted = FALSE
                    JOIN users u ON d.user_id = u.id AND u.is_deleted = FALSE
                    WHERE mr.patient_id = %s
                    {deleted_clause}
                """
                params = [patient_id]
                
                if from_date:
                    query += " AND mr.date >= %s"
                    params.append(from_date)
                if to_date:
                    query += " AND mr.date <= %s"
                    params.append(to_date)
                if doctor_id:
                    query += " AND mr.doctor_id = %s"
                    params.append(doctor_id)
                if diagnosis:
                    query += " AND mr.diagnosis ILIKE %s"
                    params.append(f"%{diagnosis}%")
                
                query += " ORDER BY mr.date DESC"
                cursor.execute(query, params)
                return cursor.fetchall()
            except Exception as e:
                print(f"Error getting medical records: {e}")
                return []

    # Billing methods
    def get_patient_bills(self, patient_id: int, 
                        from_date: str = None, 
                        to_date: str = None, 
                        status: str = None,
                        include_deleted: bool = False) -> List[Dict]:
        """Get filtered bills for a patient"""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                deleted_clause = "" if include_deleted else "AND b.is_deleted = FALSE"
                query = f"""
                    SELECT b.*, a.date as appointment_date, a.reason as appointment_reason
                    FROM billing b
                    LEFT JOIN appointments a ON b.appointment_id = a.id AND a.is_deleted = FALSE
                    WHERE b.patient_id = %s
                    {deleted_clause}
                """
                params = [patient_id]
                
                if from_date:
                    query += " AND b.date >= %s"
                    params.append(from_date)
                if to_date:
                    query += " AND b.date <= %s"
                    params.append(to_date)
                if status:
                    query += " AND b.status = %s"
                    params.append(status.lower())
                
                query += " ORDER BY b.date DESC"
                cursor.execute(query, params)
                return cursor.fetchall()
            except Exception as e:
                print(f"Error getting patient bills: {e}")
                return []

    def get_all_bills(self, include_deleted: bool = False) -> List[Dict]:
        """Get all bills"""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                deleted_clause = "" if include_deleted else "WHERE b.is_deleted = FALSE"
                query = f"""
                    SELECT b.*, u.name as patient_name, a.date as appointment_date
                    FROM billing b
                    JOIN patients p ON b.patient_id = p.user_id AND p.is_deleted = FALSE
                    JOIN users u ON p.user_id = u.id AND u.is_deleted = FALSE
                    LEFT JOIN appointments a ON b.appointment_id = a.id AND a.is_deleted = FALSE
                    {deleted_clause}
                    ORDER BY b.date DESC
                """
                cursor.execute(query)
                return cursor.fetchall()
            except Exception as e:
                print(f"Error getting all bills: {e}")
                return []

    # Admin methods
    def get_all_patients(self, include_deleted: bool = False) -> List[Dict]:
        """Get all patients"""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                deleted_clause = "" if include_deleted else "WHERE u.is_deleted = FALSE AND p.is_deleted = FALSE"
                query = f"""
                    SELECT u.*, p.address, p.date_of_birth, p.blood_type, p.insurance
                    FROM users u
                    JOIN patients p ON u.id = p.user_id
                    {deleted_clause} AND u.role = 'patient'
                    
                    ORDER BY u.name
                """
                cursor.execute(query)
                return cursor.fetchall()
            except Exception as e:
                print(f"Error getting all patients: {e}")
                return [] 
    
    def get_all_doctors(self, include_deleted: bool = False) -> List[Dict]:
        """Get all doctors"""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                deleted_clause = "" if include_deleted else "AND u.is_deleted = FALSE AND d.is_deleted = FALSE"
                query = f"""
                    SELECT u.*, d.specialization, d.department, d.from_time, until_time
                    FROM users u
                    JOIN doctors d ON u.id = d.user_id
                    WHERE u.role = 'doctor'
                    {deleted_clause}
                    ORDER BY u.name
                """
                cursor.execute(query)
                return cursor.fetchall()
            except Exception as e:
                print(f"Error getting all doctors: {e}")
                self.conn.rollback()
                return []


    def get_all_appointments(self, include_deleted: bool = False) -> List[Dict]:
        """Get all appointments"""        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            query = """
                UPDATE appointments
                SET status = 'no-show'
                WHERE date < CURRENT_DATE
                AND status = 'scheduled'
                AND is_deleted = FALSE;
            """
            cursor.execute(query)
            try:
                deleted_clause = "" if include_deleted else "WHERE a.is_deleted = FALSE"
                query = f"""
                    SELECT a.*, 
                           u1.name as patient_name, 
                           u2.name as doctor_name
                    FROM appointments a
                    JOIN patients p ON a.patient_id = p.user_id AND p.is_deleted = FALSE
                    JOIN users u1 ON p.user_id = u1.id AND u1.is_deleted = FALSE
                    JOIN doctors d ON a.doctor_id = d.user_id AND d.is_deleted = FALSE
                    JOIN users u2 ON d.user_id = u2.id AND u2.is_deleted = FALSE
                    {deleted_clause}
                    ORDER BY a.date DESC, a.time DESC
                """
                cursor.execute(query)
                return cursor.fetchall()
            except Exception as e:
                print(f"Error getting all appointments: {e}")
                return []
                
    def get_appointments_with_details(self, filters=None):
        """Get appointments with patient and doctor names"""
        filters = filters or {}
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                    SELECT 
                        a.id, a.date, a.time, a.reason, a.status,
                        p.user_id as patient_id, u1.name as patient_name,
                        d.user_id as doctor_id, u2.name as doctor_name
                    FROM appointments a
                    JOIN patients p ON a.patient_id = p.user_id AND p.is_deleted = FALSE
                    JOIN users u1 ON p.user_id = u1.id AND u1.is_deleted = FALSE
                    JOIN doctors d ON a.doctor_id = d.user_id AND d.is_deleted = FALSE
                    JOIN users u2 ON d.user_id = u2.id AND u2.is_deleted = FALSE
                    WHERE a.is_deleted = FALSE
                """
                
                conditions = []
                params = []
                
                if filters.get('patient_name'):
                    conditions.append("u1.name ILIKE %s")
                    params.append(f"%{filters['patient_name']}%")
                    
                if filters.get('doctor_name'):
                    conditions.append("u2.name ILIKE %s")
                    params.append(f"%{filters['doctor_name']}%")
                    
                if filters.get('date'):
                    conditions.append("a.date = %s")
                    params.append(filters['date'])
                    
                if conditions:
                    query += " AND " + " AND ".join(conditions)
                    
                query += " ORDER BY a.date DESC, a.time DESC"
                cursor.execute(query, params)
                return cursor.fetchall()
        except Exception as e:
            print(f"Error getting appointments: {e}")
            return []

    def update_appointment_status(self, appointment_id, status):
        """Update appointment status"""
        try:
            with self.conn.cursor() as cursor:
                query = """
                    UPDATE appointments 
                    SET status = %s
                    WHERE id = %s
                """
                cursor.execute(query, (status, appointment_id))
                self.conn.commit()
                return True
        except Exception as e:
            print(f"Error updating appointment status: {e}")
            self.conn.rollback()
            return False

    def get_billing_with_details(self, filters=None):
        """Get billing records with patient names"""
        filters = filters or {}
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                    SELECT 
                        b.id, b.amount, b.date, b.status, 
                        b.payment_method, b.payment_date, b.appointment_id,
                        u.name as patient_name
                    FROM billing b
                    JOIN patients p ON b.patient_id = p.user_id
                    JOIN users u ON p.user_id = u.id
                    WHERE b.is_deleted = FALSE
                """
                
                conditions = []
                params = []
                
                if filters.get('patient_name'):
                    conditions.append("u.name ILIKE %s")
                    params.append(f"%{filters['patient_name']}%")
                    
                if filters.get('date_from'):
                    conditions.append("b.date >= %s")
                    params.append(filters['date_from'])
                    
                if filters.get('date_to'):
                    conditions.append("b.date <= %s")
                    params.append(filters['date_to'])
                    
                if filters.get('status'):
                    conditions.append("b.status = %s")
                    params.append(filters['status'])
                    
                if conditions:
                    query += " AND " + " AND ".join(conditions)
                    
                query += " ORDER BY b.date DESC"
                cursor.execute(query, params)
                return cursor.fetchall()
        except Exception as e:
            print(f"Error getting billing records: {e}")
            return []


    def update_billing_status(self, billing_id, status):
        """Update billing status"""
        try:
            with self.conn.cursor() as cursor:
                query = """
                    UPDATE billing 
                    SET status = %s,
                        payment_date = CASE WHEN %s = 'paid' THEN CURRENT_TIMESTAMP ELSE payment_date END
                    WHERE id = %s
                """
                cursor.execute(query, (status, status, billing_id))
                self.conn.commit()
                return True
        except Exception as e:
            print(f"Error updating billing status: {e}")
            self.conn.rollback()
            return False


    def get_booked_times(self, doctor_id: int, date: str) -> List[str]:
        """Get booked time slots for a doctor on specific date"""
        with self.conn.cursor() as cursor:
            try:
                query = """
                    SELECT time::text as time
                    FROM appointments
                    WHERE doctor_id = %s AND date = %s AND is_deleted = FALSE
                    ORDER BY time
                """
                cursor.execute(query, (doctor_id, date))
                return [row[0][:5] for row in cursor.fetchall()]  # Extract HH:MM format
            except Exception as e:
                print(f"Error getting booked times: {e}")
                return []

    def get_all_prescriptions(self, include_deleted: bool = False) -> List[Dict]:
        """Get all prescriptions"""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                deleted_clause = "" if include_deleted else "WHERE p.is_deleted = FALSE"
                query = f"""
                    SELECT p.*, 
                           u1.name as patient_name, 
                           u2.name as doctor_name
                    FROM prescriptions p
                    JOIN patients pt ON p.patient_id = pt.user_id AND pt.is_deleted = FALSE
                    JOIN users u1 ON pt.user_id = u1.id AND u1.is_deleted = FALSE
                    JOIN doctors d ON p.doctor_id = d.user_id AND d.is_deleted = FALSE
                    JOIN users u2 ON d.user_id = u2.id AND u2.is_deleted = FALSE
                    {deleted_clause}
                    ORDER BY p.date DESC
                """
                cursor.execute(query)
                return cursor.fetchall()
            except Exception as e:
                print(f"Error getting all prescriptions: {e}")
                return []

    def get_last_doctors(self) -> List[Dict]:
        """Get last add doctors"""
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                    SELECT 
                        name,
                        email,
                        phone,
                        DATE(created_at) AS creation_date,
                        CAST(created_at AS TIME) AS creation_time
                    FROM users
                    WHERE role = 'doctor'
                    AND is_deleted = FALSE
                    AND created_at >= CURRENT_DATE - INTERVAL '7 days'
                    ORDER BY created_at DESC;
                """
                cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            print(f"Error getting last doctors: {e}")
            return []
        
    def get_last_patients(self) -> List[Dict]:
        """Get last add patients"""
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                    SELECT 
                        name,
                        email,
                        phone,
                        DATE(created_at) AS creation_date,
                        CAST(created_at AS TIME) AS creation_time
                    FROM users
                    WHERE role = 'patient'
                    AND is_deleted = FALSE
                    AND created_at >= CURRENT_DATE - INTERVAL '7 days'
                    ORDER BY created_at DESC;
                """
                cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            print(f"Error getting last patients: {e}")
            return []

    def get_last_appointments(self) -> List[Dict]:
        """Get last add appointments"""
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                    SELECT
                        u1.name AS patient_name,
                        u2.name AS doctor_name,
                        a.date,
                        a.time,
                        a.reason,
                        a.status,
                        DATE(a.created_at) AS creation_date,
                        CAST(a.created_at AS TIME) AS creation_time
                    FROM
                        appointments a
                    JOIN users u1 ON a.patient_id = u1.id
                    JOIN users u2 ON a.doctor_id = u2.id
                    WHERE
                        a.is_deleted = FALSE
                        AND DATE(a.created_at) >= CURRENT_DATE - INTERVAL '7 days'
                    ORDER BY
                        a.date DESC, a.time DESC;
                """
                cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            print(f"Error getting last appointments: {e}")
            return []

    def get_last_bills(self) -> List[Dict]:
        """Get last add bills"""
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                    SELECT
                        u.name AS patient_name,
                        b.amount,
                        b.status,
                        DATE(b.created_at) AS creation_date,
                        CAST(b.created_at AS TIME) AS creation_time
                    FROM billing b
                    JOIN users u ON b.patient_id = u.id
                    WHERE b.is_deleted = FALSE
                    AND b.created_at >= CURRENT_DATE - INTERVAL '7 days'
                    ORDER BY b.created_at DESC;
                """
                cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            print(f"Error getting last bills: {e}")
            return []

    def add_patient(self, patient_data: Dict) -> Optional[Dict]:
        """Add a new patient to the database"""
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
                # First insert the user record
                user_query = """
                    INSERT INTO users 
                    (email, password, name, phone, role, is_deleted)
                    VALUES (%s, %s, %s, %s, 'patient', FALSE)
                    RETURNING id
                """
                cursor.execute(user_query, (
                    patient_data['email'],
                    patient_data['password'],
                    patient_data['name'],
                    patient_data.get('phone')
                ))
                user_id = cursor.fetchone()['id']
                
                # Then insert the patient record
                patient_query = """
                    INSERT INTO patients 
                    (user_id, address, date_of_birth, blood_type, insurance, is_deleted)
                    VALUES (%s, %s, %s, %s, %s, FALSE)
                    RETURNING *
                """
                cursor.execute(patient_query, (
                    user_id,
                    patient_data.get('address'),
                    patient_data.get('date_of_birth'),
                    patient_data.get('blood_type'),
                    patient_data.get('insurance')
                ))
                
                # Get the complete patient record
                result = cursor.fetchone()
                self.conn.commit()
                
                # Combine user and patient data
                combined = {
                    **{k: v for k, v in patient_data.items() if k not in ['address', 'date_of_birth', 'blood_type', 'insurance']},
                    **result,
                    'id': user_id  # Use the user_id as the primary identifier
                }
                return combined
                
        except Exception as e:
            print(f"Error adding patient: {e}")
            self.conn.rollback()
            return None

    def add_doctor(self, doctor_data: Dict) -> Optional[Dict]:
        """Add a new doctor to the database"""
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
                # First insert the user record
                user_query = """
                    INSERT INTO users 
                    (email, password, name, phone, role, is_deleted)
                    VALUES (%s, %s, %s, %s, 'doctor', FALSE)
                    RETURNING id
                """
                cursor.execute(user_query, (
                    doctor_data['email'],
                    doctor_data['password'],
                    doctor_data['name'],
                    doctor_data.get('phone')
                ))
                user_id = cursor.fetchone()['id']
                
                # Then insert the doctor record
                doctor_query = """
                    INSERT INTO doctors 
                    (user_id, specialization, department, from_time, until_time, is_deleted)
                    VALUES (%s, %s, %s, %s, %s, FALSE)
                    RETURNING *
                """
                cursor.execute(doctor_query, (
                    user_id,
                    doctor_data.get('specialization'),
                    doctor_data.get('department'),
                    doctor_data.get('from_time'),
                    doctor_data.get('until_time')
                ))
                
                # Get the complete doctor record
                result = cursor.fetchone()
                self.conn.commit()
                
                # Combine user and doctor data
                combined = {
                    **{k: v for k, v in doctor_data.items() if k not in ['specialization', 'department', 'from_time', 'until_time']},
                    **result,
                    'id': user_id  # Use the user_id as the primary identifier
                }
                return combined
                
        except Exception as e:
            print(f"Error adding doctor: {e}")
            self.conn.rollback()
            return None
  
    # Add new records
    def add_appointment(self, appointment: Dict) -> Dict:
        """Add new appointment"""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                query = """
                    INSERT INTO appointments 
                    (patient_id, doctor_id, date, time, reason, status, is_deleted)
                    VALUES (%s, %s, %s, %s, %s, %s, FALSE)
                    RETURNING *
                """
                cursor.execute(query, (
                    appointment['patient_id'],
                    appointment['doctor_id'],
                    appointment['date'],
                    appointment['time'],
                    appointment['reason'],
                    appointment.get('status', 'scheduled')
                ))
                result = cursor.fetchone()
                self.conn.commit()
                return result
            except Exception as e:
                print(f"Error adding appointment: {e}")
                self.conn.rollback()
                return None

    def add_prescription(self, prescription: Dict) -> Dict:
        """Add new prescription"""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                query = """
                    INSERT INTO prescriptions 
                    (patient_id, doctor_id, date, medication, dosage, status, notes, is_deleted)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, FALSE)
                    RETURNING *
                """
                cursor.execute(query, (
                    prescription['patient_id'],
                    prescription['doctor_id'],
                    prescription['date'],
                    prescription['medication'],
                    prescription['dosage'],
                    # prescription['duration'],
                    prescription.get('status', 'active'),
                    prescription.get('notes', '')
                ))
                result = cursor.fetchone()
                self.conn.commit()
                return result
            except Exception as e:
                print(f"Error adding prescription: {e}")
                self.conn.rollback()
                return None

    def add_medical_record(self, record: Dict) -> Dict:
        """Add new medical record"""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                query = """
                    INSERT INTO medical_records 
                    (patient_id, doctor_id, date, diagnosis, treatment, notes, is_deleted)
                    VALUES (%s, %s, %s, %s, %s, %s, FALSE)
                    RETURNING *
                """
                cursor.execute(query, (
                    record['patient_id'],
                    record['doctor_id'],
                    record['date'],
                    record['diagnosis'],
                    record.get('treatment', ''),
                    record.get('notes', '')
                ))
                result = cursor.fetchone()
                self.conn.commit()
                return result
            except Exception as e:
                print(f"Error adding medical record: {e}")
                self.conn.rollback()
                return None

    def update_doctor_data(self, user_id: int, data: Dict) -> Optional[Dict]:
        """Update user and doctor fields dynamically based on input dict."""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                # Split fields into user and doctor
                user_fields = {
                    k: v for k, v in data.items()
                    if k in ['name', 'email', 'phone']
                }
                doctor_fields = {
                    k: v for k, v in data.items()
                    if k in ['specialization', 'department']
                }

                # Build dynamic UPDATE for users table
                user_update_sql = ''
                user_params = []
                if user_fields:
                    set_clauses = [f"{key} = %s" for key in user_fields.keys()]
                    user_update_sql = f"UPDATE users SET {', '.join(set_clauses)} WHERE id = %s RETURNING *"
                    user_params = list(user_fields.values()) + [user_id]

                # Build dynamic UPDATE for doctors table
                doctor_update_sql = ''
                doctor_params = []
                if doctor_fields:
                    set_clauses = [f"{key} = %s" for key in doctor_fields.keys()]
                    doctor_update_sql = f"UPDATE doctors SET {', '.join(set_clauses)} WHERE user_id = %s"
                    doctor_params = list(doctor_fields.values()) + [user_id]

                # Execute user update
                updated_user = None
                if user_update_sql:
                    cursor.execute(user_update_sql, user_params)
                    updated_user = cursor.fetchone()

                # Execute doctor update
                if doctor_update_sql:
                    cursor.execute(doctor_update_sql, doctor_params)

                self.conn.commit()

                # Fetch final result including doctor fields
                cursor.execute("""
                    SELECT u.*, d.specialization, d.department 
                    FROM users u
                    LEFT JOIN doctors d ON u.id = d.user_id
                    WHERE u.id = %s AND u.is_deleted = FALSE
                """, (user_id,))
                result = cursor.fetchone()

                return result

            except Exception as e:
                print(f"Error updating user/doctor: {e}")
                self.conn.rollback()
                return None
    
    def update_patient_data(self, user_id: int, data: Dict) -> Optional[Dict]:
        """Update user and patient fields dynamically based on input dict."""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                # Split fields
                user_fields = {
                    k: v for k, v in data.items()
                    if k in ['name', 'email', 'phone']
                }
                patient_fields = {
                    k: v for k, v in data.items()
                    if k in ['address', 'dob', 'blood_type']
                }

                # Rename 'dob' to 'date_of_birth' for database
                if 'dob' in patient_fields:
                    patient_fields['date_of_birth'] = patient_fields.pop('dob')

                # Build dynamic UPDATE for users table
                user_update_sql = ''
                user_params = []
                if user_fields:
                    set_clauses = [f"{key} = %s" for key in user_fields.keys()]
                    user_update_sql = f"UPDATE users SET {', '.join(set_clauses)} WHERE id = %s RETURNING *"
                    user_params = list(user_fields.values()) + [user_id]

                # Build dynamic UPDATE for patients table
                patient_update_sql = ''
                patient_params = []
                if patient_fields:
                    set_clauses = [f"{key} = %s" for key in patient_fields.keys()]
                    patient_update_sql = f"UPDATE patients SET {', '.join(set_clauses)} WHERE user_id = %s"
                    patient_params = list(patient_fields.values()) + [user_id]

                # Execute user update
                if user_update_sql:
                    cursor.execute(user_update_sql, user_params)

                # Execute patient update
                if patient_update_sql:
                    cursor.execute(patient_update_sql, patient_params)

                self.conn.commit()

                # Fetch final result including patient fields
                cursor.execute("""
                    SELECT u.*, p.address, p.date_of_birth, p.blood_type 
                    FROM users u
                    LEFT JOIN patients p ON u.id = p.user_id
                    WHERE u.id = %s AND u.is_deleted = FALSE
                """, (user_id,))
                result = cursor.fetchone()

                return result

            except Exception as e:
                print(f"Error updating user/patient: {e}")
                self.conn.rollback()
                return None
    def update_admin_data(self, user_id: int, data: Dict) -> Optional[Dict]:
        """Update user and admin fields dynamically based on input dict."""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                # Split fields
                user_fields = {
                    k: v for k, v in data.items()
                    if k in ['name', 'email', 'password', 'phone']
                }
                admin_fields = {
                    k: v for k, v in data.items()
                    if k in ['role_detail']
                }

                # Build dynamic UPDATE for users table
                user_update_sql = ''
                user_params = []
                if user_fields:
                    set_clauses = [f"{key} = %s" for key in user_fields.keys()]
                    user_update_sql = f"UPDATE users SET {', '.join(set_clauses)} WHERE id = %s RETURNING *"
                    user_params = list(user_fields.values()) + [user_id]

                # Build dynamic UPDATE for admins table
                admin_update_sql = ''
                admin_params = []
                if admin_fields:
                    set_clauses = [f"{key} = %s" for key in admin_fields.keys()]
                    admin_update_sql = f"UPDATE admins SET {', '.join(set_clauses)} WHERE user_id = %s"
                    admin_params = list(admin_fields.values()) + [user_id]

                # Execute user update
                if user_update_sql:
                    cursor.execute(user_update_sql, user_params)

                # Execute admin update
                if admin_update_sql:
                    cursor.execute(admin_update_sql, admin_params)

                self.conn.commit()

                # Fetch final result including admin fields
                cursor.execute("""
                    SELECT u.*, a.role_detail 
                    FROM users u
                    LEFT JOIN admins a ON u.id = a.user_id
                    WHERE u.id = %s AND u.is_deleted = FALSE
                """, (user_id,))
                result = cursor.fetchone()

                return result

            except Exception as e:
                print(f"Error updating admin: {e}")
                self.conn.rollback()
                return None
        
    def add_billing(self, bill: Dict) -> Dict:
        """Add new billing record"""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                query = """
                    INSERT INTO billing 
                    (patient_id, appointment_id, amount, date, status, is_deleted)
                    VALUES (%s, %s, %s, %s, %s, FALSE)
                    RETURNING *
                """
                cursor.execute(query, (
                    bill['patient_id'],
                    bill.get('appointment_id'),
                    bill['amount'],
                    bill['date'],
                    bill.get('status', 'pending')
                ))
                result = cursor.fetchone()
                self.conn.commit()
                return result
            except Exception as e:
                print(f"Error adding billing record: {e}")
                self.conn.rollback()
                return None

    # Update records
    def update_appointment_status(self, appointment_id: int, status: str) -> bool:
        """Update appointment status"""
        with self.conn.cursor() as cursor:
            try:
                query = """
                    UPDATE appointments
                    SET status = %s
                    WHERE id = %s AND is_deleted = FALSE
                """
                cursor.execute(query, (status, appointment_id))
                self.conn.commit()
                return cursor.rowcount > 0
            except Exception as e:
                print(f"Error updating appointment status: {e}")
                self.conn.rollback()
                return False

    def update_prescription_status(self, prescription_id: int, status: str) -> bool:
        """Update prescription status"""
        with self.conn.cursor() as cursor:
            try:
                query = """
                    UPDATE prescriptions
                    SET status = %s
                    WHERE id = %s AND is_deleted = FALSE
                """
                cursor.execute(query, (status, prescription_id))
                self.conn.commit()
                return cursor.rowcount > 0
            except Exception as e:
                print(f"Error updating prescription status: {e}")
                self.conn.rollback()
                return False

    def update_billing_status(self, bill_id: int, status: str) -> bool:
        """Update billing status"""
        with self.conn.cursor() as cursor:
            try:
                query = """
                    UPDATE billing
                    SET status = %s
                    WHERE id = %s AND is_deleted = FALSE
                """
                cursor.execute(query, (status, bill_id))
                self.conn.commit()
                return cursor.rowcount > 0
            except Exception as e:
                print(f"Error updating billing status: {e}")
                self.conn.rollback()
                return False

    # Soft delete methods
    def delete_patient(self, patient_id: int) -> bool:
        """Soft delete a patient"""
        with self.conn.cursor() as cursor:
            try:
                # First soft delete the patient record
                cursor.execute("""
                    UPDATE patients 
                    SET is_deleted = TRUE, deleted_at = CURRENT_TIMESTAMP
                    WHERE user_id = %s
                    RETURNING user_id
                """, (patient_id,))
                
                if cursor.rowcount == 0:
                    return False
                
                # Then soft delete the user record
                cursor.execute("""
                    UPDATE users 
                    SET is_deleted = TRUE, deleted_at = CURRENT_TIMESTAMP
                    WHERE id = %s AND role = 'patient'
                    RETURNING id
                """, (patient_id,))
                
                self.conn.commit()
                return cursor.rowcount > 0
            except Exception as e:
                print(f"Error soft deleting patient: {e}")
                self.conn.rollback()
                return False

    def delete_doctor(self, doctor_id: int) -> bool:
        """Soft delete a doctor"""
        with self.conn.cursor() as cursor:
            try:
                cursor.execute("""
                    UPDATE doctors 
                    SET is_deleted = TRUE, deleted_at = CURRENT_TIMESTAMP
                    WHERE user_id = %s
                    RETURNING user_id
                """, (doctor_id,))
                
                if cursor.rowcount == 0:
                    return False
                
                cursor.execute("""
                    UPDATE users 
                    SET is_deleted = TRUE, deleted_at = CURRENT_TIMESTAMP
                    WHERE id = %s AND role = 'doctor'
                    RETURNING id
                """, (doctor_id,))
                
                self.conn.commit()
                return cursor.rowcount > 0
            except Exception as e:
                print(f"Error soft deleting doctor: {e}")
                self.conn.rollback()
                return False

    def delete_appointment(self, appointment_id: int) -> bool:
        """Soft delete an appointment"""
        return self._soft_delete('appointments', appointment_id)

    def delete_prescription(self, prescription_id: int) -> bool:
        """Soft delete a prescription"""
        return self._soft_delete('prescriptions', prescription_id)

    def delete_medical_record(self, record_id: int) -> bool:
        """Soft delete a medical record"""
        return self._soft_delete('medical_records', record_id)

    def delete_billing(self, bill_id: int) -> bool:
        """Soft delete a billing record"""
        return self._soft_delete('billing', bill_id)

    def _soft_delete(self, table: str, id: int) -> bool:
        """Generic soft delete method"""
        with self.conn.cursor() as cursor:
            try:
                query = sql.SQL("""
                    UPDATE {} 
                    SET is_deleted = TRUE, deleted_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                    RETURNING id
                """).format(sql.Identifier(table))
                cursor.execute(query, (id,))
                self.conn.commit()
                return cursor.rowcount > 0
            except Exception as e:
                print(f"Error soft deleting from {table}: {e}")
                self.conn.rollback()
                return False

    # Restore methods
    def restore_patient(self, patient_id: int) -> bool:
        """Restore a soft-deleted patient"""
        with self.conn.cursor() as cursor:
            try:
                # Restore patient record
                cursor.execute("""
                    UPDATE patients 
                    SET is_deleted = FALSE, deleted_at = NULL
                    WHERE user_id = %s
                    RETURNING user_id
                """, (patient_id,))
                
                if cursor.rowcount == 0:
                    return False
                
                # Restore user record
                cursor.execute("""
                    UPDATE users 
                    SET is_deleted = FALSE, deleted_at = NULL
                    WHERE id = %s AND role = 'patient'
                    RETURNING id
                """, (patient_id,))
                
                self.conn.commit()
                return cursor.rowcount > 0
            except Exception as e:
                print(f"Error restoring patient: {e}")
                self.conn.rollback()
                return False

    def restore_doctor(self, doctor_id: int) -> bool:
        """Restore a soft-deleted doctor"""
        with self.conn.cursor() as cursor:
            try:
                cursor.execute("""
                    UPDATE doctors 
                    SET is_deleted = FALSE, deleted_at = NULL
                    WHERE user_id = %s
                    RETURNING user_id
                """, (doctor_id,))
                
                if cursor.rowcount == 0:
                    return False
                
                cursor.execute("""
                    UPDATE users 
                    SET is_deleted = FALSE, deleted_at = NULL
                    WHERE id = %s AND role = 'doctor'
                    RETURNING id
                """, (doctor_id,))
                
                self.conn.commit()
                return cursor.rowcount > 0
            except Exception as e:
                print(f"Error restoring doctor: {e}")
                self.conn.rollback()
                return False

    def restore_appointment(self, appointment_id: int) -> bool:
        """Restore a soft-deleted appointment"""
        return self._restore('appointments', appointment_id)

    def restore_prescription(self, prescription_id: int) -> bool:
        """Restore a soft-deleted prescription"""
        return self._restore('prescriptions', prescription_id)

    def restore_medical_record(self, record_id: int) -> bool:
        """Restore a soft-deleted medical record"""
        return self._restore('medical_records', record_id)

    def restore_billing(self, bill_id: int) -> bool:
        """Restore a soft-deleted billing record"""
        return self._restore('billing', bill_id)

    def _restore(self, table: str, id: int) -> bool:
        """Generic restore method"""
        with self.conn.cursor() as cursor:
            try:
                query = sql.SQL("""
                    UPDATE {} 
                    SET is_deleted = FALSE, deleted_at = NULL
                    WHERE id = %s
                    RETURNING id
                """).format(sql.Identifier(table))
                cursor.execute(query, (id,))
                self.conn.commit()
                return cursor.rowcount > 0
            except Exception as e:
                print(f"Error restoring from {table}: {e}")
                self.conn.rollback()
                return False

    # Admin methods to view deleted records
    def get_deleted_patients(self) -> List[Dict]:
        """Get all deleted patients"""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                query = """
                    SELECT u.*, p.address, p.date_of_birth, p.blood_type, p.insurance
                    FROM users u
                    JOIN patients p ON u.id = p.user_id
                    WHERE u.role = 'patient' 
                    AND (u.is_deleted = TRUE OR p.is_deleted = TRUE)
                    ORDER BY u.name
                """
                cursor.execute(query)
                return cursor.fetchall()
            except Exception as e:
                print(f"Error getting deleted patients: {e}")
                return []

    def get_deleted_doctors(self) -> List[Dict]:
        """Get all deleted doctors"""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                query = """
                    SELECT u.*, d.specialization, d.department, d.from_date, d.until_date
                    FROM users u
                    JOIN doctors d ON u.id = d.user_id
                    WHERE u.role = 'doctor' 
                    AND (u.is_deleted = TRUE OR d.is_deleted = TRUE)
                    ORDER BY u.name
                """
                cursor.execute(query)
                return cursor.fetchall()
            except Exception as e:
                print(f"Error getting deleted doctors: {e}")
                return []

    def get_deleted_appointments(self) -> List[Dict]:
        """Get all deleted appointments"""
        return self._get_deleted_records('appointments')

    def get_deleted_prescriptions(self) -> List[Dict]:
        """Get all deleted prescriptions"""
        return self._get_deleted_records('prescriptions')

    def get_deleted_medical_records(self) -> List[Dict]:
        """Get all deleted medical records"""
        return self._get_deleted_records('medical_records')

    def get_deleted_billing(self) -> List[Dict]:
        """Get all deleted billing records"""
        return self._get_deleted_records('billing')

    def _get_deleted_records(self, table: str) -> List[Dict]:
        """Generic method to get deleted records"""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                query = sql.SQL("""
                    SELECT * FROM {} 
                    WHERE is_deleted = TRUE
                    ORDER BY deleted_at DESC
                """).format(sql.Identifier(table))
                cursor.execute(query)
                return cursor.fetchall()
            except Exception as e:
                print(f"Error getting deleted records from {table}: {e}")
                return []