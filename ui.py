import sys
import json
import requests
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QComboBox, QTableWidget, QTableWidgetItem,
    QTextEdit, QTabWidget, QSpinBox, QDoubleSpinBox, QDialog, QFormLayout,
    QMessageBox, QCheckBox, QFileDialog
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QColor
import subprocess
from datetime import datetime

API_BASE = "http://localhost:5000"

class APIClient:
    @staticmethod
    def get(endpoint):
        return requests.get(f"{API_BASE}{endpoint}").json()
    
    @staticmethod
    def post(endpoint, data):
        return requests.post(f"{API_BASE}{endpoint}", json=data).json()
    
    @staticmethod
    def put(endpoint, data):
        return requests.put(f"{API_BASE}{endpoint}", json=data).json()

class ScrapeWorker(QThread):
    """Background scraper thread"""
    progress = pyqtSignal(str)
    finished = pyqtSignal()
    
    def __init__(self, program_id):
        super().__init__()
        self.program_id = program_id
    
    def run(self):
        self.progress.emit(f"Scraping program {self.program_id}...")
        try:
            job = APIClient.post('/api/scrape-queue', {'affiliate_program_id': self.program_id})
            self.progress.emit(f"Scrape job created: {job['id']}")
            self.finished.emit()
        except Exception as e:
            self.progress.emit(f"Error: {e}")
            self.finished.emit()

