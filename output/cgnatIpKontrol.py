import ipaddress, os, sys
from PyQt5.QtWidgets import *
#from PyQt5.QtGui import *
from PyQt5.QtCore import *

cgnatIpAdresi = []
cgnatIpAdresiDegil = []

class sonucPenceresi(QWidget):
    def __init__(self):
        super().__init__()
        global cgnatIpAdresi
        global cgnatIpAdresiDegil
        self.init_ui()

    def init_ui(self):
        v_layout1 = QVBoxLayout()
        h_layout1 = QHBoxLayout()
        h_layout2 = QHBoxLayout()
        h_layout3 = QHBoxLayout()
        h_layout4 = QHBoxLayout()
        h_layout5 = QHBoxLayout()

        self.hlabel1 = QLabel("<h1>CGNAT IP KONTROL SONUCU:</h1>")
        self.hlabel1.setAlignment(Qt.AlignCenter)
        v_layout1.addWidget(self.hlabel1)

        self.hlabel2 = QLabel("")
        v_layout1.addWidget(self.hlabel2)

        self.label3 = QLabel("<h3>CGNAT OLAN IPLER:</h3>")
        h_layout1.addWidget(self.label3)
        #h_layout1.addStretch()

        self.label4 = QLabel("<h3>CGNAT OLMAYAN IPLER:</h3>")
        h_layout1.addWidget(self.label4)

        self.cgnatOlanTextWidget = QTextEdit()
        h_layout2.addWidget(self.cgnatOlanTextWidget)
        policy = self.cgnatOlanTextWidget.sizePolicy()
        policy.setVerticalStretch(1)
        self.cgnatOlanTextWidget.setSizePolicy(policy)
        #h_layout2.addStretch()

        self.cgnatOlmayanTextWidget = QTextEdit()
        h_layout2.addWidget(self.cgnatOlmayanTextWidget)

        self.hlabel5 = QLabel("")
        h_layout3.addWidget(self.hlabel5)

        h_layout4.addStretch()
        self.buttonKaydet = QPushButton("KAYDET")
        self.buttonKaydet.clicked.connect(self.kaydet)
        h_layout4.addWidget(self.buttonKaydet)


        v_layout1.addLayout(h_layout1)
        v_layout1.addLayout(h_layout2)
        v_layout1.addStretch()
        v_layout1.addLayout(h_layout3)
        v_layout1.addStretch()
        v_layout1.addLayout(h_layout4)
        self.setLayout(v_layout1)

        self.setWindowTitle("SONUC!")

    def ipleriYazdir(self):
        self.cgnatOlanTextWidget.setPlainText('\n'.join(cgnatIpAdresi))
        self.cgnatOlmayanTextWidget.setPlainText('\n'.join(cgnatIpAdresiDegil))


    def kaydet(self):
        try:
            name, _ = QFileDialog.getSaveFileName(self, 'Dosya Kaydet',"","Text Files (*.txt)")

            with open(name, 'w') as f:
                text = 'CGNAT\'DA OLMAYAN IP ADRESLERI:\n\n'
                text += self.cgnatOlmayanTextWidget.toPlainText()
                text += '\n\nCGNAT\'DA OLAN IP ADRESLERI:\n\n'
                text += self.cgnatOlanTextWidget.toPlainText()
                f.write(text)
        except Exception as e:
            pass

