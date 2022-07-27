import sys
from PyQt5 import QtWidgets

def Pencere():

    app = QtWidgets.QApplication(sys.argv)


    pencere = QtWidgets.QWidget()
    pencere.setWindowTitle("CGNAT IP KONTROL")

    etiket1 = QtWidgets.QLabel(pencere)
    etiket1.setText("Aramak Istediginiz CGNAT IP'sini Giriniz!")
    etiket1.move(50,50)

    buton = QtWidgets.QPushButton(pencere)
    buton.setText("ARA")
    buton.move(50, 70)
    
    pencere.setGeometry(300,300,500,500)
    pencere.show()

    sys.exit(app.exec_())

Pencere()