from .needs import *

BILLING_TRANSLATIONS = {
    'en': {
        'page_title': 'Manage Billing',
        'buttons': {
            'refresh': 'Refresh',
            'search': 'Search',
            'clear': 'Clear',
            'mark_paid': 'Mark Paid'
        },
        'filters': {
            'title': 'Search Filters',
            'patient': 'Patient:',
            'patient_placeholder': 'Patient name',
            'from_date': 'From:',
            'to_date': 'To:',
            'status': 'Status:',
            'status_options': ['All', 'pending', 'paid', 'cancelled', 'refunded']
        },
        'table_headers': [
            "ID", "Patient", "Date", "Amount", "Status", 
            "Payment Method", "Payment Date", "Appointment", "Actions"
        ],
        'summary': {
            'title': 'Financial Summary',
            'total': 'Total: ${amount:.2f}',
            'paid': 'Paid: ${amount:.2f}',
            'pending': 'Pending: ${amount:.2f}',
            'overdue': 'Overdue: ${amount:.2f}'
        },
        'messages': {
            'already_paid': 'This bill is already paid',
            'confirm_payment': 'Mark bill #{bill_id} for {patient_name} (${amount}) as paid?',
            'payment_success': 'Bill marked as paid successfully',
            'payment_error': 'Failed to update bill: {error}'
        }
    },
    'ru': {
        'page_title': 'Управление платежами',
        'buttons': {
            'refresh': 'Обновить',
            'search': 'Поиск',
            'clear': 'Очистить',
            'mark_paid': 'Отметить оплаченным'
        },
        'filters': {
            'title': 'Фильтры поиска',
            'patient': 'Пациент:',
            'patient_placeholder': 'Имя пациента',
            'from_date': 'От:',
            'to_date': 'До:',
            'status': 'Статус:',
            'status_options': ['Все', 'ожидает', 'оплачено', 'отменено', 'возврат']
        },
        'table_headers': [
            "ID", "Пациент", "Дата", "Сумма", "Статус", 
            "Метод оплаты", "Дата оплаты", "Запись", "Действия"
        ],
        'summary': {
            'title': 'Финансовая сводка',
            'total': 'Всего: {amount:.2f}₽',
            'paid': 'Оплачено: {amount:.2f}₽',
            'pending': 'Ожидает: {amount:.2f}₽',
            'overdue': 'Просрочено: {amount:.2f}₽'
        },
        'messages': {
            'already_paid': 'Этот счет уже оплачен',
            'confirm_payment': 'Отметить счет #{bill_id} для {patient_name} ({amount}₽) как оплаченный?',
            'payment_success': 'Счет успешно отмечен как оплаченный',
            'payment_error': 'Ошибка при обновлении счета: {error}'
        }
    }
}

