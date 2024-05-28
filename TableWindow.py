import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QVBoxLayout, QPushButton, \
    QTableWidgetItem, QTabWidget, QInputDialog
from PyQt5.QtGui import QKeySequence
from Dataset import Dataset
from PyQt5.QtCore import pyqtSignal

class TableWindow(QWidget):
    collect_data_signal = pyqtSignal(bool)
    def __init__(self):
        super().__init__()

        self.init_ui()
        self.datasets = []


    def init_ui(self):
        self.setWindowTitle('Table Window')

        self.tab_widget = QTabWidget()

        self.resize(800, 600)  # Set width and height of the window

        self.add_tab()

        self.add_button = QPushButton('Add Tab')
        self.add_button.clicked.connect(self.add_tab)
        self.add_button.setVisible(False)

        self.store_button = QPushButton('Collect data from table.')
        self.store_button.clicked.connect(self.store_data_to_dataframes)

        layout = QVBoxLayout()
        layout.addWidget(self.tab_widget)
        layout.addWidget(self.add_button)
        layout.addWidget(self.store_button)

        self.setLayout(layout)

    def add_tab(self):
        table_widget = QTableWidget()
        table_widget.setRowCount(5)
        table_widget.setColumnCount(2)
        column_labels = ['x', 'y']
        table_widget.setHorizontalHeaderLabels(column_labels)
        # table_widget.horizontalHeader().sectionDoubleClicked.connect(self.rename_column)
        self.tab_widget.addTab(table_widget, f'Table {self.tab_widget.count()}')
        self.tab_widget.tabBar().tabBarDoubleClicked.connect(self.rename_tab)

    # def rename_column(self, index):
    #     new_name, ok = QInputDialog.getText(self, "Rename Column", "Enter new name:")
    #     if ok:
    #         self.tab_widget.currentWidget().horizontalHeaderItem(index).setText(new_name)

    def rename_tab(self, index):
        new_name, ok = QInputDialog.getText(self, "Rename Tab", "Enter new name:")
        if ok:
            self.tab_widget.setTabText(index, new_name)

    def store_data_to_dataframes(self):
        for index in range(self.tab_widget.count()):
            current_table = self.tab_widget.widget(index)
            tab_name = self.tab_widget.tabText(index)
            rows = current_table.rowCount()
            cols = current_table.columnCount()
            data = []
            for row in range(rows):
                row_data = []
                for col in range(cols):
                    item = current_table.item(row, col)
                    if item is not None:
                        row_data.append(item.text())
                    else:
                        row_data.append('')
                data.append(row_data)
            # INit dataset object:
            self.datasets.append(Dataset(data, tab_name))


            # Emit the signal
        self.collect_data_signal.emit(True)
        self.close() # Close table window.

        # print("Data stored to Pandas DataFrames:")
        # for ds in self.datasets:
        #     print(f"DataFrame for '{ds.tab_name}':")
        #     print(ds.df)

    def paste_data(self, clipboard_data):
        current_index = self.tab_widget.currentIndex()
        current_table = self.tab_widget.widget(current_index)

        rows = len(clipboard_data)
        cols = len(clipboard_data[0])

        current_table.setRowCount(rows)
        current_table.setColumnCount(cols)

        for row in range(rows):
            for col in range(cols):
                item = QTableWidgetItem(str(clipboard_data[row][col]))
                current_table.setItem(row, col, item)

    def resize_rows(self):
        current_index = self.tab_widget.currentIndex()
        current_table = self.tab_widget.widget(current_index)

        current_table.resizeRowsToContents()

    def keyPressEvent(self, event):
        if event.matches(QKeySequence.Paste):
            clipboard = QApplication.clipboard()
            mime_data = clipboard.mimeData()
            if mime_data.hasText():
                clipboard_text = mime_data.text()
                clipboard_data = [line.split('\t') for line in clipboard_text.split('\n')]
                self.paste_data(clipboard_data)


