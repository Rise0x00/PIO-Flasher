from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from UI import Ui_MainWindow
from datetime import datetime
import sys

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.Button_flash.clicked.connect(self.flash_button_clicked)
        self.ui.Button_uploadfs.clicked.connect(self.uploadfs_button_clicked)
        self.ui.toolButton.clicked.connect(self.browse_folder)
        
        # Инициализируем прогресс-бар
        self.ui.progressBar.setValue(0)
        
    def write_output(self, text):
        self.ui.conOut.append(f"[{datetime.now().strftime('%H:%M:%S')}] {text}")

    def clear_output(self):
        self.ui.conOut.setText("")

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
        else:
            self.write_output("Операция отменена. Путь к папке проекта не указан.")
        self.set_buttons_enable(True)

    def uploadfs_button_clicked(self):
        self.set_buttons_enable(False)
        self.clear_output()
        self.write_output("Загружаю файловую систему...")
        self.ui.progressBar.setValue(0)
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