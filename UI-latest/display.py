import sys
import time
import subprocess

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import paramiko

test_image = "cve-image"


class PresentationApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.cve_app = None
        self.dmesg_app = None
        self.performance_app = None

        self.dmesg_port = 10000

        self.setWindowTitle('vkernel系统演示')
        self.setFixedSize(400, 500)

        layout = QtWidgets.QVBoxLayout()

        button1 = QtWidgets.QToolButton(self)
        button1.clicked.connect(self.display2)
        button1.setIcon(QtGui.QIcon('vs.png'))
        button1.setIconSize(QtCore.QSize(128, 128))
        button1.setText("内核日志隔离")
        button1.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        layout.addWidget(button1, alignment=QtCore.Qt.AlignCenter)

        button0 = QtWidgets.QToolButton(self)
        button0.clicked.connect(self.display1)
        button0.setIcon(QtGui.QIcon('security.png'))
        button0.setIconSize(QtCore.QSize(128, 128))
        button0.setText('提权漏洞防护')
        button0.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        layout.addWidget(button0, alignment=QtCore.Qt.AlignCenter)

        button2 = QtWidgets.QToolButton(self)
        button2.clicked.connect(self.display3)
        button2.setIcon(QtGui.QIcon('performance.png'))
        button2.setIconSize(QtCore.QSize(128, 128))
        button2.setText("系统性能对比")
        button2.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        layout.addWidget(button2, alignment=QtCore.Qt.AlignCenter)

        self.setLayout(layout)

        self.center_window()

    def center_window(self):
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        window_size = self.geometry()
        x = (screen.width() - window_size.width()) // 6
        y = (screen.height() - window_size.height()) // 3
        self.move(x, y)

    def display1(self):
        self.cve_app = CveApp()
        self.cve_app.show()

    def display2(self):
        # self.dmesg_port += 2
        # self.dmesg_app = DmesgApp(self.dmesg_port)
        # self.dmesg_app.show()
        self.dmesg_app = DmesgApp1()
        self.dmesg_app.show()

    def display3(self):
        self.performance_app = PerformanceApp()
        self.performance_app.show()


