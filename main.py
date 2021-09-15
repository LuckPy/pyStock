import datetime

from PySide6 import QtWidgets, QtGui
from PySide6.QtPrintSupport import QPrinter
from qt_material import apply_stylesheet


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setWindowTitle("Devis Numérique")
        self.setFixedWidth(1025)
        apply_stylesheet(app, theme='dark_lightgreen.xml')

    def setup_ui(self):
        self.create_widgets()
        self.modify_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()
        self.setup_connections()
        # SETTINGS
        self.TVA = 5
        self.DEVISE = " €"

    def create_widgets(self):
        self.tablewidget_body = QtWidgets.QTableWidget()
        self.le_designation = QtWidgets.QLineEdit()
        self.le_quantity = QtWidgets.QLineEdit()
        self.le_puht = QtWidgets.QLineEdit()
        self.le_total = QtWidgets.QLineEdit()
        self.btn_add = QtWidgets.QPushButton("Ajouter")
        self.btn_reload = QtWidgets.QPushButton()
        self.lbl_total_quantity = QtWidgets.QLabel()
        self.lbl_total_price_ht = QtWidgets.QLabel()
        self.lbl_total_price_ttc = QtWidgets.QLabel()

    def modify_widgets(self):
        def initialize_table(nb_collumn, nb_row, widget_name):
            widget_name.setColumnCount(nb_collumn)
            widget_name.setRowCount(nb_row) 
            for i in range(nb_collumn):
                widget_name.setColumnWidth(i, 250)

        # TABLEWIDGET BODY
        self.tablewidget_body.setFixedHeight(500)
        initialize_table(4, 0, self.tablewidget_body)
        self.tablewidget_body.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem("DESIGNATION"))
        self.tablewidget_body.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem("QUANTITE"))
        self.tablewidget_body.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem("P.U HT"))
        self.tablewidget_body.setHorizontalHeaderItem(3, QtWidgets.QTableWidgetItem("TOTAL"))
        
        # LIGNE EDIT
        self.le_designation.setPlaceholderText("Désignation")
        self.le_quantity.setPlaceholderText("Quantité")
        self.le_puht.setPlaceholderText("P.U")
        self.le_total.setPlaceholderText("Total")
        self.le_total.setReadOnly(True)

        # BUTTON
        self.reload = self.style().standardIcon(QtWidgets.QStyle.SP_BrowserReload)
        self.btn_reload.setIcon(self.reload)

        # LABEL
        self.add_text_to_bot_labels()

    def add_text_to_bot_labels(self):
        self.lbl_total_quantity.setText("QUANTITE : ")
        self.lbl_total_price_ht.setText("TOTAL HT : ")
        self.lbl_total_price_ttc.setText("TOTAL TTC : ")

    def create_layouts(self):
        self.layout = QtWidgets.QGridLayout(self)
        self.top_layout = QtWidgets.QHBoxLayout()

    def add_widgets_to_layouts(self):
        # ADD LAYOUT TO LAYOUT
        self.layout.addLayout(self.top_layout, 0, 0, 1, 5)

        # ADD WIDGET TO LAYOUT
        self.layout.addWidget(self.tablewidget_body, 1, 0, 1, 5)
        self.top_layout.addWidget(self.le_designation)
        self.top_layout.addWidget(self.le_quantity)
        self.top_layout.addWidget(self.le_puht)
        self.top_layout.addWidget(self.le_total)
        self.top_layout.addWidget(self.btn_add)
        self.top_layout.addWidget(self.btn_reload)
        self.layout.addWidget(self.lbl_total_quantity, 2, 2, 1, 1)
        self.layout.addWidget(self.lbl_total_price_ht, 2, 3, 1, 1)
        self.layout.addWidget(self.lbl_total_price_ttc, 2, 4, 1, 1)

    def setup_connections(self):
        self.btn_add.clicked.connect(self.add_to_table)
        # self.btn_reload.clicked.connect(self.clear)
        self.btn_reload.clicked.connect(self.to_pdf)

    def add_to_table(self):
        if self.le_puht.text().isdigit() or self.le_quantity.text().isdigit():
            self.actual_row = self.tablewidget_body.rowCount()
            self.tablewidget_body.setRowCount(self.tablewidget_body.rowCount() + 1)

            designation = QtWidgets.QTableWidgetItem(self.le_designation.text().upper())
            quantity = QtWidgets.QTableWidgetItem(self.le_quantity.text())
            puht = QtWidgets.QTableWidgetItem(self.le_puht.text() + self.DEVISE)  

            self.tablewidget_body.setItem(self.actual_row, 0, designation)        
            self.tablewidget_body.setItem(self.actual_row, 1,  quantity)         
            self.tablewidget_body.setItem(self.actual_row, 2,  puht)  

            puht, quantity = float(self.le_puht.text()), int(self.le_quantity.text())  
            total = QtWidgets.QTableWidgetItem(str(round((puht * quantity), 2)) + self.DEVISE)                        
            self.tablewidget_body.setItem(self.actual_row, 3,  total)
            
            self.total_sum()

    def total_sum(self):
        rows = self.tablewidget_body.rowCount()
        cols = self.tablewidget_body.columnCount()
        quantity = sum(int(self.tablewidget_body.item(i, 1).text()) for i in range(rows))
        total_ht = [(self.tablewidget_body.item(i, 2).text().split(" "))[0] for i in range(rows)]
        total_ht = round((sum(float(i) for i in total_ht)), 2)
        total_ttc = round((float(total_ht + (total_ht * (self.TVA/100)))), 2)
      
        self.lbl_total_quantity.setText("QUANTITE : " + str(quantity))
        self.lbl_total_price_ht.setText("TOTAL HT : " + str(total_ht) + self.DEVISE)
        self.lbl_total_price_ttc.setText("TOTAL TTC : " + str(total_ttc) + self.DEVISE)

    def clear(self):
        self.tablewidget_body.setRowCount(0)
        self.lbl_total_price_ht.clear()
        self.lbl_total_price_ttc.clear()
        self.lbl_total_quantity.clear()
        self.add_text_to_bot_labels()


app = QtWidgets.QApplication([])
window = MainWindow()
window.show()
app.exec_()
 
