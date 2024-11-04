from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
from ERP_vue_dossier.employe_hr import EmployeHRWindow
from ERP_vue_dossier.commandes_hr import CommandesHRWindow

class qHRWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.setStyleSheet("QPushButton{padding: 10px; background-color:white; border:2px solid black;} QPushButton:pressed{background-color:#cacccf;}")

        # Title and Layout
        self.setWindowTitle("Gestion des Ressources Humaines")
        layout = QVBoxLayout()

        # Navigation Buttons
        button_layout = QHBoxLayout()

        employe_button = QPushButton("Employés")
        employe_button.clicked.connect(self.open_employe_hr)
        button_layout.addWidget(employe_button)

        commandes_button = QPushButton("Commandes")
        commandes_button.clicked.connect(self.open_commandes_hr)
        button_layout.addWidget(commandes_button)

        # Back Button
        back_button = QPushButton("<-")
        back_button.clicked.connect(parent.basculer_before)

        # Add Layouts and Improve Organization
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def open_employe_hr(self):
        self.close()
        self.employe_window = EmployeHRWindow()
        self.employe_window.show()

    def open_commandes_hr(self):
        self.close()
        self.commandes_window = CommandesHRWindow()
        self.commandes_window.show()

    def emit_back_signal(self):
        self.backButtonPressed.emit()  # Emit the custom signal for back