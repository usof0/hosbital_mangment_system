

from .needs import *

LANGUAGES = {
    'en': {
        'page_title': 'My Billing',
        'refresh_btn': 'Refresh',
        'filter_group': 'Filter Bills',
        'status_label': 'Status:',
        'from_label': 'From:',
        'to_label': 'To:',
        'apply_filters': 'Apply Filters',
        'table_headers': ["Date", "Description", "Amount", "Status", "Due Date", "Actions"],
        'payment_group': 'Payment Information',
        'total_balance': 'Total Balance: {:.2f}руб',
        'pending': 'Pending: {:.2f}руб',
        'overdue': 'Overdue: {:.2f}руб',
        'amount_label': 'Amount to Pay:',
        'method_label': 'Payment Method:',
        'pay_btn': 'Make Payment',
        'pay_now': 'Pay Now',
        'status_all': 'All Statuses',
        'status_pending': 'Pending',
        'status_paid': 'Paid',
        'status_overdue': 'Overdue',
        'payment_methods': ['Credit Card', 'Debit Card', 'Bank Transfer', 'Cash'],
        'amount_placeholder': 'Enter amount to pay',
        'payment_success': 'Payment Successful',
        'payment_success_msg': 'Payment of {:.2f}руб via {} processed successfully!',
        'error_title': 'Error',
        'amount_empty': 'Please enter payment amount',
        'amount_positive': 'Payment amount must be positive',
        'amount_invalid': 'Please enter a valid payment amount',
        'payment_failed': 'Payment failed: {}',
        'load_bills_error': 'Failed to load bills: {}',
        'no_due_date': 'N/A'
    },
    'ru': {
        'page_title': 'Мои счета',
        'refresh_btn': 'Обновить',
        'filter_group': 'Фильтр счетов',
        'status_label': 'Статус:',
        'from_label': 'От:',
        'to_label': 'До:',
        'apply_filters': 'Применить фильтры',
        'table_headers': ["Дата", "Описание", "Сумма", "Статус", "Срок оплаты", "Действия"],
        'payment_group': 'Информация об оплате',
        'total_balance': 'Общий баланс: {:.2f}руб',
        'pending': 'Ожидает: {:.2f}руб',
        'overdue': 'Просрочено: {:.2f}руб',
        'amount_label': 'Сумма к оплате:',
        'method_label': 'Способ оплаты:',
        'pay_btn': 'Оплатить',
        'pay_now': 'Оплатить сейчас',
        'status_all': 'Все статусы',
        'status_pending': 'Ожидает',
        'status_paid': 'Оплачено',
        'status_overdue': 'Просрочено',
        'payment_methods': ['Кредитная карта', 'Дебетовая карта', 'Банковский перевод', 'Наличные'],
        'amount_placeholder': 'Введите сумму для оплаты',
        'payment_success': 'Оплата успешна',
        'payment_success_msg': 'Оплата {:.2f}руб через {} выполнена успешно!',
        'error_title': 'Ошибка',
        'amount_empty': 'Пожалуйста, введите сумму оплаты',
        'amount_positive': 'Сумма оплаты должна быть положительной',
        'amount_invalid': 'Пожалуйста, введите корректную сумму оплаты',
        'payment_failed': 'Ошибка оплаты: {}',
        'load_bills_error': 'Ошибка загрузки счетов: {}',
        'no_due_date': 'Н/Д'
    }
}

