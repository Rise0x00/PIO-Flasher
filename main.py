from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtCore import QProcess, QTextCodec, QTimer
from UI import Ui_MainWindow
from datetime import datetime
from time import sleep
import sys

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.Button_flash.clicked.connect(self.flash_button_clicked)
        self.ui.Button_uploadfs.clicked.connect(self.uploadfs_button_clicked)
        self.ui.toolButton.clicked.connect(self.browse_folder)
        
        self.ui.progressBar.setValue(0)
        self.codec = QTextCodec.codecForName("cp866")

        # Настройка процесса
        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.process.finished.connect(self.process_finished)
        self.process.errorOccurred.connect(self.handle_error)

    def run_command(self, command):
        self.process.setWorkingDirectory(self.ui.lineEdit.text())
        self.process.start("cmd.exe", ["/c", "chcp 65001 > nul & " + command])

    def handle_stdout(self):
        """Чтение стандартного вывода"""
        data = self.process.readAllStandardOutput()
        codec = QTextCodec.codecForLocale()
        text = codec.toUnicode(data)
        self.append_output(text)

    def handle_stderr(self):
        """Чтение ошибок"""
        data = self.process.readAllStandardError()
        codec = QTextCodec.codecForLocale()
        text = codec.toUnicode(data)
        self.append_output(f"ERROR: {text}")

    def append_output(self, text):
        self.ui.conOut.append(text)

    def process_finished(self):
        """Действия после завершения команды"""
        self.append_output("\nProcess finished. Exit code: " + str(self.process.exitCode()))

    def handle_error(self, error):
        """Обработка ошибок выполнения"""
        self.append_output(f"ERROR: {error}")
        
    def write_output(self, text):
        self.ui.conOut.append(f"[{datetime.now().strftime('%H:%M:%S')}] {text}")

    def clear_output(self):
        self.ui.conOut.setText("")

    def clear_progress(self):
        for i in range(100):
            self.ui.progressBar.setValue(100-i)
            QApplication.processEvents() # UI Update
            sleep(0.01)

    def set_buttons_enable(self, state):
        self.ui.Button_flash.setEnabled(state)
        self.ui.Button_uploadfs.setEnabled(state)
        self.ui.toolButton.setEnabled(state)

    def flash_button_clicked(self):
        self.set_buttons_enable(False)
        self.clear_output()
        self.write_output("Начинаю прошивку...")
        # Получаем путь из поля ввода
        project_path = self.ui.lineEdit.text()
        if project_path:
            self.write_output(f"Путь к проекту: {project_path}")
            self.ui.progressBar.setValue(20)
            self.run_command('dir')
            self.process.waitForFinished()
            self.ui.progressBar.setValue(50)
            self.run_command('pio run -t upload')
            self.process.waitForFinished()
            self.ui.progressBar.setValue(100)
        else:
            self.write_output("Операция отменена. Путь к папке проекта не указан.")
        self.clear_progress()
        self.set_buttons_enable(True)

    def uploadfs_button_clicked(self):
        self.set_buttons_enable(False)
        self.clear_output()
        self.write_output("Загружаю файловую систему...")
        project_path = self.ui.lineEdit.text()
        if project_path:
            self.ui.progressBar.setValue(80)
            self.run_command('pio run -t uploadfs')
            self.process.waitForFinished()
            self.ui.progressBar.setValue(100)
        else:
            self.write_output("Операция отменена. Путь к папке проекта не указан.")
        self.clear_progress()
        self.set_buttons_enable(True)
    
    def browse_folder(self):
        """Обработчик кнопки выбора папки"""
        folder_path = QFileDialog.getExistingDirectory(self, "Выберите папку проекта")
        if folder_path:
            self.ui.lineEdit.setText(folder_path)
            self.clear_output()
            self.write_output(f"Выбрана папка проекта: {folder_path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())