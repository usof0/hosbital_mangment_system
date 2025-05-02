import sys
from PyQt5.QtWidgets import QApplication
from ui.login_window import LoginWindow
from ui.styles import STYLESHEET

class HospitalApp(QApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyleSheet(STYLESHEET)
        
def main():
    app = HospitalApp(sys.argv)
    
    # Set application info
    app.setApplicationName("MediCare Hospital Management System")
    app.setApplicationVersion("1.0.0")
    
    # Show login window
    login_window = LoginWindow()
    login_window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()