class DmesgApp1(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.name1 = ""
        self.name2 = ""
        self.execdmesg1_app = []
        self.execdmesg2_app = []
        self.port = 10000
        self.client = None
        self.setWindowTitle('内核日志隔离')
        self.setFixedSize(400, 500)

        # Create the main layout with 1 row and 2 columns
        main_layout = QtWidgets.QHBoxLayout()

        # Create the layout for the first column
        column1_layout = QtWidgets.QVBoxLayout()

        self.create_container_button1 = QtWidgets.QToolButton(self)
        self.create_container_button1.clicked.connect(lambda _, flag=False: self.create_container(flag))
        self.create_container_button1.setIcon(QtGui.QIcon('normal.png'))
        self.create_container_button1.setIconSize(QtCore.QSize(128, 128))
        self.create_container_button1.setText("普通容器")
        self.create_container_button1.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        column1_layout.addWidget(self.create_container_button1, alignment=QtCore.Qt.AlignCenter)

        # Create the layout for the second column
        column2_layout = QtWidgets.QVBoxLayout()

        self.create_container_button2 = QtWidgets.QToolButton(self)
        self.create_container_button2.clicked.connect(lambda _, flag=True: self.create_container(flag))
        self.create_container_button2.setIcon(QtGui.QIcon('vkernel.png'))
        self.create_container_button2.setIconSize(QtCore.QSize(128, 128))
        self.create_container_button2.setText("vkernel容器")
        self.create_container_button2.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        column2_layout.addWidget(self.create_container_button2, alignment=QtCore.Qt.AlignCenter)

        # Add both column layouts to the main layout
        main_layout.addLayout(column1_layout)
        main_layout.addLayout(column2_layout)

        self.setLayout(main_layout)

        self.center_window()

    def center_window(self):
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        window_size = self.geometry()
        x = (screen.width() - window_size.width()) // 6
        y = (screen.height() - window_size.height()) // 3
        self.move(x, y)

    def create_container(self, flag):
        self.port += 1
        if flag:
            self.name2 = f"vkernel{self.port}"
            command = f"docker run --rm -d --name {self.name2} -p {self.port}:22 --privileged --runtime=vkernel-runtime {test_image}"
        else:
            self.name1 = f"normal{self.port}"
            command = f"docker run --rm -d --name {self.name1} -p {self.port}:22 --privileged {test_image}"

        process = QtCore.QProcess(self)
        process.setProcessChannelMode(QtCore.QProcess.MergedChannels)

        process.start(command)
        process.waitForFinished()

        # Check if there was an error during the command execution
        if process.exitStatus() != QtCore.QProcess.NormalExit:
            error_message = "Error occurred while executing the command."
            msg_box = QtWidgets.QMessageBox(self)
            msg_box.setWindowTitle('Command Error')
            msg_box.setText("Error:")
            msg_box.setInformativeText(error_message)
            msg_box.setIcon(QtWidgets.QMessageBox.Critical)
            msg_box.exec_()
            return

        output = process.readAll().data().decode()

        # Show the command output in a QMessageBox
        msg_box = QtWidgets.QMessageBox(self)
        msg_box.setWindowTitle('Command Output')
        msg_box.setText("Command Output:")
        msg_box.setInformativeText(output)
        msg_box.setIcon(QtWidgets.QMessageBox.Information)
        msg_box.exec_()

        if flag:
            self.execdmesg2_app.append(ExecDmesgApp(self.name2, self.port))
            self.execdmesg2_app[-1].show()
        else:
            self.execdmesg1_app.append(ExecDmesgApp(self.name1, self.port))
            self.execdmesg1_app[-1].show()


class ExecDmesgApp(QtWidgets.QWidget):
    def __init__(self, name, port):
        super().__init__()
        self.name = name
        self.port = port
        self.client = None
        self.setWindowTitle(f'{name} container')
        self.setFixedSize(800, 500)

        layout = QtWidgets.QVBoxLayout()

        self.dmesg = QtWidgets.QPushButton('Dmesg', self)
        self.dmesg.clicked.connect(self.execute_dmesg)
        self.dmesg.setFixedSize(780, 50)

        font = QFont()
        font.setPointSize(16)  # 设置字体大小为16
        self.dmesg.setFont(font)

        layout.addWidget(self.dmesg)

        self.textbox = QtWidgets.QPlainTextEdit(self)
        layout.addWidget(self.textbox)

        self.setLayout(layout)

        self.move_window()

    def move_window(self):
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        window_size = self.geometry()
        x = (screen.width() - window_size.width()) // 6 * 5
        y = (screen.height() - window_size.height()) // 3
        self.move(x, y)

    def connect_container(self):
        try:
            if self.client is not None:
                self.client.close()
                self.client = None
            self.client = paramiko.SSHClient()
            self.client.load_system_host_keys()
            self.client.set_missing_host_key_policy(paramiko.WarningPolicy())

            remote_host = '127.0.0.1'
            username = 'testuser'
            password = 'testuser'

            self.client.connect(hostname=remote_host, username=username, password=password, port=self.port)
        except paramiko.AuthenticationException:
            QtWidgets.QMessageBox.critical(self, '进入容器失败', '认证失败，请检查用户名和密码。')
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, '进入容器失败', f"无法进入容器: {e}")

    def execute_dmesg(self):
        self.connect_container()
        self.textbox.clear()
        stdin, stdout, stderr = self.client.exec_command('dmesg')
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()
        if output:
            print(f"Output from remote host: {output}")
            self.textbox.setPlainText(output)
        elif error:
            print(f"Error from remote host: {error}")
            self.textbox.setPlainText(error)
        self.client.close()

    def closeEvent(self, event):
        if self.name:
            process = QtCore.QProcess(self)
            process.setProcessChannelMode(QtCore.QProcess.MergedChannels)

            process.start(f'docker stop {self.name}')
            process.waitForFinished()


