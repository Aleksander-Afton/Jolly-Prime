import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit, QTextEdit
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from playsound import playsound
import os

class AssistantGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Мой ассистент')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.central_widget = QWidget()
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)

        self.chat_display = QTextEdit()  # Окошко для отображения чата
        self.chat_display.setReadOnly(True)  # Сделаем его только для чтения
        layout.addWidget(self.chat_display)

        self.web_view = QWebEngineView()  # Окошко для отображения веб-страницы
        self.web_view.setMinimumSize(800, 300)  # Установите минимальный размер с увеличенной высотой
        layout.addWidget(self.web_view)

        send_button = QPushButton('Отправить')
        layout.addStretch()
        layout.addWidget(send_button, alignment=Qt.AlignBottom)

        self.command_input = QLineEdit()
        layout.addWidget(self.command_input, alignment=Qt.AlignBottom)
        send_button.clicked.connect(self.handle_command)

        self.show_chat()  # Показываем окошко с чатом по умолчанию

    def handle_command(self):
        user_input = self.command_input.text()
        current_time = time.strftime('%H:%M:%S')
        self.chat_display.append(f"{current_time} - Вы: {user_input}")

        if user_input.startswith('поиск'):
            query = user_input[6:]
            self.load_web_page(query)
            self.hide_chat()  # Скрываем окошко с чатом
        elif user_input.startswith('открой'):
            program_name = user_input[7:]
            self.open_program(program_name)
            self.chat_display.append(f"{current_time} - Ассистент: Открываю программу: {program_name}")
        else:
            self.show_chat()  # Показываем окошко с чатом

        self.command_input.clear()

    def load_web_page(self, query):
        search_url = f"https://www.google.com/search?q={query}"
        self.web_view.setUrl(QUrl(search_url))  # Отображаем веб-страницу

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.show_chat()  # Показываем окошко с чатом
            self.web_view.setVisible(False)  # Скрываем окошко с веб-просмотром

    def hide_chat(self):
        self.chat_display.setVisible(False)
        self.web_view.setVisible(True)

    def show_chat(self):
        self.chat_display.setVisible(True)
        self.web_view.setVisible(False)

    def open_program(self, program_name):
        os.system(f'start "" "{program_name}"')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    playsound("welcome_to_jolly_prime.wav")  # Воспроизведение аудио
    assistant = AssistantGUI()
    assistant.show()

    sys.exit(app.exec_())