class ManageBillingPage(QWidget):
    def __init__(self, user_data, db, lang='en'):
        super().__init__()
        self.user_data = user_data
        self.db = db
        self.lang = lang
        self.init_ui()
        
    def init_ui(self):
        self.setup_main_layout()
        self.setup_header()
        self.setup_search_filters()
        self.setup_billing_table()
        self.setup_summary_section()
        self.load_billing()
        
    def setup_main_layout(self):
        self.layout = QVBoxLayout(self)
        
    def setup_header(self):
        header = QHBoxLayout()
        
        title = QLabel(BILLING_TRANSLATIONS[self.lang]['page_title'])
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        
        refresh_btn = QPushButton(BILLING_TRANSLATIONS[self.lang]['buttons']['refresh'])
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
        """)
        refresh_btn.clicked.connect(self.load_billing)
        
        header.addWidget(title)
        header.addStretch()
        header.addWidget(refresh_btn)
        
        self.layout.addLayout(header)
        
    def setup_search_filters(self):
        filter_group = QGroupBox(BILLING_TRANSLATIONS[self.lang]['filters']['title'])
        filter_layout = QHBoxLayout()
        
        self.search_patient = QLineEdit()
        self.search_patient.setPlaceholderText(BILLING_TRANSLATIONS[self.lang]['filters']['patient_placeholder'])
        
        self.search_date_from = QDateEdit()
        self.search_date_from.setDisplayFormat("yyyy-MM-dd")
        self.search_date_from.setCalendarPopup(True)
        self.search_date_from.setDate(QDate.currentDate().addMonths(-1))
        
        self.search_date_to = QDateEdit()
        self.search_date_to.setDisplayFormat("yyyy-MM-dd")
        self.search_date_to.setCalendarPopup(True)
        self.search_date_to.setDate(QDate.currentDate())
        
        self.search_status = QComboBox()
        self.search_status.addItems(BILLING_TRANSLATIONS[self.lang]['filters']['status_options'])
        
        search_btn = QPushButton(BILLING_TRANSLATIONS[self.lang]['buttons']['search'])
        search_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        search_btn.clicked.connect(self.load_billing)
        
        clear_btn = QPushButton(BILLING_TRANSLATIONS[self.lang]['buttons']['clear'])
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #ef4444;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #dc2626;
            }
        """)
        clear_btn.clicked.connect(self.clear_search_filters)
        
        filter_layout.addWidget(QLabel(BILLING_TRANSLATIONS[self.lang]['filters']['patient']))
        filter_layout.addWidget(self.search_patient)
        filter_layout.addWidget(QLabel(BILLING_TRANSLATIONS[self.lang]['filters']['from_date']))
        filter_layout.addWidget(self.search_date_from)
        filter_layout.addWidget(QLabel(BILLING_TRANSLATIONS[self.lang]['filters']['to_date']))
        filter_layout.addWidget(self.search_date_to)
        filter_layout.addWidget(QLabel(BILLING_TRANSLATIONS[self.lang]['filters']['status']))
        filter_layout.addWidget(self.search_status)
        filter_layout.addWidget(search_btn)
        filter_layout.addWidget(clear_btn)
        
        filter_group.setLayout(filter_layout)
        self.layout.addWidget(filter_group)
        
    def setup_billing_table(self):
        self.billing_table = QTableWidget()
        self.billing_table.setColumnCount(9)
        self.billing_table.setHorizontalHeaderLabels(
            BILLING_TRANSLATIONS[self.lang]['table_headers']
        )
        self.billing_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.billing_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.billing_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        self.layout.addWidget(self.billing_table)
        
    def setup_summary_section(self):
        summary_group = QGroupBox(BILLING_TRANSLATIONS[self.lang]['summary']['title'])
        summary_layout = QHBoxLayout()
        
        self.total_label = QLabel(BILLING_TRANSLATIONS[self.lang]['summary']['total'].format(amount=0))
        self.total_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        self.paid_label = QLabel(BILLING_TRANSLATIONS[self.lang]['summary']['paid'].format(amount=0))
        self.paid_label.setStyleSheet("font-size: 16px; color: #10b981;")
        
        self.pending_label = QLabel(BILLING_TRANSLATIONS[self.lang]['summary']['pending'].format(amount=0))
        self.pending_label.setStyleSheet("font-size: 16px; color: #f59e0b;")
        
        self.overdue_label = QLabel(BILLING_TRANSLATIONS[self.lang]['summary']['overdue'].format(amount=0))
        self.overdue_label.setStyleSheet("font-size: 16px; color: #ef4444;")
        
        summary_layout.addWidget(self.total_label)
        summary_layout.addWidget(self.paid_label)
        summary_layout.addWidget(self.pending_label)
        summary_layout.addWidget(self.overdue_label)
        
        summary_group.setLayout(summary_layout)
        self.layout.addWidget(summary_group)
        
    def load_billing(self):
        filters = {
            'patient_name': self.search_patient.text(),
            'date_from': self.search_date_from.date().toString("yyyy-MM-dd"),
            'date_to': self.search_date_to.date().toString("yyyy-MM-dd"),
            'status': self.search_status.currentText() if self.search_status.currentText() != BILLING_TRANSLATIONS[self.lang]['filters']['status_options'][0] else None
        }
        
        bills = self.db.get_billing_with_details()
        self.billing_table.setRowCount(len(bills))
        
        total = 0
        paid = 0
        pending = 0
        
        for row_idx, bill in enumerate(bills):
            amount = float(bill.get('amount', 0))
            status = bill.get('status', '')
            
            total += amount
            if status == 'paid':
                paid += amount
            elif status == 'pending':
                pending += amount
            
            items = [
                QTableWidgetItem(str(bill.get('id', ''))),
                QTableWidgetItem(bill.get('patient_name', '')),
                QTableWidgetItem(bill.get('date', '')),
                QTableWidgetItem(f"{amount:.2f}₽" if self.lang == 'ru' else f"${amount:.2f}"),
                QTableWidgetItem(status),
                QTableWidgetItem(bill.get('payment_method', '')),
                QTableWidgetItem(bill.get('payment_date', '')),
                QTableWidgetItem(str(bill.get('appointment_id', '')))
            ]
            
            # Action buttons
            mark_paid_btn = QPushButton(BILLING_TRANSLATIONS[self.lang]['buttons']['mark_paid'])
            mark_paid_btn.setStyleSheet("""
                QPushButton {
                    background-color: #10b981;
                    color: white;
                    padding: 5px 10px;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #059669;
                }
            """)
            mark_paid_btn.clicked.connect(lambda _, b=bill: self.mark_bill_paid(b))
            
            btn_widget = QWidget()
            btn_layout = QHBoxLayout(btn_widget)
            btn_layout.addWidget(mark_paid_btn)
            btn_layout.setContentsMargins(0, 0, 0, 0)
            
            for col_idx, item in enumerate(items):
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.billing_table.setItem(row_idx, col_idx, item)
            
            self.billing_table.setCellWidget(row_idx, 8, btn_widget)
        
        # Update summary with proper currency
        currency_format = {
            'en': '${amount:.2f}',
            'ru': '{amount:.2f}₽'
        }
        
        self.total_label.setText(BILLING_TRANSLATIONS[self.lang]['summary']['total'].format(amount=total))
        self.paid_label.setText(BILLING_TRANSLATIONS[self.lang]['summary']['paid'].format(amount=paid))
        self.pending_label.setText(BILLING_TRANSLATIONS[self.lang]['summary']['pending'].format(amount=pending))
        self.overdue_label.setText(BILLING_TRANSLATIONS[self.lang]['summary']['overdue'].format(amount=0))
        
    def mark_bill_paid(self, bill):
        if bill['status'] == 'paid':
            QMessageBox.information(self, "Info", BILLING_TRANSLATIONS[self.lang]['messages']['already_paid'])
            return
            
        reply = QMessageBox.question(
            self, 'Confirm Payment',
            BILLING_TRANSLATIONS[self.lang]['messages']['confirm_payment'].format(
                bill_id=bill['id'],
                patient_name=bill['patient_name'],
                amount=bill['amount']
            ),
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.db.update_billing_status(bill['id'], 'paid')
                QMessageBox.information(
                    self, 
                    "Success", 
                    BILLING_TRANSLATIONS[self.lang]['messages']['payment_success']
                )
                self.load_billing()
            except Exception as e:
                QMessageBox.critical(
                    self, 
                    "Error", 
                    BILLING_TRANSLATIONS[self.lang]['messages']['payment_error'].format(error=str(e))
                )
        
    def clear_search_filters(self):
        self.search_patient.clear()
        self.search_date_from.setDate(QDate.currentDate().addMonths(-1))
        self.search_date_to.setDate(QDate.currentDate())
        self.search_status.setCurrentIndex(0)
        self.load_billing()