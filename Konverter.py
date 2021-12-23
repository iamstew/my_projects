import pandas # pip install pandas
import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
class Konv(QMainWindow):
	def __init__(self, parent = None):
		super().__init__()

		aaa = None
		self.plainTextEdit = QPlainTextEdit()
		QToolTip.setFont(QFont('Calibri', 10))

		getFileNameButton = QPushButton("Выбрать файл", self)
		getFileNameButton.pressed.connect(self.getFileName)

		saveFileNameButton = QPushButton("Конвертировать и сохранить файл")
		saveFileNameButton.pressed.connect(self.saveFile)
		
		layoutV = QVBoxLayout()
		layoutV.addWidget(getFileNameButton)
		layoutV.addWidget(saveFileNameButton)

		layoutH = QHBoxLayout()
		layoutH.addLayout(layoutV)
		layoutH.addWidget(self.plainTextEdit)

		centerWidget = QWidget()
		centerWidget.setLayout(layoutH) 
		self.setCentralWidget(centerWidget)
		
		self.setGeometry(0, 0, 740, 480)
		self.setWindowTitle('Конвертер')
		self.setWindowIcon(QIcon('k.png'))

	def getFileName(self):
		filename, filetype = QFileDialog.getOpenFileName(self,
							 "Выбрать файл",
							 ".",
							 "JSON files(*.json)")
		global aaa
		aaa = pandas.read_json(f'{filename}')
		self.plainTextEdit.appendHtml("<br>Выбрали файл: <b>{}</b> <br> <b>{:*^54}</b>"
									 "".format(filename, filetype))

	def saveFile(self):
		filename, ok = QFileDialog.getSaveFileName(self,
							 "Сохранить файл",
							 ".",
							 "Таблица Excel(*.xlsx*)")
		global aaa 
		aaa.to_excel(f'{filename}')
		self.plainTextEdit.appendHtml("<br>Сохранить файл: <b>{}</b> <br> <b>{:*^54}</b>"
									  "".format(filename, ok))

if __name__ == '__main__':

	app = QApplication(sys.argv)
	ex = Konv()
	ex.show()
	sys.exit(app.exec_())