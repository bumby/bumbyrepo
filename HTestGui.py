import sys
import threading
import copy

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
#from subject import *
from observer import *
from ControllerInterface import *

from OptScanController import *
from OptStatusMonitor import *
# ... 기타 필요한 모듈들 ...
import pandas as pd

class MyWindow(QMainWindow, Observer):
    def __init__(self, ControllerInterface, optdata):
        super().__init__()

        self.controller = ControllerInterface
        self.optdata = optdata  
        self.initUI()
        
        # 자신을 observer로 등록
        self.register_subject(optdata)

        # 초기 시작
        self.controller.Start(optdata)
        self.updateGuiOptHoga()

    def initUI(self):
        # Window 설정
        self.setWindowTitle('OptData Streamer')
        self.setGeometry(300, 300, 800, 600)

        # Table 설정
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setRowCount(10)
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(["단축코드", "매도호가1", "매수호가1", "이론가", "Kospi200", "HV"])
        self.tableWidget.resize(780, 500)

        # 시작 및 중지 버튼 설정
        self.startButton = QPushButton('Start', self)
        self.startButton.move(100, 550)
        self.startButton.clicked.connect(self.StartButton)

        self.stopButton = QPushButton('Stop', self)
        self.stopButton.move(600, 550)
        self.stopButton.clicked.connect(self.EndButton)

    # 기존의 update, register_subject, display, updateGuiOptHoga 메소드는 그대로 유지
    def update(self, *args, **kwargs):
        self.updateGuiOptHoga()

    def updateGuiOptHoga(self):
        # OptData에서 정보를 가져옵니다.
        optHogaChart = self.optdata.get_optChart()
        row_no = 0

        for m_optCode, optInfo in optHogaChart.items():
            # 각 row에 맞게 정보를 tableWidget에 삽입
            self.tableWidget.setItem(row_no, 0, QTableWidgetItem(m_optCode))
            self.tableWidget.setItem(row_no, 1, QTableWidgetItem(optInfo.get("offerho1", "")))
            self.tableWidget.setItem(row_no, 2, QTableWidgetItem(optInfo.get("bidho1", "")))
            self.tableWidget.setItem(row_no, 3, QTableWidgetItem(optInfo.get("theoryPrice", "")))
            self.tableWidget.setItem(row_no, 4, QTableWidgetItem(self.optdata.get_optEnvStatus("kospi200Index")))
            self.tableWidget.setItem(row_no, 5, QTableWidgetItem(self.optdata.get_optEnvStatus("HV")))
            
            row_no += 1

        # 현재 row_no가 전체 row보다 작을 경우, 나머지 행을 비움 (예: 이전 데이터가 더 많았을 경우)
        while row_no < self.tableWidget.rowCount():
            for col in range(self.tableWidget.columnCount()):
                self.tableWidget.setItem(row_no, col, QTableWidgetItem(""))
            row_no += 1
            
    def StartButton(self):
        # 데이터 스트리밍 시작 로직
        self.controller.Start()
        
    def EndButton(self):
        # 데이터 스트리밍 중지 로직
        self.controller.End()

    def closeEvent(self, event):
        print("event")
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?", QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.controller.End()
            event.accept()
        else:
            event.ignore()

# ...

if __name__=="__main__":
    app = QApplication(sys.argv)
    optdata = OptData()  # 해당 부분은 구체적인 생성 로직에 따라 다를 수 있습니다.

    # ... 생성자 및 기타 초기화 로직 ...
    optstatmon = OptStatMonitorSimul()  #data 획득 방법 xing api냐 simulation 이냐 에 따라 생성자 변경
    optscancon = OptScanContoller(optdata,optstatmon, "XingAPI")

    myWindow = MyWindow(optscancon, optdata)  # 해당 부분은 구체적인 인자에 따라 다를 수 있습니다.
    myWindow.show()
    app.exec_()
