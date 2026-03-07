# quiz_logic.py
import random
from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from questions import questions_easy, questions_normal, questions_hard, money_steps

class QuizLogic(QObject):
    # Signals to communicate with UI
    question_loaded = pyqtSignal(str, list)          # question text, options list
    money_updated = pyqtSignal(int)                  # current winnings
    timer_updated = pyqtSignal(int)                  # seconds left
    game_over = pyqtSignal(str)                       # message
    lifeline_used = pyqtSignal(str)                   # name of lifeline used (for disabling buttons)
    answer_feedback = pyqtSignal(bool, str)           # is_correct, message
    reset_ui = pyqtSignal()                            # reset UI after wrong answer or menu

    def __init__(self):
        super().__init__()
        self.all_questions = questions_easy + questions_normal + questions_hard
        self.questions = []
        self.current_index = 0
        self.score = 0
        self.used_questions = []
        self.lifelines_used = {"50-50": False, "Husu Audiensia": False, "Telefoni Kolega": False}
        self.timer = QTimer()
        self.timer.timeout.connect(self._timer_tick)
        self.time_left = 30
        self.current_question_data = None

    def start_new_game(self):
        """Shuffle all questions and reset state."""
        self.questions = random.sample(self.all_questions, len(self.all_questions))
        self.current_index = 0
        self.score = 0
        self.used_questions = []
        self.lifelines_used = {"50-50": False, "Husu Audiensia": False, "Telefoni Kolega": False}
        self.money_updated.emit(0)
        self._load_question()

    def _load_question(self):
        if self.current_index >= len(self.questions):
            self.game_over.emit(f"Parabéns! Ita manan $1,000,000!")
            return

        # Skip already used questions (though we shouldn't have repeats)
        q = self.questions[self.current_index]
        while q in self.used_questions:
            self.current_index += 1
            if self.current_index >= len(self.questions):
                self.game_over.emit(f"Quiz hotu! Ita manan ${money_steps.get(self.current_index-1, 0)}")
                return
            q = self.questions[self.current_index]

        self.used_questions.append(q)
        self.current_question_data = q
        self.question_loaded.emit(q["question"], q["options"])

        # Start timer
        self.time_left = 30
        self.timer_updated.emit(self.time_left)
        self.timer.start(1000)

    def _timer_tick(self):
        self.time_left -= 1
        self.timer_updated.emit(self.time_left)
        if self.time_left <= 0:
            self.timer.stop()
            self.answer_feedback.emit(False, "Tempu remata! Resposta la loos.")
            # Wrong answer => reset game (original behavior)
            self._reset_game()

    def submit_answer(self, answer_letter):
        """Check answer (call from UI)."""
        self.timer.stop()
        if not self.current_question_data:
            return

        correct = self.current_question_data["answer"]
        if answer_letter == correct:
            self.score += 1
            winnings = money_steps.get(self.current_index + 1, 0)
            self.money_updated.emit(winnings)
            self.answer_feedback.emit(True, "Resposta loos! Kontinua ba pergunta tuir mai.")
            self.current_index += 1
            self._load_question()
        else:
            self.answer_feedback.emit(False, f"Sala! Resposta loos mak {correct}.")
            self._reset_game()

    def _reset_game(self):
        """After wrong answer, go back to start screen."""
        self.timer.stop()
        self.game_over.emit("Game Over! Ita komesa fali.")
        # Reset all state but keep questions shuffled? Original resets completely.
        self.questions = []
        self.current_index = 0
        self.score = 0
        self.used_questions = []
        self.lifelines_used = {"50-50": False, "Husu Audiensia": False, "Telefoni Kolega": False}
        self.reset_ui.emit()  # tell UI to show start screen

    def use_lifeline(self, lifeline_name):
        if self.lifelines_used[lifeline_name]:
            self.answer_feedback.emit(False, f"{lifeline_name} tiha ona uza.")
            return

        self.lifelines_used[lifeline_name] = True
        self.lifeline_used.emit(lifeline_name)

        if lifeline_name == "50-50":
            self._fifty_fifty()
        elif lifeline_name == "Husu Audiensia":
            self._audience()
        elif lifeline_name == "Telefoni Kolega":
            self._phone_friend()

    def _fifty_fifty(self):
        if not self.current_question_data:
            return
        correct = self.current_question_data["answer"]
        options = self.current_question_data["options"]
        # Find two incorrect options to remove
        incorrect = [opt for opt in options if not opt.startswith(correct)]
        if len(incorrect) >= 2:
            to_remove = random.sample(incorrect, 2)
            # We'll send the letters of options to disable (like "A", "B")
            remove_letters = [opt[0] for opt in to_remove]
            # Let UI handle disabling buttons
            self.answer_feedback.emit(True, f"50-50: opsaun {', '.join(remove_letters)} husik tiha.")
            # We need a signal to tell UI which buttons to disable.
            # We'll reuse lifeline_used with extra data? Simpler: emit a custom signal.
            # For now, we'll just let UI handle it by knowing which options are still enabled?
            # Better: create a new signal fifty_fifty_result(list_of_letters_to_disable)
            # But to keep it simple, we'll store the info in a variable and UI can call a method.
            # Let's add a method to get disabled letters.
            self._fifty_fifty_remove = remove_letters
        else:
            self.answer_feedback.emit(False, "La bele uza 50-50 agora.")

    def _audience(self):
        correct = self.current_question_data["answer"]
        # Simulate audience suggestion (always suggests correct with high confidence)
        self.answer_feedback.emit(True, f"Audiensia sujere opsaun {correct} ho 85% votus.")

    def _phone_friend(self):
        correct = self.current_question_data["answer"]
        self.answer_feedback.emit(True, f"Telefoni kolega: 'Hili opsaun {correct}! Tenki certeza.'")

    def get_fifty_fifty_remove(self):
        """Return list of option letters to disable (e.g., ['A','C']) after 50-50."""
        return getattr(self, '_fifty_fifty_remove', [])