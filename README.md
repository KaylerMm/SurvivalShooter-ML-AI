# 🧠 Machine Learning 2D Shooter (Python)

An AI-enhanced 2D shooter game built in **Python** using **Pygame**, where the enemy learns and adapts to the player's movements using **Random Forest Regression**. As you play, the AI gets smarter, making dodging projectiles increasingly difficult!

---

## 🎮 Gameplay Overview

In this 2D shooter:
- You control the player, dodging bullets.
- The enemy uses machine learning to predict where you’ll move next.
- Each game session records your movement and velocity.
- After each game over, the AI model is retrained to aim more accurately in future rounds.

---

## 🤖 Machine Learning

| Feature               | Details                                           |
|-----------------------|---------------------------------------------------|
| **Algorithm**         | `RandomForestRegressor` (from scikit-learn)       |
| **Inputs**            | `x`, `y`, `vx`, `vy`, `timestamp`                |
| **Target Output**     | Next predicted position of the player            |
| **Data Format**       | CSV (`data/player_moves.csv`)                    |
| **Training Trigger**  | Automatically retrains at every game over        |
| **Behavior**          | Uses predictions to aim bullets at future positions |

---

## 📦 Tech Stack

- 🐍 **Python 3**
- 🎮 **Pygame** — for game loop, rendering, and input
- 🧠 **scikit-learn** — for AI model training
- 📁 **CSV** — for logging player movement

---

## 🚀 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/Machine-Learning-2D-Shooter-Python.git
cd Machine-Learning-2D-Shooter-Python
```

### 2. Install dependencies
Make sure Python 3.8+ is installed.

```bash
pip install -r requirements.txt
```

Or manually install:

```bash

pip install pygame scikit-learn
```

### 3. Run the game
```bash
python main.py
```

## 📁 File Structure
```graphql
.
├── ai/
│   └── trainer.py            # Trains the RandomForest model
├── data/
│   └── player_moves.csv      # Movement data saved between sessions
├── game/
│   ├── player.py             # Player class and controls
│   └── enemy.py              # Enemy with AI aiming logic
├── sounds/
│   ├── background_music.mp3
│   └── click.mp3
├── main.py                   # Main game loop and UI
└── README.md
```

## 🛠️ Future Improvements
💾 Save/load trained models to avoid retraining on every run

⚙️ Use multithreading for training during gameplay

📈 Add score leaderboard and difficulty scaling

🧬 Try LSTM or other sequence models for more accurate prediction

🌐 Create a web-based version with Pygbag or similar

## 📜 License
This project is licensed under the MIT License — use freely and contribute if you'd like!

## 🙌 Acknowledgments
Built for fun and experimentation at the intersection of AI + Games

Inspired by classic arcade games and modern ML ideas

Shoutout to the open-source community!

### Enjoy trying to beat your own AI!