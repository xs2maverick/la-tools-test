import os
#basepath = 'C:\\Users\wb5888\la-tools-test\IDR_Drop'
basepath = '/home/steven/la-tools-test/IDR_Drop'
os.chdir(basepath)
print('working in directory {}.'.format(basepath))

from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
import selenium.webdriver as webdriver
from pandas.io.json import json_normalize
import datetime as dt
import pandas as pd
import numpy as np
import IDRdrop
import EPOwebscrape
#import emailscrape
import json
import math
import time
import ast
import pprint
from PyQt5.QtWidgets import QApplication, QLabel, QTableView, QMainWindow, QFrame, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5 import QtCore, QtGui

Qt = QtCore.Qt
pp = pprint.PrettyPrinter(1)
os.chdir(os.path.join(basepath, 'Logins'))

app = QApplication([])

## get login info

filename = 'email_bodies_12_31_2019.json'

with open(filename, 'r') as email:
    email = json.load(email)
    email = json.loads(email)
    
email_df = pd.DataFrame.from_dict(email)
email_df = email_df.T
email_df['date'] = pd.to_datetime(email_df['date'])
email_df.set_index('date', drop = False, inplace = True)
email_df.sort_index(inplace = True, ascending = False)
util = []

for a in email_df.accts:
    leading = a[0][:2]
    if leading == '80':
        util.append('PSNH')
    elif leading == '51':
        util.append('CLP')
    elif leading == '54':
        util.append('WMECO')
    else:
        util.append('NSTAR_NGRID')
        
email_df['util'] = util
n = email_df.shape[0]

### show downloads, filter
readpath = os.path.join(basepath, 'Downloads')
writepath = os.path.join(basepath, 'Raw_IDR')

rawfiles = IDRdrop.show_dir(readpath, 20)

#### populate table w df

"""class PandasModel(QtCore.QAbstractTableModel):
    
    #Class to populate a table view with a pandas dataframe
    
    def __init__(self, data, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return str(self._data.values[index.row()][index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._data.columns[col]
        return None"""

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self,parent)
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.setCentralWidget(self.table)
        data1 = ['row1','row2','row3','row4']
        data2 = ['1','2.0','3.00000001','3.9999999']

        self.table.setRowCount(4)

        for index in range(4):
            item1 = QTableWidgetItem(data1[index])
            self.table.setItem(index,0,item1)
            item2 = QTableWidgetItem(data2[index])
            self.table.setItem(index,1,item2)
            self.btn_sell = QPushButton('Edit')
            self.btn_sell.clicked.connect(self.handleButtonClicked)
            self.table.setCellWidget(index,2,self.btn_sell)

    def handleButtonClicked(self):
        button = QtGui.qApp.focusWidget()
        # or button = self.sender()
        index = self.table.indexAt(button.pos())
        if index.isValid():
            print(index.row(), index.column())"""

## populate logins

#model = MainWindow()
model = PandasModel(email_df)
#model.setHorizontalHeaderLabels(['IDR Drop'])
#header = model.horizontalHeader()
view = QTableView()
#view = QTableWidget()
view.setModel(model)

#add download button
def handleButtonClicked(row):
    EPOwebscrape.idr_download(row, email_df)



## download idr
files = []
for row in range(0, len(email_df.accts)):
    f = EPOwebscrape.idr_download(row, email_df)
    files.append(f)
    #btn_sell = QPushButton('Download')
    #btn_sell.clicked.connect(handleButtonClicked, row)
    #view.setCellWidget(row,5,btn_sell)
    print('done with {} of {}.'.format(row+1, len(email_df.accts)))
    print('---------------------------')

email_df['files'] = files"""

model = MainWindow()
#model = PandasModel(email_df)
#model.setHorizontalHeaderLabels(['IDR Drop'])
#header = model.horizontalHeader()
#view = QTableView()
view = QTableWidget()
view.setModel(model)

## set window/frame
w = 1080
h = 920
#frame = QFrame()
win = QMainWindow()
win.setCentralWidget(view)
win.resize(w,h)
#btn_sell.show()
win.show()
view.show()
app.exec_()