class PatientBillingPage(QWidget):
    def __init__(self, user_data, db, lang='en'):
        super().__init__()
        self.user_data = user_data
        self.db = db
        self.lang = lang
        self.init_ui()
        
    def init_ui(self):
        self.setup_main_layout()
        self.setup_header()
        self.setup_filters()
        self.setup_bills_table()
        self.setup_payment_section()
        self.load_bills()
        
    def setup_main_layout(self):
        """Setup the main layout with scroll area"""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        container = QWidget()
        self.layout = QVBoxLayout(container)
        self.layout.setSpacing(20)
        
        scroll.setWidget(container)
        self.main_layout.addWidget(scroll)
        
    def setup_header(self):
        """Setup the page header"""
        header = QHBoxLayout()
        
        title = QLabel(LANGUAGES[self.lang]['page_title'])
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
        """)
        
        self.refresh_btn = QPushButton(LANGUAGES[self.lang]['refresh_btn'])
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.refresh_btn.clicked.connect(self.load_bills)
        
        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.refresh_btn)
        
        self.layout.addLayout(header)
        
    def setup_filters(self):
        """Setup filter controls"""
        group = QGroupBox(LANGUAGES[self.lang]['filter_group'])
        group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
        """)
        
        filter_layout = QHBoxLayout()
        
        # Status filter
        self.status_filter = QComboBox()
        self.status_filter.addItem(LANGUAGES[self.lang]['status_all'], "all")
        self.status_filter.addItem(LANGUAGES[self.lang]['status_pending'], "pending")
        self.status_filter.addItem(LANGUAGES[self.lang]['status_paid'], "paid")
        self.status_filter.addItem(LANGUAGES[self.lang]['status_overdue'], "overdue")
        
        # Date range filters
        self.from_date = QDateEdit()
        self.from_date.setDisplayFormat("yyyy-MM-dd")
        self.from_date.setCalendarPopup(True)
        self.from_date.setDate(QDate.currentDate().addMonths(-3))
        
        self.to_date = QDateEdit()
        self.to_date.setDisplayFormat("yyyy-MM-dd")
        self.to_date.setCalendarPopup(True)
        self.to_date.setDate(QDate.currentDate())
        
        # Filter button
        filter_btn = QPushButton(LANGUAGES[self.lang]['apply_filters'])
        filter_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        filter_btn.clicked.connect(self.load_bills)
        
        filter_layout.addWidget(QLabel(LANGUAGES[self.lang]['status_label']))
        filter_layout.addWidget(self.status_filter)
        filter_layout.addWidget(QLabel(LANGUAGES[self.lang]['from_label']))
        filter_layout.addWidget(self.from_date)
        filter_layout.addWidget(QLabel(LANGUAGES[self.lang]['to_label']))
        filter_layout.addWidget(self.to_date)
        filter_layout.addWidget(filter_btn)
        
        group.setLayout(filter_layout)
        self.layout.addWidget(group)
        
    def setup_bills_table(self):
        """Setup the bills table"""
        self.bills_table = QTableWidget()
        self.bills_table.setColumnCount(5)
        self.bills_table.setHorizontalHeaderLabels(
            LANGUAGES[self.lang]['table_headers']
        )
        self.bills_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.bills_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.bills_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.bills_table.setSelectionMode(QTableWidget.SingleSelection)
        
        self.layout.addWidget(self.bills_table)
        
    def setup_payment_section(self):
        """Setup payment section"""
        group = QGroupBox(LANGUAGES[self.lang]['payment_group'])
        group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
        """)
        
        layout = QVBoxLayout()
        
        # Summary labels
        summary_layout = QHBoxLayout()
        self.total_label = QLabel(LANGUAGES[self.lang]['total_balance'].format(0))
        self.pending_label = QLabel(LANGUAGES[self.lang]['pending'].format(0))
        self.overdue_label = QLabel(LANGUAGES[self.lang]['overdue'].format(0))
        
        for label in [self.total_label, self.pending_label, self.overdue_label]:
            label.setStyleSheet("font-size: 14px; font-weight: bold;")
            summary_layout.addWidget(label)
        
        summary_layout.addStretch()
        layout.addLayout(summary_layout)
        
        # Payment form
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignRight)
        
        self.payment_amount = QLineEdit()
        self.payment_amount.setPlaceholderText(LANGUAGES[self.lang]['amount_placeholder'])
        
        self.payment_method = QComboBox()
        self.payment_method.addItems(LANGUAGES[self.lang]['payment_methods'])
        
        pay_btn = QPushButton(LANGUAGES[self.lang]['pay_btn'])
        pay_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        pay_btn.clicked.connect(self.process_payment)
        
        form_layout.addRow(LANGUAGES[self.lang]['amount_label'], self.payment_amount)
        form_layout.addRow(LANGUAGES[self.lang]['method_label'], self.payment_method)
        form_layout.addRow("", pay_btn)
        
        layout.addLayout(form_layout)
        group.setLayout(layout)
        self.layout.addWidget(group)
        
    def load_bills(self):
        """Load bills based on current filters"""
        try:
            # Get filter values
            from_date = self.from_date.date().toString("yyyy-MM-dd")
            to_date = self.to_date.date().toString("yyyy-MM-dd")
            status = self.status_filter.currentData()
            
            # Get bills from database
            bills = self.db.get_patient_bills(
                self.user_data['id'],
                from_date=from_date,
                to_date=to_date,
                status=status if status != "all" else None
            )
            
            # Update summary
            self.update_summary(bills)
            
            # Populate table
            self.bills_table.setRowCount(len(bills))
            
            for row_idx, bill in enumerate(bills):
                date_str = bill['date'].strftime("%Y-%m-%d") if hasattr(bill['date'], 'strftime') else str(bill['date'])

                items = [
                    QTableWidgetItem(date_str),
                    QTableWidgetItem(f"Appointment number: {bill['appointment_id']}"),
                    QTableWidgetItem(f"{bill['amount']:.2f}руб"),
                    QTableWidgetItem(self.translate_status(bill['status'])),
                    QTableWidgetItem(bill.get('due_date', LANGUAGES[self.lang]['no_due_date'])),
                ]
                
                # Status styling
                if bill['status'] == 'pending':
                    items[3].setForeground(Qt.darkYellow)
                elif bill['status'] == 'paid':
                    items[3].setForeground(Qt.darkGreen)
                elif bill['status'] == 'overdue':
                    items[3].setForeground(Qt.red)
                
                # # Pay button
                # if bill['status'] in ['pending', 'overdue']:
                #     pay_btn = QPushButton(LANGUAGES[self.lang]['pay_now'])
                #     pay_btn.setStyleSheet("""
                #         QPushButton {
                #             background-color: #3498db;
                #             color: white;
                #             padding: 5px 10px;
                #             border-radius: 3px;
                #         }
                #         QPushButton:hover {
                #             background-color: #2980b9;
                #         }
                #     """)
                #     pay_btn.clicked.connect(lambda _, b=bill: self.prepare_payment(b))
                #     self.bills_table.setCellWidget(row_idx, 5, pay_btn)
                
                for col_idx, item in enumerate(items):
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self.bills_table.setItem(row_idx, col_idx, item)
            
            # self.bills_table.resizeColumnsToContents()
            
        except Exception as e:
            QMessageBox.critical(
                self, 
                LANGUAGES[self.lang]['error_title'], 
                LANGUAGES[self.lang]['load_bills_error'].format(str(e))
            )
    
    def translate_status(self, status):
        """Translate status to current language"""
        status_map = {
            'pending': LANGUAGES[self.lang]['status_pending'],
            'paid': LANGUAGES[self.lang]['status_paid'],
            'overdue': LANGUAGES[self.lang]['status_overdue']
        }
        return status_map.get(status, status.capitalize())
    
    def update_summary(self, bills):
        """Update the summary labels"""
        total = sum(b['amount'] for b in bills)
        pending = sum(b['amount'] for b in bills if b['status'] == 'pending')
        overdue = sum(b['amount'] for b in bills if b['status'] == 'overdue')
        
        self.total_label.setText(LANGUAGES[self.lang]['total_balance'].format(total))
        self.pending_label.setText(LANGUAGES[self.lang]['pending'].format(pending))
        self.overdue_label.setText(LANGUAGES[self.lang]['overdue'].format(overdue))
    
    def prepare_payment(self, bill):
        """Prepare payment for a specific bill"""
        self.payment_amount.setText(f"{bill['amount']:.2f}")
        self.bills_table.scrollToBottom()
    
    def process_payment(self):
        """Process payment for selected bills"""
        try:
            amount_text = self.payment_amount.text().strip()
            if not amount_text:
                QMessageBox.warning(
                    self, 
                    LANGUAGES[self.lang]['error_title'], 
                    LANGUAGES[self.lang]['amount_empty']
                )
                return
                
            amount = float(amount_text)
            if amount <= 0:
                QMessageBox.warning(
                    self, 
                    LANGUAGES[self.lang]['error_title'], 
                    LANGUAGES[self.lang]['amount_positive']
                )
                return
                
            method = self.payment_method.currentText()
            
            QMessageBox.information(
                self,
                LANGUAGES[self.lang]['payment_success'],
                LANGUAGES[self.lang]['payment_success_msg'].format(amount, method)
            )
            
            self.payment_amount.clear()
            
            self.load_bills()
            
        except ValueError:
            QMessageBox.warning(
                self, 
                LANGUAGES[self.lang]['error_title'], 
                LANGUAGES[self.lang]['amount_invalid']
            )
        except Exception as e:
            QMessageBox.critical(
                self, 
                LANGUAGES[self.lang]['error_title'], 
                LANGUAGES[self.lang]['payment_failed'].format(str(e))
            )