class Layer1Window(QMainWindow):
    """Layer 1: Affiliate Program Workspace"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Focus Worthy - Affiliate Programs (Layer 1)")
        self.setGeometry(100, 100, 1200, 700)
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Affiliate Program Manager")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Add Program Form
        form_layout = QHBoxLayout()
        form_layout.addWidget(QLabel("Program Name:"))
        self.program_name = QLineEdit()
        form_layout.addWidget(self.program_name)
        
        form_layout.addWidget(QLabel("URL:"))
        self.program_url = QLineEdit()
        form_layout.addWidget(self.program_url)
        
        form_layout.addWidget(QLabel("API Type:"))
        self.api_type = QComboBox()
        self.api_type.addItems(['html_scrape', 'json', 'xml'])
        form_layout.addWidget(self.api_type)
        
        add_btn = QPushButton("+ Add Program")
        add_btn.clicked.connect(self.add_program)
        form_layout.addWidget(add_btn)
        
        layout.addLayout(form_layout)
        
        # Programs Table
        self.programs_table = QTableWidget()
        self.programs_table.setColumnCount(5)
        self.programs_table.setHorizontalHeaderLabels(['ID', 'Name', 'URL', 'API Type', 'Action'])
        layout.addWidget(self.programs_table)
        
        # Refresh
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.load_programs)
        layout.addWidget(refresh_btn)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        self.load_programs()
    
    def load_programs(self):
        try:
            programs = APIClient.get('/api/affiliate-programs')
            self.programs_table.setRowCount(len(programs))
            for row, prog in enumerate(programs):
                self.programs_table.setItem(row, 0, QTableWidgetItem(str(prog['id'])))
                self.programs_table.setItem(row, 1, QTableWidgetItem(prog['name']))
                self.programs_table.setItem(row, 2, QTableWidgetItem(prog.get('url', '')))
                self.programs_table.setItem(row, 3, QTableWidgetItem(prog.get('api_type', '')))
                
                scrape_btn = QPushButton("Scrape")
                scrape_btn.clicked.connect(lambda checked, pid=prog['id']: self.scrape_program(pid))
                self.programs_table.setCellWidget(row, 4, scrape_btn)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load programs: {e}")
    
    def add_program(self):
        data = {
            'name': self.program_name.text(),
            'url': self.program_url.text(),
            'api_type': self.api_type.currentText()
        }
        try:
            result = APIClient.post('/api/affiliate-programs', data)
            QMessageBox.information(self, "Success", "Program added!")
            self.load_programs()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
    
    def scrape_program(self, program_id):
        self.worker = ScrapeWorker(program_id)
        self.worker.progress.connect(self.on_progress)
        self.worker.finished.connect(self.on_scrape_finished)
        self.worker.start()
    
    def on_progress(self, msg):
        QMessageBox.information(self, "Progress", msg)
    
    def on_scrape_finished(self):
        QMessageBox.information(self, "Done", "Scrape completed!")
        self.load_programs()

class Layer2Window(QMainWindow):
    """Layer 2: Affiliate Workspace (Browse, Category, Queue)"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Focus Worthy - Affiliate Workspace (Layer 2)")
        self.setGeometry(100, 100, 1400, 800)
        
        layout = QVBoxLayout()
        
        # Tabs for different views
        tabs = QTabWidget()
        
        # Tab 1: Browse Affiliate Sources
        browse_widget = self.create_browse_tab()
        tabs.addTab(browse_widget, "Browse Products")
        
        # Tab 2: COP Workspace
        cop_widget = self.create_cop_tab()
        tabs.addTab(cop_widget, "COP Products")
        
        # Tab 3: Queue
        queue_widget = self.create_queue_tab()
        tabs.addTab(queue_widget, "Scrape Queue")
        
        layout.addWidget(tabs)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
    
    def create_browse_tab(self):
        """Browse affiliate sources (immutable)"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Affiliate Source Products (Immutable)"))
        
        self.affiliate_table = QTableWidget()
        self.affiliate_table.setColumnCount(6)
        self.affiliate_table.setHorizontalHeaderLabels(['SKU', 'Name', 'Price', 'Category', 'Scraped At', 'Action'])
        layout.addWidget(self.affiliate_table)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.load_affiliate_sources)
        layout.addWidget(refresh_btn)
        
        widget.setLayout(layout)
        self.load_affiliate_sources()
        return widget
    
    def create_cop_tab(self):
        """COP workspace (editable)"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Combined Output Products (COP) - Editable"))
        
        # Filter by status
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Status:"))
        self.cop_status_filter = QComboBox()
        self.cop_status_filter.addItems(['draft', 'ready_for_launch', 'published'])
        self.cop_status_filter.currentTextChanged.connect(self.load_cop_products)
        filter_layout.addWidget(self.cop_status_filter)
        layout.addLayout(filter_layout)
        
        self.cop_table = QTableWidget()
        self.cop_table.setColumnCount(7)
        self.cop_table.setHorizontalHeaderLabels(['SKU', 'Name', 'Price', 'Category', 'Status', 'Quality', 'Action'])
        self.cop_table.itemClicked.connect(self.on_cop_product_click)
        layout.addWidget(self.cop_table)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.load_cop_products)
        layout.addWidget(refresh_btn)
        
        widget.setLayout(layout)
        self.load_cop_products()
        return widget
    
    def create_queue_tab(self):
        """Scrape queue status"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Scrape Queue"))
        
        self.queue_display = QTextEdit()
        self.queue_display.setReadOnly(True)
        layout.addWidget(self.queue_display)
        
        refresh_btn = QPushButton("Refresh Queue")
        refresh_btn.clicked.connect(self.load_queue)
        layout.addWidget(refresh_btn)
        
        widget.setLayout(layout)
        self.load_queue()
        return widget
    
    def load_affiliate_sources(self):
        try:
            sources = APIClient.get('/api/affiliate-sources')
            self.affiliate_table.setRowCount(len(sources))
            for row, src in enumerate(sources):
                self.affiliate_table.setItem(row, 0, QTableWidgetItem(src.get('sku', '')))
                self.affiliate_table.setItem(row, 1, QTableWidgetItem(src.get('product_name', '')))
                self.affiliate_table.setItem(row, 2, QTableWidgetItem(str(src.get('price', ''))))
                self.affiliate_table.setItem(row, 3, QTableWidgetItem(src.get('category', '')))
                self.affiliate_table.setItem(row, 4, QTableWidgetItem(src.get('scraped_at', '')))
                
                move_btn = QPushButton("→ COP")
                move_btn.clicked.connect(lambda checked, s=src: self.move_to_cop(s))
                self.affiliate_table.setCellWidget(row, 5, move_btn)
        except Exception as e:
            print(f"Error loading sources: {e}")
    
    def load_cop_products(self):
        try:
            status = self.cop_status_filter.currentText()
            products = APIClient.get(f'/api/cop-products?status={status}')
            self.cop_table.setRowCount(len(products))
            for row, prod in enumerate(products):
                self.cop_table.setItem(row, 0, QTableWidgetItem(prod.get('sku', '')))
                self.cop_table.setItem(row, 1, QTableWidgetItem(prod.get('product_name', '')))
                self.cop_table.setItem(row, 2, QTableWidgetItem(str(prod.get('price', ''))))
                self.cop_table.setItem(row, 3, QTableWidgetItem(prod.get('category', '')))
                self.cop_table.setItem(row, 4, QTableWidgetItem(prod.get('status', '')))
                quality = prod.get('ai_quality_score', 0)
                self.cop_table.setItem(row, 5, QTableWidgetItem(str(quality)))
                
                edit_btn = QPushButton("Edit")
                edit_btn.clicked.connect(lambda checked, p=prod: self.edit_cop_product(p))
                self.cop_table.setCellWidget(row, 6, edit_btn)
        except Exception as e:
            print(f"Error loading COP products: {e}")
    
    def move_to_cop(self, source):
        """Create COP product from affiliate source"""
        try:
            cop_data = {
                'sku': source['sku'],
                'product_name': source['product_name'],
                'description': source.get('description', ''),
                'price': source.get('price'),
                'category': source.get('category'),
                'main_image_url': source.get('image_url'),
                'affiliate_url': source.get('url'),
                'affiliate_source_id': source['id']
            }
            result = APIClient.post('/api/cop-products', cop_data)
            QMessageBox.information(self, "Success", f"Moved to COP: {result['id']}")
            self.load_cop_products()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
    
    def on_cop_product_click(self, item):
        pass
    
    def edit_cop_product(self, product):
        """Open COP product editor"""
        dialog = COPEditorDialog(product)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_cop_products()
    
    def load_queue(self):
        try:
            # Placeholder for queue status
            self.queue_display.setText("Queue status updates will appear here.\nCheck API for scrape job status.")
        except Exception as e:
            self.queue_display.setText(f"Error: {e}")

class COPEditorDialog(QDialog):
    """Edit COP product"""
    
    def __init__(self, product):
        super().__init__()
        self.product = product
        self.setWindowTitle(f"Edit: {product['product_name']}")
        self.setGeometry(200, 200, 500, 600)
        
        layout = QFormLayout()
        
        self.sku_input = QLineEdit(product.get('sku', ''))
        self.sku_input.setReadOnly(True)
        layout.addRow("SKU:", self.sku_input)
        
        self.name_input = QLineEdit(product.get('product_name', ''))
        layout.addRow("Name:", self.name_input)
        
        self.desc_input = QTextEdit()
        self.desc_input.setText(product.get('description', ''))
        layout.addRow("Description:", self.desc_input)
        
        self.price_input = QDoubleSpinBox()
        self.price_input.setValue(product.get('price', 0))
        layout.addRow("Price:", self.price_input)
        
        self.category_input = QLineEdit(product.get('category', ''))
        layout.addRow("Category:", self.category_input)
        
        self.subcategory_input = QLineEdit(product.get('subcategory', ''))
        layout.addRow("Subcategory:", self.subcategory_input)
        
        self.status_input = QComboBox()
        self.status_input.addItems(['draft', 'ready_for_launch', 'published'])
        self.status_input.setCurrentText(product.get('status', 'draft'))
        layout.addRow("Status:", self.status_input)
        
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_changes)
        layout.addRow(save_btn)
        
        self.setLayout(layout)
    
    def save_changes(self):
        try:
            data = {
                'product_name': self.name_input.text(),
                'description': self.desc_input.toPlainText(),
                'price': self.price_input.value(),
                'category': self.category_input.text(),
                'subcategory': self.subcategory_input.text(),
                'status': self.status_input.currentText()
            }
            APIClient.put(f'/api/cop-products/{self.product["id"]}', data)
            QMessageBox.information(self, "Success", "Changes saved!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

class MainWindow(QMainWindow):
    """Main launcher window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Focus Worthy - MVP Launcher")
        self.setGeometry(100, 100, 400, 300)
        
        layout = QVBoxLayout()
        
        title = QLabel("Focus Worthy MVP")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(title)
        
        layout.addWidget(QLabel("Select workspace:"))
        
        layer1_btn = QPushButton("Layer 1: Affiliate Programs")
        layer1_btn.clicked.connect(self.open_layer1)
        layout.addWidget(layer1_btn)
        
        layer2_btn = QPushButton("Layer 2: Affiliate Workspace")
        layer2_btn.clicked.connect(self.open_layer2)
        layout.addWidget(layer2_btn)
        
        start_api_btn = QPushButton("Start API Backend")
        start_api_btn.clicked.connect(self.start_api)
        layout.addWidget(start_api_btn)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
    
    def open_layer1(self):
        self.layer1 = Layer1Window()
        self.layer1.show()
    
    def open_layer2(self):
        self.layer2 = Layer2Window()
        self.layer2.show()
    
    def start_api(self):
        try:
            subprocess.Popen(['python3', 'api.py'], cwd='/home/alf/focus-worthy')
            QMessageBox.information(self, "API", "Backend started at http://localhost:5000")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to start API: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
