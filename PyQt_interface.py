from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton

class SimpleInterface(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Create widgets
        self.label = QLabel('Hello, PyQt!')
        self.button = QPushButton('Click me!')

        # Set up layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        # Set the layout for the main window
        self.setLayout(layout)

        # Connect button click event to a function
        self.button.clicked.connect(self.on_button_click)

        # Set up the main window
        self.setGeometry(100, 100, 300, 200)
        self.setWindowTitle('Simple Interface')
        self.show()

    def on_button_click(self):
        self.label.setText('Button Clicked!')

if __name__ == '__main__':
    app = QApplication([])
    window = SimpleInterface()
    app.exec_()
