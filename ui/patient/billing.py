from .needs import *

class PatientBillingPage(QWidget):
    def __init__(self, user_data, db):
        super().__init__()
        self.user_data = user_data
        self.db = db
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
        
        title = QLabel("My Billing")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
        """)
        
        self.refresh_btn = QPushButton("Refresh")
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
        group = QGroupBox("Filter Bills")
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
        self.status_filter.addItem("All Statuses", "all")
        self.status_filter.addItem("Pending", "pending")
        self.status_filter.addItem("Paid", "paid")
        self.status_filter.addItem("Overdue", "overdue")
        
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
        filter_btn = QPushButton("Apply Filters")
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
        
        filter_layout.addWidget(QLabel("Status:"))
        filter_layout.addWidget(self.status_filter)
        filter_layout.addWidget(QLabel("From:"))
        filter_layout.addWidget(self.from_date)
        filter_layout.addWidget(QLabel("To:"))
        filter_layout.addWidget(self.to_date)
        filter_layout.addWidget(filter_btn)
        
        group.setLayout(filter_layout)
        self.layout.addWidget(group)
        
    def setup_bills_table(self):
        """Setup the bills table"""
        self.bills_table = QTableWidget()
        self.bills_table.setColumnCount(6)
        self.bills_table.setHorizontalHeaderLabels(
            ["Date", "Description", "Amount", "Status", "Due Date", "Actions"]
        )
        self.bills_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.bills_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.bills_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.bills_table.setSelectionMode(QTableWidget.SingleSelection)
        
        self.layout.addWidget(self.bills_table)
        
    def setup_payment_section(self):
        """Setup payment section"""
        group = QGroupBox("Payment Information")
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
        self.total_label = QLabel("Total Balance: $0.00")
        self.pending_label = QLabel("Pending: $0.00")
        self.overdue_label = QLabel("Overdue: $0.00")
        
        for label in [self.total_label, self.pending_label, self.overdue_label]:
            label.setStyleSheet("font-size: 14px; font-weight: bold;")
            summary_layout.addWidget(label)
        
        summary_layout.addStretch()
        layout.addLayout(summary_layout)
        
        # Payment form
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignRight)
        
        self.payment_amount = QLineEdit()
        self.payment_amount.setPlaceholderText("Enter amount to pay")
        
        self.payment_method = QComboBox()
        self.payment_method.addItems(["Credit Card", "Debit Card", "Bank Transfer", "Cash"])
        
        pay_btn = QPushButton("Make Payment")
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
        
        form_layout.addRow("Amount to Pay:", self.payment_amount)
        form_layout.addRow("Payment Method:", self.payment_method)
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
                items = [
                    QTableWidgetItem(bill['date']),
                    QTableWidgetItem(f"Appointment number: {bill['appointment_id']}"),
                    QTableWidgetItem(f"${bill['amount']:.2f}"),
                    QTableWidgetItem(bill['status'].capitalize()),
                    QTableWidgetItem(bill.get('due_date', 'N/A')),
                ]
                
                # Status styling
                if bill['status'] == 'pending':
                    items[3].setForeground(Qt.darkYellow)
                elif bill['status'] == 'paid':
                    items[3].setForeground(Qt.darkGreen)
                elif bill['status'] == 'overdue':
                    items[3].setForeground(Qt.red)
                
                # Pay button
                if bill['status'] in ['pending', 'overdue']:
                    pay_btn = QPushButton("Pay Now")
                    pay_btn.setStyleSheet("""
                        QPushButton {
                            background-color: #3498db;
                            color: white;
                            padding: 5px 10px;
                            border-radius: 3px;
                        }
                        QPushButton:hover {
                            background-color: #2980b9;
                        }
                    """)
                    pay_btn.clicked.connect(lambda _, b=bill: self.prepare_payment(b))
                    self.bills_table.setCellWidget(row_idx, 5, pay_btn)
                
                for col_idx, item in enumerate(items):
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self.bills_table.setItem(row_idx, col_idx, item)
            
            self.bills_table.resizeColumnsToContents()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load bills: {str(e)}")
    
    def update_summary(self, bills):
        """Update the summary labels"""
        total = sum(b['amount'] for b in bills)
        pending = sum(b['amount'] for b in bills if b['status'] == 'pending')
        overdue = sum(b['amount'] for b in bills if b['status'] == 'overdue')
        
        self.total_label.setText(f"Total Balance: ${total:.2f}")
        self.pending_label.setText(f"Pending: ${pending:.2f}")
        self.overdue_label.setText(f"Overdue: ${overdue:.2f}")
    
    def prepare_payment(self, bill):
        """Prepare payment for a specific bill"""
        self.payment_amount.setText(f"{bill['amount']:.2f}")
        self.bills_table.scrollToBottom()
    
    def process_payment(self):
        """Process payment for selected bills"""
        try:
            amount_text = self.payment_amount.text().strip()
            if not amount_text:
                QMessageBox.warning(self, "Error", "Please enter payment amount")
                return
                
            amount = float(amount_text)
            if amount <= 0:
                QMessageBox.warning(self, "Error", "Payment amount must be positive")
                return
                
            method = self.payment_method.currentText()
            
            # In a real app, this would process payment through a payment gateway
            QMessageBox.information(
                self,
                "Payment Successful",
                f"Payment of ${amount:.2f} via {method} processed successfully!"
            )
            
            # Reset form
            self.payment_amount.clear()
            
            # Refresh bills
            self.load_bills()
            
        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter a valid payment amount")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Payment failed: {str(e)}")