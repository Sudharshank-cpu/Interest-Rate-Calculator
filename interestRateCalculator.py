# Importing Modules
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QTreeView, QLineEdit, QMainWindow, QMessageBox, QFileDialog, QCheckBox
from PyQt5.QtGui import QStandardItem, QStandardItemModel
import matplotlib.pyplot as pyplot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as figureCanvas
import os

# Creating Main Window Class
class FinanceApp(QMainWindow):
    def __init__(self):
        # Main Window Class Created
        super(FinanceApp, self).__init__()
        self.setWindowTitle("Interest Calculator")
        self.resize(800,600)

        mainWindow = QWidget()

        # Adding Widgets
        self.rateText = QLabel("Interest Rate (%):")
        self.rateInput = QLineEdit()
        self.initialText = QLabel("Initial Investment:")
        self.initialInput = QLineEdit()
        self.yearsText = QLabel("Years to Invest:")
        self.yearsInput = QLineEdit()
        self.darkMode = QCheckBox("Dark Mode")

        self.model = QStandardItemModel()
        self.treeView = QTreeView()
        self.treeView.setModel(self.model)

        self.calcButton = QPushButton("Calculate")
        self.clearButton = QPushButton("Reset")
        self.saveButton = QPushButton("Save")

        # Events Trigger
        self.calcButton.clicked.connect(self.calculateInterest)
        self.clearButton.clicked.connect(self.resetData)
        self.saveButton.clicked.connect(self.saveSources)
        self.darkMode.stateChanged.connect(self.applyStyles)

        # Creating Matplotlib Figures to show as Graph
        self.figure = pyplot.figure()
        self.canvas = figureCanvas(self.figure)

        # Designing Layout
        self.masterLayout = QVBoxLayout()
        self.row = QHBoxLayout()
        self.row1 = QHBoxLayout()
        self.col = QVBoxLayout()
        self.col1 = QVBoxLayout()

        self.row.addWidget(self.rateText)
        self.row.addWidget(self.rateInput)
        self.row.addWidget(self.initialText)
        self.row.addWidget(self.initialInput)
        self.row.addWidget(self.yearsText)
        self.row.addWidget(self.yearsInput)
        self.row.addWidget(self.darkMode)

        self.col.addWidget(self.treeView)
        self.col.addWidget(self.calcButton)
        self.col.addWidget(self.clearButton)
        self.col.addWidget(self.saveButton)

        self.col1.addWidget(self.canvas)

        self.row1.addLayout(self.col, 30)
        self.row1.addLayout(self.col1, 70)
        
        self.masterLayout.addLayout(self.row)
        self.masterLayout.addLayout(self.row1)

        mainWindow.setLayout(self.masterLayout)
        self.setCentralWidget(mainWindow)

        # After Positioning Widgets, Applying CSS Styles
        self.applyStyles()

    # CSS Styles applied here
    def applyStyles(self):
        self.setStyleSheet('''
                           FinanceApp{
                           background-color: #f0f0f0;
                           color: #000;
                           }
                           QLabel, QLineEdit, QPushButton, QCheckBox{
                           background-color: #f8f8f8;
                           color: #000;
                           }
                           QTreeView{
                           background-color: #fff;
                           color: #000;
                           }
                           ''')
        if self.darkMode.isChecked():
            self.setStyleSheet('''
                               FinanceApp{
                               background-color: #222222;
                               }
                               QLabel, QLineEdit, QPushButton, QCheckBox{
                               background-color: #333333;
                               color: #eee;
                               }
                               QTreeView{
                               background-color: #444444;
                               color: #eee;
                               }
                               ''')

    # Interest Calculation
    def calculateInterest(self):
        initialInvestment = None
        try:
            interestRate = float(self.rateInput.text())
            initialInvestment = float(self.initialInput.text())
            numberOfYears = int(self.yearsInput.text())
        except ValueError:
            QMessageBox.warning(self,"ERROR","Invalid Input, Enter a Number")
            return

        self.model.clear()
        self.model.setHorizontalHeaderLabels(["Year", "Total"])

        total = initialInvestment
        self.model.clear()
        for year in range(1, numberOfYears+1):
            total += total * (interestRate/100)
            itemYear = QStandardItem(str(year))
            itemTotal = QStandardItem(f"{total :.2f}")
            self.model.appendRow([itemYear, itemTotal])

        self.figure.clear()
        pyplot.style.use("seaborn-v0_8")
        chart = self.figure.subplots()
        years = list(range(1, numberOfYears+1))
        totals = [initialInvestment * (1 + interestRate/100) ** year for year in years]

        chart.plot(years, totals)
        chart.set_title("Interest Chart")
        chart.set_xlabel("Year")
        chart.set_ylabel("Total")
        self.canvas.draw()

    # Resets Data    
    def resetData(self):
        self.rateInput.clear()
        self.initialInput.clear()
        self.yearsInput.clear()
        self.model.clear()
        
        self.figure.clear()
        self.canvas.draw()

    # Saves Data at "Saved" Folder
    def saveSources(self):
        dirPath = QFileDialog.getExistingDirectory(self, "Select Directory")
        if dirPath:
            folderPath = os.path.join(dirPath, "Saved")
            # os.mkdir(folderPath)  #Doesnot allows, if already existed
            os.makedirs(folderPath, exist_ok=True)  #Allow to save in Existing "Saved" Folder
            filePath = os.path.join(folderPath, "results.csv")
            with open(filePath, "w") as file:
                file.write("Year, Total \n")
                for row in range(self.model.rowCount()):
                    year = self.model.index(row, 0).data()
                    total = self.model.index(row, 1).data()
                    file.write("{}, {} \n".format(year, total))

            pyplot.savefig("Saved/chart.png")
            QMessageBox.information(self, "Save Results", "Results were saved to \"Saved\" folder!")
        else:
            QMessageBox.warning(self, "Save Results", "No Directory were selected")

# Execution of Whole Application
if __name__ == "__main__":
    app = QApplication([])
    myApp = FinanceApp()
    myApp.show()
    app.exec_()

