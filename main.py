from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtCore import QProcess, QTextCodec
from UI import Ui_MainWindow
from datetime import datetime
import warnings
import ctypes
import sys

DWMWA_USE_IMMERSIVE_DARK_MODE = 20
DWMWA_USE_IMMERSIVE_DARK_MODE_BEFORE_20H1 = 19

warnings.filterwarnings("ignore", category=DeprecationWarning, message="sipPyTypeDict.*")

class Features():
    def __init__(self) -> None:
        pass

    def enable_dark_title_bar(self, hwnd):
        try:
            self.value = ctypes.c_int(1)
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd, 
                DWMWA_USE_IMMERSIVE_DARK_MODE,
                ctypes.byref(self.value),
                ctypes.sizeof(self.value))
            
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd,
                DWMWA_USE_IMMERSIVE_DARK_MODE_BEFORE_20H1,
                ctypes.byref(self.value),
                ctypes.sizeof(self.value))
        except Exception as e: pass

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.Button_flash.clicked.connect(self.flash_button_clicked)
        self.ui.Button_uploadfs.clicked.connect(self.uploadfs_button_clicked)
        self.ui.Button_erase_flash.clicked.connect(self.erase_flash_button_clicked)
        self.ui.toolButton.clicked.connect(self.browse_folder)
        
        self.ui.progressBar.setRange(0, 100)
        self.ui.progressBar.setValue(0)
        self.codec = QTextCodec.codecForName("cp866")

        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.process.finished.connect(self.process_finished)
        self.process.errorOccurred.connect(self.handle_error)

    def showEvent(self, event):
        super().showEvent(event)
        if sys.platform == "win32":
            hwnd = self.winId()
            Features.enable_dark_title_bar(self, int(hwnd))

    # Service functions
    def run_command(self, command):
        self.process.setWorkingDirectory(self.ui.lineEdit.text())
        self.process.start("cmd.exe", ["/c", "chcp 65001 > nul & " + command])

    def handle_stdout(self):
        data = self.process.readAllStandardOutput()
        codec = QTextCodec.codecForLocale()
        text = codec.toUnicode(data)
        self.append_output(text)

    def handle_stderr(self):
        data = self.process.readAllStandardError()
        codec = QTextCodec.codecForLocale()
        text = codec.toUnicode(data)
        self.append_output(f"ERROR: {text}")

    def append_output(self, text):
        self.ui.conOut.append(text)

    def process_finished(self):
        self.append_output("\nProcess finished. Exit code: " + str(self.process.exitCode()))
        self.stop_progress()
        self.set_buttons_enable(True)

    def handle_error(self, error):
        self.append_output(f"ERROR: {error}")
        
    def write_output(self, text):
        self.ui.conOut.append(f"[{datetime.now().strftime('%H:%M:%S')}] {text}")

    def clear_output(self):
        self.ui.conOut.setText("")

    def start_progress(self):
        self.ui.progressBar.setRange(0, 0)

    def stop_progress(self):
        self.ui.progressBar.setRange(0, 100)
        self.ui.progressBar.setValue(0)

    def set_buttons_enable(self, state):
        self.ui.Button_flash.setEnabled(state)
        self.ui.Button_uploadfs.setEnabled(state)
        self.ui.toolButton.setEnabled(state)
        self.ui.Button_erase_flash.setEnabled(state)
        self.ui.lineEdit.setEnabled(state)
    ###
    # Button processing
    def flash_button_clicked(self):
        self.set_buttons_enable(False)
        self.clear_output()
        self.start_progress()
        self.write_output("Начинаю прошивку...")
        project_path = self.ui.lineEdit.text()
        self.ui.lineEdit.clearFocus()
        if project_path:
            self.write_output(f"Путь к проекту: {project_path}")
            self.run_command('dir')
            self.process.waitForFinished()
            self.set_buttons_enable(False)
            self.start_progress()
            self.run_command('pio run -t upload')
        else:
            self.write_output("Операция отменена. Путь к папке проекта не указан.")
            self.stop_progress()
            self.set_buttons_enable(True)

    def uploadfs_button_clicked(self):
        self.set_buttons_enable(False)
        self.start_progress()
        self.clear_output()
        self.write_output("Загружаю файловую систему...")
        project_path = self.ui.lineEdit.text()
        self.ui.lineEdit.clearFocus()
        if project_path:
            self.run_command('pio run -t uploadfs')
        else:
            self.write_output("Операция отменена. Путь к папке проекта не указан.")
            self.stop_progress()
            self.set_buttons_enable(True)

    def erase_flash_button_clicked(self):
        self.set_buttons_enable(False)
        self.start_progress()
        self.clear_output()
        self.write_output("Очищаю flash память платы...")
        project_path = self.ui.lineEdit.text()
        self.ui.lineEdit.clearFocus()
        if project_path:
            self.run_command('pio run -t erase')
        else:
            self.write_output("Операция отменена. Путь к папке проекта не указан.")
            self.stop_progress()
            self.set_buttons_enable(True)
    
    def browse_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Выберите папку проекта")
        if folder_path:
            self.ui.lineEdit.setText(folder_path)
            self.ui.lineEdit.clearFocus()
            self.clear_output()
            self.write_output(f"Выбрана папка проекта: {folder_path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())