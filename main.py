from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMenu, QAction, QFileDialog, QLineEdit, QSlider, \
    QLabel, QMessageBox, QTextEdit
from PyQt5.QtCore import Qt
import sys, compress


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Создаем кнопку
        self.select_button = QPushButton("Выбрать", self)
        self.select_button.setGeometry(50, 30, 100, 30)

        # Создаем поле для отображения выбранного пути
        self.source_line_edit = QLineEdit(self)
        self.source_line_edit.setGeometry(170, 30, 400, 30)

        # Привязываем обработчик события нажатия на кнопку
        self.select_button.clicked.connect(self.show_menu)

        # Создание ползунка
        slider = QSlider(self)
        slider.setOrientation(Qt.Horizontal)  # Установка горизонтальной ориентации
        slider.setGeometry(85, 120, 330, 30)  # Установка размеров и позиции
        slider.setTickPosition(QSlider.TicksBelow)  # Установка позиции меток
        slider.setTickPosition(QSlider.TicksAbove)
        # Установка минимального, максимального и начального значения
        slider.setMinimum(10)
        slider.setMaximum(90)
        slider.setValue(10)
        slider.setTickInterval(5)
        slider.setSingleStep(5)

        # Создание метки для отображения значений
        label = QLabel(self)
        label.setGeometry(365, 120, 180, 30)
        label.setAlignment(Qt.AlignCenter)
        label.setText('10')
        # Обработка изменения значения ползунка
        slider.valueChanged.connect(lambda value: self.on_slider_value_changed(value, label))

        # Добавление значений над слайдером
        ticks = QLabel(self)
        ticks.setGeometry(85, 95, 330, 30)
        ticks.setAlignment(Qt.AlignCenter)
        ticks.setText("10    .    20    .    30    .    40    .    50    .    60    .    70    .    80    .    90")

        # Инициализация переменной для хранения значения ползунка
        self.slider_value = slider.value()

        # Создание кнопки с иконкой вопросительного знака
        btn = QPushButton('?', self)
        btn.setGeometry(50, 110, 30, 30)
        btn.clicked.connect(self.show_info)

        self.select_target_bunnon = QPushButton("Сохранить в:", self)
        self.select_target_bunnon.setGeometry(50, 200, 100, 30)
        self.select_target_bunnon.clicked.connect(self.select_folder_target)

        self.target_line_edit = QLineEdit(self)
        self.target_line_edit.setGeometry(170, 200, 400, 30)

        self.agregate_button = QPushButton("Сжать", self)
        self.agregate_button.setGeometry(50, 270, 100, 30)
        self.agregate_button.clicked.connect(self.compressing)


        # создаем экземпляр QTextEdit и добавляем его на основную форму
        self.textEdit = QTextEdit(self)
        # настройки QTextEdit
        self.textEdit.setReadOnly(True)  # запрет редактирования текста
        self.textEdit.setFrameStyle(1)  # рамка
        self.textEdit.setGeometry(50, 310, 400, 260)



    def compressing(self):
        self.textEdit.clear()
        for filename in compress.compress_images(self.source_line_edit.text(), self.target_line_edit.text(),
                                           self.slider_value):
            self.textEdit.insertPlainText("✓ " + filename + "\n")


    def show_info(self):
        # Создание всплывающего окна с информацией
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Ползунок отображает качество итогового изображения.\n"
                    "10 - низкое качество (максимальное сжатие изображений)\n"
                    "90 - высокое качество (минимальное сжатие изображений)")
        msg.setWindowTitle("Слайдер")
        msg.exec_()

    def on_slider_value_changed(self, value, label):
        # Обновление метки с текущим значением
        label.setText(str(value))
        # Сохранение значения в переменную
        self.slider_value = value

    def show_menu(self):
        # Создаем выпадающее меню
        menu = QMenu(self.select_button)
        file_action = QAction("Файл", self)
        folder_action = QAction("Папка", self)
        menu.addAction(file_action)
        menu.addAction(folder_action)

        # Привязываем обработчики событий выбора действия из выпадающего меню
        file_action.triggered.connect(self.select_file_source)
        folder_action.triggered.connect(self.select_folder_source)

        # Показываем выпадающее меню
        menu.exec_(self.select_button.mapToGlobal(self.select_button.rect().bottomLeft()))

    def select_file_source(self):
        filename = QFileDialog.getOpenFileName(self, "Выбрать файл", "/")
        if filename:
            self.source_line_edit.setText(filename[0])

    def select_folder_source(self):
        foldername = QFileDialog.getExistingDirectory(self, "Выбрать папку", "/")
        if foldername:
            self.source_line_edit.setText(foldername)

    def select_folder_target(self):
        foldername = QFileDialog.getExistingDirectory(self, "Сохранять в:", "/")
        if foldername:
            self.target_line_edit.setText(foldername)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.setGeometry(100, 100, 850, 600)
    main_window.show()
    sys.exit(app.exec_())
