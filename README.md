# 💰 Quiz Game: How to Be a Millionaire (Tetum Edition)

*A high-stakes, interactive trivia application built with Python and PyQt6, featuring lifelines, difficulty scaling, and a dark-mode "Fusion" interface.*

---

## 📖 Description
Inspired by the world-famous game show, this application challenges users to answer increasingly difficult questions to reach the $1,000,000 prize. The project demonstrates advanced **GUI development**, **Signal-Slot communication**, and **Game Logic separation** in Python. 

The game is fully localized in **Tetum**, making it an engaging educational tool for the Timorese community.

## 🚀 Key Features
* **Dynamic Difficulty:** Questions are categorized into Easy, Normal, and Hard levels, with the prize money increasing at each stage.
* **Classic Lifelines:**
  * **50-50:** Automatically removes two incorrect options.
  * **Husu Audiensia (Ask the Audience):** Simulates audience feedback with high-confidence suggestions.
  * **Telefoni Kolega (Phone a Friend):** Get a "call" from a friend to help with the answer.
* **Timed Gameplay:** A 30-second countdown timer adds pressure to every question.
* **Responsive "Fusion" UI:** A sleek, dark-gradient interface optimized for laptop screens with real-time feedback animations.
* **Automated Money Progression:** Tracks winnings from $100 up to the $1 Million milestone.

## 🛠️ Tech Stack
* **Language:** Python 3.11+
* **Framework:** PyQt6 (GUI)
* **Logic:** Object-Oriented Programming (OOP)
* **Styling:** QSS (Qt Style Sheets) with Linear Gradients

## 📁 Repository Structure
* **`main_app.py`**: The entry point that initializes the PyQt6 application.
* **`main_window.py`**: Manages the UI layouts, buttons, timer displays, and screen switching (StackedWidgets).
* **`quiz_logic.py`**: The "Brain" of the game. Handles score tracking, timer logic, and lifeline calculations.
* **`questions.py`**: The database containing the trivia questions and the money progression table.

## ⚙️ Installation & Usage

### 1. Prerequisites
Ensure you have Python installed on your system.

### 2. Install Dependencies
```bash
pip install PyQt6
