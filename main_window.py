# main_window.py
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QStackedWidget,
                             QMessageBox, QFrame)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QPalette, QColor, QLinearGradient, QBrush
from quiz_logic import QuizLogic
from questions import money_steps

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quiz: How to Be a Millionaire")
        self.setGeometry(100, 100, 900, 700)
        self.setMinimumSize(800, 600)

        # Apply dark gradient background
        self.setStyleSheet("""
            QMainWindow {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                                  stop:0 #0a0f0f, stop:1 #1a2a2a);
            }
            QLabel {
                color: #f0e68c;
                font-weight: bold;
            }
            QPushButton {
                background-color: #2b3b3b;
                color: #ffd700;
                border: 2px solid #c5a028;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #3f5a5a;
                border-color: #ffd700;
            }
            QPushButton:pressed {
                background-color: #1f2f2f;
            }
            QPushButton:disabled {
                background-color: #4d4d4d;
                color: #a0a0a0;
                border-color: #7a7a7a;
            }
            QFrame {
                border-radius: 15px;
                background-color: rgba(0, 0, 0, 0.6);
            }
        """)

        # Central widget and stacked layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.stack = QStackedWidget(self.central_widget)
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.addWidget(self.stack)

        # Create pages
        self.start_page = self.create_start_page()
        self.game_page = self.create_game_page()

        self.stack.addWidget(self.start_page)
        self.stack.addWidget(self.game_page)

        # Connect logic
        self.logic = QuizLogic()
        self.connect_signals()

        # Show start page
        self.stack.setCurrentWidget(self.start_page)

    def create_start_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("How to Be a Millionaire")
        title.setFont(QFont("Arial", 32, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #ffd700; padding: 20px;")

        start_btn = QPushButton("Hahu Jogus")
        start_btn.setFont(QFont("Arial", 20))
        start_btn.clicked.connect(self.start_game)
        start_btn.setFixedSize(250, 60)

        about_btn = QPushButton("Konaba Jogus")
        about_btn.setFont(QFont("Arial", 20))
        about_btn.clicked.connect(self.show_about)
        about_btn.setFixedSize(250, 60)

        layout.addWidget(title)
        layout.addSpacing(30)
        layout.addWidget(start_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(20)
        layout.addWidget(about_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        return page

    def create_game_page(self):
        page = QWidget()
        main_layout = QVBoxLayout(page)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Top frame: money and timer
        top_frame = QFrame()
        top_frame.setFrameShape(QFrame.Shape.StyledPanel)
        top_layout = QHBoxLayout(top_frame)

        self.money_label = QLabel("Osan: $0")
        self.money_label.setFont(QFont("Arial", 18))
        self.money_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.timer_label = QLabel("⏳ 30")
        self.timer_label.setFont(QFont("Arial", 18))
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.timer_label.setStyleSheet("color: #ffaa00;")

        top_layout.addWidget(self.money_label)
        top_layout.addStretch()
        top_layout.addWidget(self.timer_label)

        main_layout.addWidget(top_frame)

        # Question frame
        question_frame = QFrame()
        question_frame.setFrameShape(QFrame.Shape.StyledPanel)
        q_layout = QVBoxLayout(question_frame)
        self.question_label = QLabel("")
        self.question_label.setFont(QFont("Arial", 18))
        self.question_label.setWordWrap(True)
        self.question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        q_layout.addWidget(self.question_label)
        main_layout.addWidget(question_frame)

        # Options frame
        options_frame = QFrame()
        options_frame.setFrameShape(QFrame.Shape.StyledPanel)
        options_layout = QVBoxLayout(options_frame)
        self.option_buttons = []
        for i in range(4):
            btn = QPushButton("")
            btn.setFont(QFont("Arial", 14))
            btn.setMinimumHeight(50)
            btn.clicked.connect(lambda checked, idx=i: self.on_option_clicked(idx))
            options_layout.addWidget(btn)
            self.option_buttons.append(btn)
        main_layout.addWidget(options_frame)

        # Lifelines frame
        lifelines_frame = QFrame()
        lifelines_frame.setFrameShape(QFrame.Shape.StyledPanel)
        lifelines_layout = QHBoxLayout(lifelines_frame)

        self.fifty_btn = QPushButton("50-50")
        self.fifty_btn.clicked.connect(lambda: self.logic.use_lifeline("50-50"))
        self.audience_btn = QPushButton("Husu Audiensia")
        self.audience_btn.clicked.connect(lambda: self.logic.use_lifeline("Husu Audiensia"))
        self.phone_btn = QPushButton("Telefoni Kolega")
        self.phone_btn.clicked.connect(lambda: self.logic.use_lifeline("Telefoni Kolega"))
        self.back_btn = QPushButton("Fila Fali Ba Menu")
        self.back_btn.clicked.connect(self.back_to_menu)

        lifelines_layout.addWidget(self.fifty_btn)
        lifelines_layout.addWidget(self.audience_btn)
        lifelines_layout.addWidget(self.phone_btn)
        lifelines_layout.addWidget(self.back_btn)

        main_layout.addWidget(lifelines_frame)

        return page

    def connect_signals(self):
        self.logic.question_loaded.connect(self.display_question)
        self.logic.money_updated.connect(self.update_money)
        self.logic.timer_updated.connect(self.update_timer)
        self.logic.game_over.connect(self.on_game_over)
        self.logic.answer_feedback.connect(self.show_feedback)
        self.logic.reset_ui.connect(self.back_to_menu)
        self.logic.lifeline_used.connect(self.on_lifeline_used)

    def display_question(self, question, options):
        self.question_label.setText(question)
        for i, btn in enumerate(self.option_buttons):
            btn.setText(options[i])
            btn.setEnabled(True)  # re-enable after 50-50

    def update_money(self, amount):
        self.money_label.setText(f"Osan: ${amount}")

    def update_timer(self, seconds):
        self.timer_label.setText(f"⏳ {seconds}")

    def on_option_clicked(self, idx):
        # Map button index to letter A, B, C, D
        letters = ['A', 'B', 'C', 'D']
        self.logic.submit_answer(letters[idx])

    def on_game_over(self, message):
        QMessageBox.information(self, "Game Over", message)
        self.back_to_menu()

    def show_feedback(self, is_correct, msg):
        QMessageBox.information(self, "Feedback", msg)

    def on_lifeline_used(self, lifeline):
        # Disable the corresponding button
        if lifeline == "50-50":
            self.fifty_btn.setEnabled(False)
            # Also disable two wrong options
            remove_letters = self.logic.get_fifty_fifty_remove()
            for btn in self.option_buttons:
                if btn.text() and btn.text()[0] in remove_letters:
                    btn.setEnabled(False)
        elif lifeline == "Husu Audiensia":
            self.audience_btn.setEnabled(False)
        elif lifeline == "Telefoni Kolega":
            self.phone_btn.setEnabled(False)

    def start_game(self):
        self.stack.setCurrentWidget(self.game_page)
        self.logic.start_new_game()
        # Reset lifeline buttons
        self.fifty_btn.setEnabled(True)
        self.audience_btn.setEnabled(True)
        self.phone_btn.setEnabled(True)

    def back_to_menu(self):
        self.stack.setCurrentWidget(self.start_page)

    def show_about(self):
        about_text = (
            "Bem Vindo iha Quiz 'How to Be a Millionaire'!\n\n"
            "Regulamentus Jogus:\n"
            "1. Hatan Perguntas ho Lolos hodi Manan Osan.\n"
            "2. Difikuldade aumenta tuir resposta.\n"
            "3. Hahu husi $100 no bele to $1 miliaun.\n"
            "4. Ajuda: 50-50, Husu Audiensia, Telefoni Kolega.\n\n"
            "Tabela Osan:\n" +
            "\n".join([f"{k}. ${v}" for k, v in money_steps.items()])
        )
        QMessageBox.information(self, "Konaba Jogus", about_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())