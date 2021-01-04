from setup.setup import Setup as S
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Setup(object):
    def __init__(self):
        self.label = QtWidgets.QLabel(Setup)
        self.label_2 = QtWidgets.QLabel(Setup)
        self.label_3 = QtWidgets.QLabel(Setup)
        self.pushButton = QtWidgets.QPushButton(Setup)

        self.api_key_input = QtWidgets.QLineEdit(Setup)
        self.internal_username_input = QtWidgets.QLineEdit(Setup)
        self.fdesk_agent_name_input = QtWidgets.QLineEdit(Setup)
        self.setup_actions = S()

    def setupUi(self, Setup):
        Setup.setObjectName("Setup")
        Setup.setFixedSize(430, 170)

    def ui_labels(self):
        self.label.setGeometry(QtCore.QRect(30, 21, 121, 16))
        self.label.setObjectName("label")

        self.label_2.setGeometry(QtCore.QRect(30, 62, 121, 16))
        self.label_2.setObjectName("label_2")

        self.label_3.setGeometry(QtCore.QRect(30, 102, 121, 16))
        self.label_3.setObjectName("label_3")

    def confirm(self):
        internal_username_input = self.internal_username_input.text()
        api_key_input = self.api_key_input.text()
        fdesk_agent_name_input = self.fdesk_agent_name_input.text()

        if internal_username_input and api_key_input and fdesk_agent_name_input != '':

            if not self.setup_actions.setup_freshdesk(fdesk_agent_name_input, api_key_input):
                self.invalid_api()
                return False
            else:
                pass

            internal = self.setup_actions.setup_internal(internal_username_input)
            if not internal:
                self.invalid_internal_username()
                return False

            self.done_message()


        else:
            self.finish_form_message()
            return False


    def done_message(self):
        msg = QMessageBox()
        msg.setWindowTitle("Success")
        msg.setText("Installation Completed. \nYou can run the Auto Ticket Opener now.")
        msg.setIcon(QMessageBox.Information)
        x = msg.exec_()

    def t(self):
        self.fdesk_agent_name_input.setGeometry(QtCore.QRect(160, 20, 251, 21))
        self.fdesk_agent_name_input.setObjectName("fdesk_agent_name_input")

        self.internal_username_input.setGeometry(QtCore.QRect(160, 60, 251, 21))
        self.internal_username_input.setObjectName("internal_username_input")

        self.api_key_input.setGeometry(QtCore.QRect(160, 100, 251, 21))
        self.api_key_input.setObjectName("api_key_input")

        self.pushButton.setGeometry(QtCore.QRect(306, 130, 113, 32))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Setup)
        self.pushButton.clicked.connect(self.confirm)

        QtCore.QMetaObject.connectSlotsByName(Setup)

    def finish_form_message(self):
        msg = QMessageBox()
        msg.setWindowTitle("Fill all fields")
        msg.setText("Please make sure all fields are filled")
        msg.setIcon(QMessageBox.Warning)
        x = msg.exec_()

    def invalid_api(self):
        msg = QMessageBox()
        msg.setWindowTitle("Invalid API")
        msg.setText("Please check your API key")
        msg.setIcon(QMessageBox.Warning)
        x = msg.exec_()

    def invalid_fd_username(self):
        msg = QMessageBox()
        msg.setWindowTitle("Invalid Fresh Desk username")
        msg.setText("Please check Fresh Desk user name.")
        msg.setIcon(QMessageBox.Warning)
        x = msg.exec_()

    def invalid_internal_username(self):
        msg = QMessageBox()
        msg.setWindowTitle("Invalid Internal username")
        msg.setText("Please check Internal user name.")
        msg.setIcon(QMessageBox.Warning)
        x = msg.exec_()

    def retranslateUi(self, Setup):
        _translate = QtCore.QCoreApplication.translate
        Setup.setWindowTitle(_translate("Setup", "Setup"))
        self.label_2.setText(_translate("Setup", "Internal username"))
        self.label.setText(_translate("Setup", "Fdesk agent name"))
        self.label_3.setText(_translate("Setup", "API Key"))
        self.pushButton.setText(_translate("Setup", "Confirm"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('icons/setup.ico'))
    Setup = QtWidgets.QDialog()
    ui = Ui_Setup()
    ui.setupUi(Setup)
    ui.ui_labels()
    ui.ui_inputs()
    Setup.show()
    sys.exit(app.exec_())


