from PySide6 import QtWidgets
from api_ninjas import api_ninjas
from api_labelf import api_labelf


class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QtWidgets.QVBoxLayout()

        # Заголовки
        labels = QtWidgets.QHBoxLayout()
        label1 = QtWidgets.QLabel("Введите текст 1")
        label2 = QtWidgets.QLabel("Введите текст 2")
        labels.addWidget(label1)
        labels.addWidget(label2)

        # Поля для сравниваемых текстов
        inputs = QtWidgets.QHBoxLayout()
        self.input1 = QtWidgets.QTextEdit()
        self.input2 = QtWidgets.QTextEdit()
        inputs.addWidget(self.input1)
        inputs.addWidget(self.input2)

        # Кнопка сравнения
        self.button = QtWidgets.QPushButton("Сравнить")
        self.button.clicked.connect(self.on_clicked)

        # Результаты сравнения
        self.result = QtWidgets.QTextEdit()
        self.result.setVisible(False)
        self.result.setPlaceholderText("Результат сравнения появится здесь...")

        main_layout.addLayout(labels)
        main_layout.addLayout(inputs)
        main_layout.addWidget(self.button)
        main_layout.addWidget(self.result)

        self.setLayout(main_layout)
        self.setWindowTitle("Сравнение текстов")
        self.resize(600, 400)

    def on_clicked(self):
        """Функция сравнения текстов при нажатии на кнопку"""

        text1 = self.input1.toPlainText()
        text2 = self.input2.toPlainText()

        score1 = api_ninjas(text1, text2)
        score2 = api_labelf(text1, text2)

        result = f"Результат сравнения api_ninjas - схожесть: {score1}\n"
        result += f"Результат сравнения api_labelf - схожесть: {score2}"

        self.result.setPlainText(result)
        self.result.setVisible(True)