class DmesgApp(QtWidgets.QWidget):
    def __init__(self, base_port):
        super().__init__()
        self.name1 = ""
        self.name2 = ""
        self.port = base_port
        self.client = None
        self.setWindowTitle('Dmesg Presentation')
        self.setGeometry(800, 800, 1600, 1600)

        # Create the main layout with 1 row and 2 columns
        main_layout = QtWidgets.QHBoxLayout()

        # Create the layout for the first column
        column1_layout = QtWidgets.QVBoxLayout()

        self.create_container_button1 = QtWidgets.QPushButton('Create normal container', self)
        self.create_container_button1.clicked.connect(lambda _, flag=False: self.create_container(flag))
        column1_layout.addWidget(self.create_container_button1)

        self.execute_command_button1 = QtWidgets.QPushButton('Dmesg', self)
        self.execute_command_button1.clicked.connect(lambda _, flag=False: self.execute_command(flag))
        column1_layout.addWidget(self.execute_command_button1)

        self.command_output_textbox1 = QtWidgets.QPlainTextEdit(self)
        column1_layout.addWidget(self.command_output_textbox1)

        # Create the layout for the second column
        column2_layout = QtWidgets.QVBoxLayout()

        self.create_container_button2 = QtWidgets.QPushButton('Create vkernel container', self)
        self.create_container_button2.clicked.connect(lambda _, flag=True: self.create_container(flag))
        column2_layout.addWidget(self.create_container_button2)

        self.execute_command_button2 = QtWidgets.QPushButton('Dmesg', self)
        self.execute_command_button2.clicked.connect(lambda _, flag=True: self.execute_command(flag))
        column2_layout.addWidget(self.execute_command_button2)

        self.command_output_textbox2 = QtWidgets.QPlainTextEdit(self)
        column2_layout.addWidget(self.command_output_textbox2)

        # Add both column layouts to the main layout
        main_layout.addLayout(column1_layout)
        main_layout.addLayout(column2_layout)

        self.setLayout(main_layout)

    def connect_container(self, flag):
        try:
            if self.client is not None:
                self.client.close()
                self.client = None
            self.client = paramiko.SSHClient()
            self.client.load_system_host_keys()
            self.client.set_missing_host_key_policy(paramiko.WarningPolicy())

            remote_host = '127.0.0.1'
            username = 'testuser'
            password = 'testuser'

            if flag:
                p = self.port + 1
            else:
                p = self.port

            self.client.connect(hostname=remote_host, username=username, password=password, port=p)
        except paramiko.AuthenticationException:
            QtWidgets.QMessageBox.critical(self, '进入容器失败', '认证失败，请检查用户名和密码。')
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, '进入容器失败', f"无法进入容器: {e}")

    def create_container(self, flag):
        if flag:
            self.name2 = f"vkernel{self.port + 1}"
            command = f"docker run --rm -d --name {self.name2} -p {self.port + 1}:22 --privileged --runtime=vkernel-runtime {test_image}"
        else:
            self.name1 = f"normal{self.port}"
            command = f"docker run --rm -d --name {self.name1} -p {self.port}:22 --privileged {test_image}"

        process = QtCore.QProcess(self)
        process.setProcessChannelMode(QtCore.QProcess.MergedChannels)

        process.start(command)
        process.waitForFinished()

        # Check if there was an error during the command execution
        if process.exitStatus() != QtCore.QProcess.NormalExit:
            error_message = "Error occurred while executing the command."
            msg_box = QtWidgets.QMessageBox(self)
            msg_box.setWindowTitle('Command Error')
            msg_box.setText("Error:")
            msg_box.setInformativeText(error_message)
            msg_box.setIcon(QtWidgets.QMessageBox.Critical)
            msg_box.exec_()
            return

        output = process.readAll().data().decode()

        # Show the command output in a QMessageBox
        msg_box = QtWidgets.QMessageBox(self)
        msg_box.setWindowTitle('Command Output')
        msg_box.setText("Command Output:")
        msg_box.setInformativeText(output)
        msg_box.setIcon(QtWidgets.QMessageBox.Information)
        msg_box.exec_()

    def execute_command(self, flag):
        self.connect_container(flag)
        if flag:
            output_textbox = self.command_output_textbox2
        else:
            output_textbox = self.command_output_textbox1
        output_textbox.clear()
        stdin, stdout, stderr = self.client.exec_command('dmesg')
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()
        if output:
            print(f"Output from remote host: {output}")
            output_textbox.setPlainText(output)
        elif error:
            print(f"Error from remote host: {error}")
            output_textbox.setPlainText(error)
        self.client.close()

    def closeEvent(self, event):
        if self.name1:
            process = QtCore.QProcess(self)
            process.setProcessChannelMode(QtCore.QProcess.MergedChannels)

            process.start(f'docker stop {self.name1}')
            process.waitForFinished()
        if self.name2:
            process = QtCore.QProcess(self)
            process.setProcessChannelMode(QtCore.QProcess.MergedChannels)

            process.start(f'docker stop {self.name2}')
            process.waitForFinished()


class PerformanceApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.process = None
        self.url = 'http://127.0.0.1:8000'
        self.setWindowTitle('系统性能对比')
        self.setFixedSize(400, 500)

        layout = QtWidgets.QGridLayout()

        button0 = QtWidgets.QToolButton(self)
        button0.clicked.connect(self.show_web)
        button0.setIcon(QtGui.QIcon('web.png'))
        button0.setIconSize(QtCore.QSize(128, 128))
        button0.setText('web')
        button0.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        layout.addWidget(button0, 0, 0, 1, 2, alignment=QtCore.Qt.AlignCenter)

        button1 = QtWidgets.QToolButton(self)
        button1.clicked.connect(lambda _, s='nginx-annual.sh': self.execute_scripts(s))
        button1.setIcon(QtGui.QIcon('nginx.png'))
        button1.setIconSize(QtCore.QSize(128, 128))
        button1.setText("Nginx Test")
        button1.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        layout.addWidget(button1, 1, 0, 1, 1)

        button2 = QtWidgets.QToolButton(self)
        button2.clicked.connect(lambda _, s='pwgen-annual.sh': self.execute_scripts(s))
        button2.setIcon(QtGui.QIcon('pwgen.png'))
        button2.setIconSize(QtCore.QSize(128, 128))
        button2.setText("Pwgen Test")
        button2.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        layout.addWidget(button2, 1, 1, 1, 1)

        button3 = QtWidgets.QToolButton(self)
        button3.clicked.connect(lambda _, s='futex-hash-annual.sh': self.execute_scripts(s))
        button3.setIcon(QtGui.QIcon('hash.png'))
        button3.setIconSize(QtCore.QSize(128, 128))
        button3.setText("Futex Hash Test")
        button3.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        layout.addWidget(button3, 2, 0, 1, 1)

        button4 = QtWidgets.QToolButton(self)
        button4.clicked.connect(lambda _, s='futex-wake-parallel-annual.sh': self.execute_scripts(s))
        button4.setIcon(QtGui.QIcon('wake.png'))
        button4.setIconSize(QtCore.QSize(128, 128))
        button4.setText("Futex Wake Test")
        button4.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        layout.addWidget(button4, 2, 1, 1, 1)

        self.setLayout(layout)

        self.center_window()

    def center_window(self):
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        window_size = self.geometry()
        x = (screen.width() - window_size.width()) // 6
        y = (screen.height() - window_size.height()) // 3
        self.move(x, y)

    def show_web(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(self.url))

    def execute_scripts(self, s):
        path = "/home/liuyijie/Projects/vkernel/Annual/vkernel-display/web-server/scripts"
        # path = "/home/yuehang"
        if "futex" in s:
            path += "/futex"
        script_path = f"{path}/{s}"
        self.process = subprocess.Popen(['sh', script_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

        while True:
            output = self.process.stdout.readline()
            if output == '' and self.process.poll() is not None:
                break
            if output:
                print(output.strip())

        if self.process.poll() == 0:
            print("执行成功")
        else:
            print("执行失败")


class CveApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('提权漏洞防护')
        self.setFixedSize(400, 500)

        layout = QtWidgets.QVBoxLayout()

        button0 = QtWidgets.QToolButton(self)
        button0.clicked.connect(self.create_container)
        button0.setIcon(QtGui.QIcon('Create a container.png'))
        button0.setIconSize(QtCore.QSize(128, 128))
        button0.setText('启动SSH服务器')
        button0.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        layout.addWidget(button0, alignment=QtCore.Qt.AlignCenter)

        button1 = QtWidgets.QToolButton(self)
        button1.clicked.connect(self.entry_container)
        button1.setIcon(QtGui.QIcon('enter.png'))
        button1.setIconSize(QtCore.QSize(128, 128))
        button1.setText("用户登录")
        button1.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        layout.addWidget(button1, alignment=QtCore.Qt.AlignCenter)

        self.button2 = QtWidgets.QToolButton(self)
        self.button2.clicked.connect(self.button2_clicked)
        self.button2.setIconSize(QtCore.QSize(128, 128))
        # button1.setText("Build vkernel")
        self.button2.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        layout.addWidget(self.button2, alignment=QtCore.Qt.AlignCenter)

        self.button2_first_clicked = True

        self.setLayout(layout)

        self.name1 = ""
        self.name2 = ""

        self.flag = False
        self.update_button_icon()

        self.center_window()

    def center_window(self):
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        window_size = self.geometry()
        x = (screen.width() - window_size.width()) // 6
        y = (screen.height() - window_size.height()) // 3
        self.move(x, y)

    def create_container(self):
        if self.flag:
            self.name2 = "vkernel"
            command = f"docker run --rm -d --name {self.name2} -p 3333:22 --privileged --runtime=vkernel-runtime {test_image}"
            # command = f"docker run --rm -d --name {self.name2} -p 3333:22 --privileged {test_image}"
        else:
            self.name1 = "cve"
            command = f"docker run --rm -d --name {self.name1} -p 2222:22 --privileged {test_image}"

        process = QtCore.QProcess(self)
        process.setProcessChannelMode(QtCore.QProcess.MergedChannels)

        process.start(command)
        process.waitForFinished()

        # Check if there was an error during the command execution
        if process.exitStatus() != QtCore.QProcess.NormalExit:
            # error_message = "Error occurred while executing the command."
            # msg_box = QtWidgets.QMessageBox(self)
            # msg_box.setWindowTitle('Command Error')
            # msg_box.setText("Error:")
            # msg_box.setInformativeText(error_message)
            # msg_box.setIcon(QtWidgets.QMessageBox.Critical)
            # msg_box.exec_()
            QtWidgets.QMessageBox.critical(self, 'Failed', '容器已创建，请勿重复创建')
            return

        if not self.flag:
            output = process.readAll().data().decode()

            # Show the command output in a QMessageBox
            msg_box = QtWidgets.QMessageBox(self)
            msg_box.setWindowTitle('Command Output')
            msg_box.setText("Command Output:")
            msg_box.setInformativeText(output)
            msg_box.setIcon(QtWidgets.QMessageBox.Information)
            msg_box.exec_()

    def button2_clicked(self):
        if self.flag:
            self.flag = False
            # QtWidgets.QMessageBox.critical(self, 'Close', 'close')
        else:
            self.flag = True
            # QtWidgets.QMessageBox.critical(self, 'Open', 'open')
        self.update_button_icon()
        if self.button2_first_clicked:
            self.create_container()
            self.button2_first_clicked = False

    def update_button_icon(self):
        if self.flag:
            self.button2.setIcon(QtGui.QIcon('close.png'))
            self.button2.setText("防护已开启")
        else:
            self.button2.setIcon(QtGui.QIcon('open.png'))
            self.button2.setText("防护未开启")

    def entry_container(self):
        if self.flag:
            remote_command_app = ContainerCommandApp(self.name2, self.flag)
        else:
            remote_command_app = ContainerCommandApp(self.name1, self.flag)
        remote_command_app.show()

    def closeEvent(self, event):
        if self.name1:
            process = QtCore.QProcess(self)
            process.setProcessChannelMode(QtCore.QProcess.MergedChannels)

            process.start(f'docker stop {self.name1}')
            process.waitForFinished()
        if self.name2:
            process = QtCore.QProcess(self)
            process.setProcessChannelMode(QtCore.QProcess.MergedChannels)

            process.start(f'docker stop {self.name2}')
            process.waitForFinished()


class ContainerCommandApp(QtWidgets.QWidget):
    def __init__(self, name, flag):
        super().__init__()
        self.output_app = None
        self.root_clicked = False
        self.name = name
        self.flag = flag
        self.client = None
        self.channel = None
        self.connect_container()

        self.setWindowTitle(f"{self.name} container")
        self.setFixedSize(400, 550)

        # Create the main layout with 3 rows
        main_layout = QtWidgets.QVBoxLayout()

        # Create the grid layout for the buttons
        button_layout = QtWidgets.QGridLayout()
        main_layout.addLayout(button_layout)

        row, col = 0, 0
        button = QtWidgets.QToolButton(self)
        button.clicked.connect(lambda _, f=True: self.upgrade_to_root(f))
        button.setIcon(QtGui.QIcon('user_root.png'))
        button.setIconSize(QtCore.QSize(128, 128))
        button.setText('Root')
        button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        button_layout.addWidget(button, row, col)

        # Create 5 buttons and add them to the grid layout
        buttons = [
            {"text": "查看当前用户", "icon": "who.png", "command": "id"},
            {"text": "创建文件", "icon": "file.png", "command": "touch /tmp/test_dir/key.txt"},
            {"text": "查看进程信息", "icon": "ps.png", "command": "ps"},
            {"text": "查看目录内容", "icon": "list.png", "command": "ls -l"},
            {"text": "查看当前路径", "icon": "pwd.png", "command": "pwd"}
        ]

        col += 1
        for button_info in buttons:
            button = QtWidgets.QToolButton(self)
            button.clicked.connect(lambda _, cmd=button_info["command"]: self.execute_command(cmd))
            button.setIcon(QtGui.QIcon(button_info["icon"]))
            button.setIconSize(QtCore.QSize(128, 128))
            button.setText(button_info["text"])
            button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
            button_layout.addWidget(button, row, col)
            col += 1
            if col >= 2:
                col = 0
                row += 1

        # Create the text input and execute button for other commands
        input_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(input_layout)

        self.command_input = QtWidgets.QLineEdit(self)
        input_layout.addWidget(self.command_input)

        execute_button = QtWidgets.QPushButton('Execute', self)
        execute_button.clicked.connect(self.execute_other_command)
        input_layout.addWidget(execute_button)

        self.setLayout(main_layout)

        self.first = True

        self.move_window()

    def move_window(self):
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        window_size = self.geometry()
        x = (screen.width() - window_size.width()) // 6 * 3
        y = (screen.height() - window_size.height()) // 3
        self.move(x, y)

    def connect_container(self):
        try:
            self.client = paramiko.SSHClient()
            self.client.load_system_host_keys()
            self.client.set_missing_host_key_policy(paramiko.WarningPolicy())

            remote_host = '127.0.0.1'
            username = 'testuser'
            password = 'testuser'

            if self.flag:
                p = 3333
            else:
                p = 2222

            self.client.connect(hostname=remote_host, username=username, password=password, port=p)

            # 使用paramiko.Channel和paramiko.invoke_shell实现交互式shell会话
            self.channel = self.client.invoke_shell()
            time.sleep(0.1)
            output = ""
            while not self.channel.recv_ready():
                continue
            while self.channel.recv_ready():
                output += self.channel.recv(65535).decode()
            print(output)
        except paramiko.AuthenticationException:
            QtWidgets.QMessageBox.critical(self, '进入容器失败', '认证失败，请检查用户名和密码。')
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, '进入容器失败', f"无法进入容器: {e}")

    def upgrade_to_root(self, flag=True):
        while self.channel.recv_ready():
            self.channel.recv(65535).decode()

        self.channel.send("sudo -u#-1 /bin/bash\n")
        time.sleep(0.1)
        output = ""
        while not self.channel.recv_ready():
            continue
        while self.channel.recv_ready():
            output += self.channel.recv(65535).decode()
        print(output)
        if flag:
            self.root_clicked = True
            if 'Operation not permitted' in output:
                QtWidgets.QMessageBox.critical(self, 'Failed', '切换到root用户失败。')
                return
            else:
                QtWidgets.QMessageBox.information(self, 'Succeed', '成功切换到root用户。')

    def execute_command(self, command, text=False):
        print(command)
        if text or command != 'id':
            self.first = False
            command = f"/cdk.sh \"{command}\""

        try:
            while self.channel.recv_ready():
                self.channel.recv(65535).decode()
            self.channel.send(f"{command}\n")
            time.sleep(0.5)
            output = ""
            while not self.channel.recv_ready():
                continue
            while self.channel.recv_ready():
                output += self.channel.recv(65535).decode()
            print(output)
            if text is not True and command == "id":
                if "root" in output:
                    QtWidgets.QMessageBox.information(self, 'root', '当前用户: root')
                else:
                    QtWidgets.QMessageBox.information(self, 'testuser', '当前用户: testuser')
            else:
                time.sleep(0.5)
                output = ""
                while not self.channel.recv_ready():
                    continue
                while self.channel.recv_ready():
                    output += self.channel.recv(65535).decode()
                print(output)
                if "exit status 1" in output:
                    if self.output_app is None:
                        self.output_app = OutputApp()
                        self.output_app.show()
                    self.output_app.append_output("-" * 50)
                    self.output_app.append_output(" ")
                    self.output_app.append_output("exit status 1")
                    QtWidgets.QMessageBox.critical(self, 'Failed', '逃逸失败')
                else:
                    lines = output.strip().splitlines()
                    filtered_lines = lines[1:]
                    result = "\n".join(filtered_lines)
                    print(result)
                    if self.output_app is None:
                        self.output_app = OutputApp()
                        self.output_app.show()
                    self.output_app.append_output("-" * 50)
                    self.output_app.append_output(result)
                    QtWidgets.QMessageBox.information(self, 'Succeed', '逃逸成功')
                self.client.close()
                self.client = None
                self.channel = None
                process = QtCore.QProcess(self)
                process.setProcessChannelMode(QtCore.QProcess.MergedChannels)

                process.start(f'docker restart {self.name}')
                process.waitForFinished()
                time.sleep(0.1)
                self.connect_container()
                if self.root_clicked:
                    self.upgrade_to_root(False)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, '错误', f"执行命令出错: {e}")

    def execute_other_command(self):
        command = self.command_input.text()
        self.execute_command(command, True)

    def closeEvent(self, event):
        if self.client is not None:
            self.client.close()
            self.client = None


class OutputApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Output')
        self.setFixedSize(600, 500)

        layout = QtWidgets.QVBoxLayout()

        self.command_output_textbox = QtWidgets.QPlainTextEdit(self)
        self.command_output_textbox.setReadOnly(True)
        layout.addWidget(self.command_output_textbox)

        self.setLayout(layout)

        self.move_window()

    def move_window(self):
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        window_size = self.geometry()
        x = (screen.width() - window_size.width()) // 20 * 19
        y = (screen.height() - window_size.height()) // 3
        self.move(x, y)

    def append_output(self, output):
        self.command_output_textbox.appendPlainText(output)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    presentation_app = PresentationApp()
    presentation_app.show()
    sys.exit(app.exec_())