class anaPencereWidget(QWidget):
    def __init__(self, parent=None):
        super(anaPencereWidget, self).__init__(parent)
        global cgnatIpAdresi
        global cgnatIpAdresiDegil
        self.cgnSubnetFileData = []
        self.setAcceptDrops(True)
        self.sonucpencere = sonucPenceresi()
        self.init_ui()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        self.labelDosyaGir.setText('Girilen Dosya: ' + str(event.mimeData().text().strip('file:///')))

        if event.mimeData().text():
            with open(str(event.mimeData().text().strip('file:///')), 'r') as f:
                self.cgnSubnetFileData = [x.strip() for x in f.readlines()]

    def yeniPencereAc(self,pencere):
        if pencere.isVisible():
            pencere.hide()
            pencere.show()
            cgnatIpAdresi = []
            cgnatIpAdresiDegil = []
        else:
            pencere.show()

    def init_ui(self):

        v_layout = QVBoxLayout()

        self.labelDosyaGir = QLabel("Aranacak IP Adreslerini Giriniz!")
        v_layout.addWidget(self.labelDosyaGir)

        self.ipAdresleriWidget = QTextEdit()
        v_layout.addWidget(self.ipAdresleriWidget)

        self.labelDosyaGir = QLabel("Icinde Arama Yapmak Istediginiz CGNAT IP Dosyasini Seciniz!")
        v_layout.addWidget(self.labelDosyaGir)
        try:
            self.cwd = os.getcwd()#.replace('\\\\','\\')
            with open(str(self.cwd)+'\CGNAT_PUBLIC_IP_LIST.txt', 'r') as f:
                self.cgnSubnetFileData = [x.strip() for x in f.readlines()]
            self.labelDosyaGir.setText('Girilen Dosya: ' + str(self.cwd)+'CGNAT_PUBLIC_IP_LIST.txt')
        except Exception as e:
            pass

        self.buttonDosyaYukle = QPushButton("CGNAT IP Dosyasini Yukle")
        self.buttonDosyaYukle.clicked.connect(self.getfile)
        v_layout.addWidget(self.buttonDosyaYukle)

        self.btnAra = QPushButton("ARA")
        self.btnAra.clicked.connect(self.ipAra)
        v_layout.addWidget(self.btnAra)

        self.setLayout(v_layout)


    def getfile(self):
        try:
            self.filename = QFileDialog.getOpenFileName(self, 'Dosya Ac',
                                                self.cwd, "Text dosyalari (*.txt)")
            self.labelDosyaGir.setText('Girilen Dosya: '+ self.filename[0])

            if self.filename[0]:
                with open(self.filename[0], 'r') as f:
                    self.cgnSubnetFileData = [x.strip() for x in f.readlines()]
        except Exception as e:
            self.raiseAlert(e)

    def raiseAlert(self, errorMessage):
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Critical)
        self.msg.setText("Error")
        self.msg.setInformativeText(errorMessage)
        self.msg.setWindowTitle("Error")
        self.msg.exec_()

    def ipAra(self):
        try:
            self.kontrolEdilecekIpAdresleri = self.ipAdresleriWidget.toPlainText().split('\n')
            if len(self.kontrolEdilecekIpAdresleri[0]) >= 1:
                for ip in self.kontrolEdilecekIpAdresleri:
                    if len(ip) < 7:
                        continue
                    if (ip in cgnatIpAdresi) or (ip in cgnatIpAdresiDegil):
                        continue
                    for subnet in self.cgnSubnetFileData:
                        if (ip not in cgnatIpAdresi) and (ipaddress.ip_address(ip) in ipaddress.ip_network(subnet)):
                            cgnatIpAdresi.append(ip)
                    if (ip not in cgnatIpAdresiDegil) and (ip not in cgnatIpAdresi):
                        cgnatIpAdresiDegil.append(ip)

                self.sonucpencere.ipleriYazdir()
                self.yeniPencereAc(self.sonucpencere)
            else:
                self.raiseAlert('Kontrol edilecek ip adresi girmediniz!')
        except Exception as e:
            self.raiseAlert(str(e))

class anaPencere(QMainWindow):
    def __init__(self):
        super().__init__()
        self.pencere = anaPencereWidget()
        self.setCentralWidget(self.pencere)
        self.setWindowTitle("CGNAT IP KONTROL")
        self.resize(600, 500)
        self.show()

app = QApplication(sys.argv)
anapencereObj = anaPencere()

sys.exit(app.exec_())
