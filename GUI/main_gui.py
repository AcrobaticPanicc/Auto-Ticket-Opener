import requests
from PyQt5.QtCore import Qt

from freshdesk.open_ticket import OpenTicket
from internal.internal import Internal
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from info.info import get_info
import sys
from counter.counter import get_total_count, get_agent_count


class Ui_AutoTicketOpener(object):
    def __init__(self):
        self.widget = QtWidgets.QWidget(AutoTicketOpener)
        self.widget1 = QtWidgets.QWidget(AutoTicketOpener)
        self.gridLayout = QtWidgets.QGridLayout(self.widget1)
        self.operating_system_input = QtWidgets.QLineEdit(self.widget)
        self.os_label = QtWidgets.QLabel(self.widget)
        self.host_app_input = QtWidgets.QLineEdit(self.widget)
        self.host_label = QtWidgets.QLabel(self.widget)
        self.ticket_title_input = QtWidgets.QLineEdit(self.widget)
        self.ticket_title_label = QtWidgets.QLabel(self.widget)
        self.username_input = QtWidgets.QLineEdit(self.widget)
        self.username_label = QtWidgets.QLabel(self.widget)
        self.top_input_container = QtWidgets.QGridLayout(self.widget)
        self.main_title_label = QtWidgets.QLabel(AutoTicketOpener)
        self.submit_button = QtWidgets.QPushButton(AutoTicketOpener)
        self.priority_label = QtWidgets.QLabel(self.widget1)
        self.radio_container = QtWidgets.QVBoxLayout()
        self.medium_button = QtWidgets.QRadioButton(self.widget1)
        self.high_button = QtWidgets.QRadioButton(self.widget1)
        self.urgent_button = QtWidgets.QRadioButton(self.widget1)
        self.widget2 = QtWidgets.QWidget(AutoTicketOpener)
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget2)
        self.description_label = QtWidgets.QLabel(self.widget2)
        self.description_input = QtWidgets.QPlainTextEdit(self.widget2)

        self.internal = Internal()

        if not self.internal.check_vpn_connection():
            self.check_connection_message()

        self.info = get_info()
        self.fd_action = OpenTicket(self.info)

        self.user_info = None
        self.priority = 'medium'
        self.total_tickets_message()

    def open_ticket(self):
        username = self.username_input.text()
        ticket_title = self.ticket_title_input.text()
        operating_system = self.operating_system_input.text()
        host_input = self.host_app_input.text()
        description_input = self.description_input.toPlainText()
        description_input = description_input.replace('\n', '<br/>')

        priority = self.get_radio_priority()
        if priority == 2:
            tag = ''
        else:
            tag = 'Soundgrid'

        if username and ticket_title and description_input != '':
            user = self.internal.search_user(username)

            if not user:
                self.user_not_found_message()
                self.username_input.clear()
                return False

            user_email = user['user_email']
            user_id = user['user_id']
            user_login = user['user_login']

            open_ticket = self.fd_action.open_ticket(ticket_title, operating_system, description_input, user_email,
                                                     user_id, user_login, tag, priority, host_input)
            if not open_ticket:
                self.ticket_was_not_created()
                return False

            self.clean_all_fields()
            self.done_message()
            # add 1 to the counter
            requests.get('https://api.countapi.xyz/hit/ato/key')
            requests.get(f'https://api.countapi.xyz/hit/{self.info["full_name"]}/key')
            return True
        else:
            self.complete_form_message()

    def actions(self):
        self.submit_button.clicked.connect(self.open_ticket)

    def clean_all_fields(self):
        self.description_input.clear()
        self.username_input.clear()
        self.operating_system_input.clear()
        self.ticket_title_input.clear()
        self.host_app_input.clear()
        self.medium_button.click()

    def get_radio_priority(self):
        if self.medium_button.isChecked():
            return 2
        elif self.high_button.isChecked():
            return 3
        elif self.urgent_button.isChecked():
            return 4

    def done_message(self):
        msg = QMessageBox()
        msg.setWindowTitle("Ticket created successfully!")
        msg.setText(f"Ticket created successfully. \nURL copied to clipboard")
        msg.setIcon(QMessageBox.Information)
        x = msg.exec_()

    def check_connection_message(self):
        msg = QMessageBox()
        msg.setWindowTitle("Not connected")
        msg.setText(f"Check your internet and VPN connection")
        msg.setIcon(QMessageBox.Warning)
        x = msg.exec_()

    def agent_id_not_found_message(self):
        msg = QMessageBox()
        msg.setWindowTitle("Agent ID not found")
        msg.setText("Agent ID file was not found. \nPlease run setup again.")
        msg.setIcon(QMessageBox.Information)
        x = msg.exec_()

    def internal_failed_message(self):
        msg = QMessageBox()
        msg.setWindowTitle("Failed to log in to Internal")
        msg.setText("Failed to log in to Internal. \nPlease run setup again or check VPN connection.")
        msg.setIcon(QMessageBox.Information)
        x = msg.exec_()

    def total_tickets_message(self):
        msg = QMessageBox()
        total_tickets = get_total_count()
        agent_total_tickets = get_agent_count(self.info['agent_name'])
        msg.setWindowTitle("Welcome back")
        msg.setText(
            f"Hi {self.info['full_name']}. \n\nSo far, you opened {agent_total_tickets} tickets \nTotal number of tickets opened: {total_tickets}")
        msg.setIcon(QMessageBox.Information)
        x = msg.exec_()

    def complete_form_message(self):
        msg = QMessageBox()
        msg.setWindowTitle("Fill all fields")
        msg.setText("Please make sure all required fields are filled")
        msg.setIcon(QMessageBox.Warning)
        x = msg.exec_()

    def user_not_found_message(self):
        msg = QMessageBox()
        msg.setWindowTitle("Username was not found")
        msg.setText("Username was not found. \nPlease check the username and try again")
        msg.setIcon(QMessageBox.Warning)
        x = msg.exec_()

    def ticket_was_not_created(self):
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText("Ticket was not created")
        msg.setIcon(QMessageBox.Warning)
        x = msg.exec_()

    def setupUi(self, AutoTicketOpener):
        AutoTicketOpener.setObjectName("AutoTicketOpener")
        AutoTicketOpener.setFixedSize(421, 567)
        self.submit_button.setGeometry(QtCore.QRect(281, 530, 131, 31))
        self.submit_button.setObjectName("submit_button")
        self.main_title_label.setGeometry(QtCore.QRect(10, 10, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.main_title_label.setFont(font)
        self.main_title_label.setObjectName("main_title_label")
        self.widget.setGeometry(QtCore.QRect(10, 50, 401, 141))
        self.widget.setObjectName("widget")
        self.top_input_container.setContentsMargins(0, 0, 0, 0)
        self.top_input_container.setObjectName("top_input_container")
        font = QtGui.QFont()
        font.setPointSize(10)
        self.username_label.setFont(font)
        self.username_label.setObjectName("username_label")
        self.top_input_container.addWidget(self.username_label, 0, 0, 1, 1)
        self.username_input.setText("")
        self.username_input.setObjectName("username_input")
        self.top_input_container.addWidget(self.username_input, 0, 1, 1, 1)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ticket_title_label.setFont(font)
        self.ticket_title_label.setObjectName("ticket_title_label")
        self.top_input_container.addWidget(self.ticket_title_label, 1, 0, 1, 1)
        self.ticket_title_input.setObjectName("ticket_title_input")
        self.top_input_container.addWidget(self.ticket_title_input, 1, 1, 1, 1)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.host_label.setFont(font)
        self.host_label.setObjectName("host_label")
        self.top_input_container.addWidget(self.host_label, 2, 0, 1, 1)
        self.host_app_input.setObjectName("host_app_input")
        self.top_input_container.addWidget(self.host_app_input, 2, 1, 1, 1)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.os_label.setFont(font)
        self.os_label.setObjectName("os_label")
        self.top_input_container.addWidget(self.os_label, 3, 0, 1, 1)
        self.operating_system_input.setEnabled(True)
        self.operating_system_input.setObjectName("operating_system_input")
        self.top_input_container.addWidget(self.operating_system_input, 3, 1, 1, 1)
        self.widget1.setGeometry(QtCore.QRect(9, 200, 63, 89))
        self.widget1.setObjectName("widget1")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        font = QtGui.QFont()
        font.setPointSize(10)
        self.priority_label.setFont(font)
        self.priority_label.setObjectName("priority_label")
        self.gridLayout.addWidget(self.priority_label, 0, 0, 1, 1)
        self.radio_container.setObjectName("radio_container")
        self.medium_button.setObjectName("medium_button")
        self.radio_container.addWidget(self.medium_button)
        self.medium_button.setChecked(True)
        self.high_button.setObjectName("high_button")
        self.radio_container.addWidget(self.high_button)
        self.urgent_button.setObjectName("urgent_button")
        self.radio_container.addWidget(self.urgent_button)
        self.gridLayout.addLayout(self.radio_container, 1, 0, 1, 1)
        self.widget2.setGeometry(QtCore.QRect(10, 310, 401, 216))
        self.widget2.setObjectName("widget2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        font = QtGui.QFont()
        font.setPointSize(10)
        self.description_label.setFont(font)
        self.description_label.setObjectName("description_label")
        self.gridLayout_2.addWidget(self.description_label, 0, 0, 1, 1)
        self.description_input.setObjectName("description_input")
        self.gridLayout_2.addWidget(self.description_input, 1, 0, 1, 1)
        self.medium_button.setObjectName("medium_radio")
        self.medium_button.setStyleSheet('color: green')
        self.high_button.setObjectName("high_radio")
        self.high_button.setStyleSheet('color: orange')
        self.urgent_button.setObjectName("urgent_radio")
        self.urgent_button.setStyleSheet('color: red')

        self.retranslateUi(AutoTicketOpener)
        QtCore.QMetaObject.connectSlotsByName(AutoTicketOpener)
        AutoTicketOpener.setTabOrder(self.username_input, self.ticket_title_input)
        AutoTicketOpener.setTabOrder(self.ticket_title_input, self.host_app_input)
        AutoTicketOpener.setTabOrder(self.host_app_input, self.operating_system_input)
        AutoTicketOpener.setTabOrder(self.operating_system_input, self.medium_button)
        AutoTicketOpener.setTabOrder(self.medium_button, self.high_button)
        AutoTicketOpener.setTabOrder(self.high_button, self.urgent_button)
        AutoTicketOpener.setTabOrder(self.urgent_button, self.description_input)
        AutoTicketOpener.setTabOrder(self.description_input, self.submit_button)

    def retranslateUi(self, AutoTicketOpener):
        _translate = QtCore.QCoreApplication.translate
        AutoTicketOpener.setWindowTitle(_translate("AutoTicketOpener", "Auto Ticket Opener"))
        self.submit_button.setText(_translate("AutoTicketOpener", "Submit"))
        self.main_title_label.setText(_translate("AutoTicketOpener", "Auto Ticket Opener "))
        self.username_label.setText(_translate("AutoTicketOpener", "Username*"))
        self.username_input.setPlaceholderText(_translate("AutoTicketOpener", "Tomer"))
        self.ticket_title_label.setText(_translate("AutoTicketOpener", "Ticket Title*"))
        self.ticket_title_input.setPlaceholderText(_translate("AutoTicketOpener", "Plugins not showing up in Logic"))
        self.host_label.setText(_translate("AutoTicketOpener", "Host Application"))
        self.host_app_input.setPlaceholderText(_translate("AutoTicketOpener", "Logic Pro X / Pro Tools 12"))
        self.os_label.setText(_translate("AutoTicketOpener", "Operating System"))
        self.operating_system_input.setPlaceholderText(_translate("AutoTicketOpener", "macOS Mojave / Windows 10"))
        self.priority_label.setText(_translate("AutoTicketOpener", "Priority"))
        self.medium_button.setText(_translate("AutoTicketOpener", "Medium"))
        self.high_button.setText(_translate("AutoTicketOpener", "High"))
        self.urgent_button.setText(_translate("AutoTicketOpener", "Urgent"))
        self.description_label.setText(_translate("AutoTicketOpener", "Description*"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AutoTicketOpener = QtWidgets.QDialog()
    ui = Ui_AutoTicketOpener()
    ui.setupUi(AutoTicketOpener)
    ui.actions()
    AutoTicketOpener.show()
    sys.exit(app.exec_())
