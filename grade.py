import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import pymysql

conn = pymysql.connect(host='localhost', user='root', password='1234', db='project', charset='utf8')

curs = conn.cursor()

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("grade.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.btn_append.clicked.connect(self.appendFunction)
        self.btn_clear.clicked.connect(self.clearFunction)
        self.btn_search.clicked.connect(self.searchFunction)
        # clear 초기화 append 추가 toPlainText() 쓰여있는 글자 가져오기

    def appendFunction(self):
        sql = "insert into grade values('{0}','{1}','{2}','{2}','{3}','{4}')".format(self.stdno_edit.text(),self.name_edit.text(),self.date_edit.text(),self.subject_edit.text(),self.score_edit.text())
        curs.execute(sql)
        conn.commit()
        QMessageBox.about(self, "message", "추가되었습니다!")
        
    def clearFunction(self):
        self.stdno_edit.clear()
        self.name_edit.clear()
        self.date_edit.clear()
        self.subject_edit.clear()
        self.score_edit.clear()
        self.textBrowser.clear()

    def searchFunction(self):
        curs = conn.cursor(pymysql.cursors.DictCursor)
        sql = "select dateS, stdno, name, subject, score from grade where stdno = '{0}' and name = '{1}' and subject = '{2}' order by date asc".format(self.stdno_edit.text(),self.name_edit.text(),self.subject_edit.text())
        curs.execute(sql)
        rows = curs.fetchall()
        count = len(rows)
        for i in range(count):
            row = list(rows[i].values())
            self.textBrowser.append("{}, {} - {} : {} -> {}".format(row[0], row[1], row[2], row[3], row[4]))





if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()

conn.close()