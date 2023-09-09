import sys
from custome_errors import *
sys.excepthook = my_excepthook
import cv2
import qrcode
import guiTools
from webbrowser import open as openLink
import language
import app
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
from PyQt6.QtCore import Qt
language.init_translation()
class main (qt.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(app.name + _("version : ") + str(app.version))
        layout=qt.QVBoxLayout()
        self.tab=guiTools.listBook(layout,_("select servis"))
        l1=qt.QVBoxLayout()
        self.text=qt.QLineEdit()
        self.text.setAccessibleName(_("text"))
        l1.addWidget(self.text)
        self.link=qt.QCheckBox(_("link"))
        l1.addWidget(self.link)
        self.genrate=qt.QPushButton(_("genrate"))
        self.genrate.setDefault(True)
        self.genrate.clicked.connect(self.dgenrate)
        l1.addWidget(self.genrate)
        self.tab.add(_("create qr code"),l1)
        l2=qt.QVBoxLayout()
        self.file=qt.QLineEdit()
        self.file.setAccessibleName(_("img path"))
        self.file.setReadOnly(True)
        l2.addWidget(self.file)
        self.brows=qt.QPushButton(_("brows"))
        self.brows.setDefault(True)
        self.brows.clicked.connect(self.fbrows)
        l2.addWidget(self.brows)
        self.get=qt.QPushButton(_("get result"))
        self.get.setDefault(True)
        self.get.clicked.connect(lambda:self.getre(self.file.text()))
        l2.addWidget(self.get)
        self.re=qt.QLineEdit()
        self.re.setReadOnly(True)
        self.re.setAccessibleName(_("result"))
        l2.addWidget(self.re)
        self.tab.add(_("extract qrcode"),l2)
        w=qt.QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)
        mb=self.menuBar()
        help=mb.addMenu(_("help"))
        cus=help.addMenu(_("contact us"))
        telegram=qt1.QAction("telegram",self)
        cus.addAction(telegram)
        telegram.triggered.connect(lambda:openLink("https://t.me/mesteranasm"))
        telegramc=qt1.QAction(_("telegram channel"),self)
        cus.addAction(telegramc)
        telegramc.triggered.connect(lambda:openLink("https://t.me/tprogrammers"))
        donate=qt1.QAction(_("donate"),self)
        help.addAction(donate)
        donate.triggered.connect(lambda:openLink("https://www.paypal.me/AMohammed231"))
        about=qt1.QAction(_("about"),self)
        help.addAction(about)
        about.triggered.connect(lambda:qt.QMessageBox.information(self,_("about"),_("{} version: {} description: {} developer: {}").format(app.name,str(app.version),app.description,app.creater)))
        self.setMenuBar(mb)
    def dgenrate(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        if self.link.isChecked():
            qr.add_data(self.text.text(), optimize=0)
        else:
            qr.add_data(self.text.text())
        qr.make(fit=True)
        file=qt.QFileDialog(self)
        file.setDefaultSuffix("png")
        file.setAcceptMode(qt.QFileDialog.AcceptMode.AcceptSave)
        file.setNameFilters(["img files(*.png)"])
        if file.exec() == qt.QFileDialog.DialogCode.Accepted:
            qr.make_image(fill_color="black", back_color="white").save(file.selectedFiles()[0])
            qt.QMessageBox.information(self,_("done"),_("file saved"))
    def fbrows(self):
        file=qt.QFileDialog(self)
        file.setDefaultSuffix("png")
        file.setAcceptMode(qt.QFileDialog.AcceptMode.AcceptOpen)
        file.setNameFilters(["img files(*.png)"])
        if file.exec() == qt.QFileDialog.DialogCode.Accepted:
            self.file.setText(file.selectedFiles()[0])
    def getre(self,path):
        img = cv2.imread(path)
        qr_code_detector = cv2.QRCodeDetector()
        try:
            decoded_objects = qr_code_detector.detectAndDecodeMulti(img)
            self.re.setText(decoded_objects[1][0])
            self.re.setFocus()
        except:
            qt.QMessageBox.information(self,_("error"),_("no qr code fownd"))

App=qt.QApplication([])
w=main()
w.show()
App.exec()