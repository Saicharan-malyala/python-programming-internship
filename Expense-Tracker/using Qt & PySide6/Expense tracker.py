#Dependencies
import sys
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QAction, QPainter
from PySide6.QtWidgets import (QApplication, QHeaderView, QHBoxLayout, QLabel,
                               QLineEdit, QMainWindow, QPushButton, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QWidget)
from PySide6.QtCharts import QChartView, QPieSeries, QChart

class Widget(QWidget):
    def __init__(self):
        super().__init__()

        # Dummy data
        self._data = {"water": 24, "rent": 1000, "coffee": 30}

        # Initialize item counter
        self.items = 0

        # Left Widget
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Description", "Expense"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Chart View
        self.chart_view = QChartView()
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        # QWidget Layout
        self.layout = QHBoxLayout()
        # Adding widget for left side (table)
        self.layout.addWidget(self.table)

        # Right side
        self.description = QLineEdit()
        self.expense = QLineEdit()
        self.add = QPushButton("Add")
        self.clear = QPushButton("Clear")
        self.quit = QPushButton("Quit")
        self.plot = QPushButton("Plot")

        self.right = QVBoxLayout()
        self.right.addWidget(QLabel("Description"))
        self.right.addWidget(self.description)
        self.right.addWidget(QLabel("(₹) Expense"))
        self.right.addWidget(self.expense)
        self.right.addWidget(self.add)
        self.right.addWidget(self.plot)
        self.right.addWidget(self.chart_view)
        self.right.addWidget(self.clear)
        self.right.addWidget(self.quit)

        # Adding right side layout to main layout
        self.layout.addLayout(self.right)

        # Set the layout to the QWidget
        self.setLayout(self.layout)

        # Signals and slots
        self.add.clicked.connect(self.add_element)
        self.quit.clicked.connect(self.quit_application)
        self.plot.clicked.connect(self.plot_data)
        self.clear.clicked.connect(self.clear_table)
        self.description.textChanged[str].connect(self.check_disable)
        self.expense.textChanged[str].connect(self.check_disable)

    # Add Element To the Table
    def add_element(self):
        des = self.description.text()
        expense = self.expense.text()
        try:
            expense_item = QTableWidgetItem(f"{float(expense):.2f}")
            expense_item.setTextAlignment(Qt.AlignRight)

            self.table.insertRow(self.items)
            self.table.setItem(self.items, 0, QTableWidgetItem(des))
            self.table.setItem(self.items, 1, expense_item)

            self.description.setText("")
            self.expense.setText("")
            self.items += 1
        except ValueError:
            print("That is a wrong input. Please enter a number!")

    @Slot()
    def check_disable(self):
        self.add.setEnabled(bool(self.description.text()) and bool(self.expense.text()))

    @Slot()
    def plot_data(self):
        # Get table information
        series = QPieSeries()
        for i in range(self.table.rowCount()):
            text = self.table.item(i, 0).text()
            number = float(self.table.item(i, 1).text())
            series.append(text, number)
        
        chart = QChart()
        chart.addSeries(series)
        chart.legend().setAlignment(Qt.AlignLeft)
        self.chart_view.setChart(chart)

    @Slot()
    def quit_application(self):
        QApplication.quit()

    def fill_table(self, data=None):
        data = self._data if not data else data
        for desc, exp in data.items():
            self.table.insertRow(self.items)
            self.table.setItem(self.items, 0, QTableWidgetItem(desc))
            self.table.setItem(self.items, 1, QTableWidgetItem(str(exp)))
            self.items += 1

    @Slot()
    def clear_table(self):
        self.table.setRowCount(0)
        self.items = 0


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Expense Tracker")

        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")

        # Exit QAction
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.exit_app)
        self.file_menu.addAction(exit_action)

    @Slot()
    def exit_app(self):
        QApplication.quit()


if __name__ == "__main__":
    # Qt Application
    app = QApplication(sys.argv)

    # Main window
    window = MainWindow()
    window.setCentralWidget(Widget())
    window.resize(800, 600)
    window.show()

    # Execute application
    sys.exit(app.exec())
