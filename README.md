# 🏙️ Monopoly

A digital clone of the classic board game **Monopoly**.  
Players join a room, take turns, roll the dice, and move around the board in real time via WebSocket.

> **Current Status:**  
> MVP demo with a live board, turn order, and synchronized dice/piece animations.  
> Property purchase and rent are not yet implemented — planned for future iterations.

---

## 📸 Screenshot

| Room Lobby & Game Board (2 players) |
|--------------------------------------|
| ![image](https://github.com/user-attachments/assets/e6c86a27-99ca-48e8-9714-2f3ff2444776) |

---

## ⚙️ Tech Stack

| Stack | Why chosen |
|-------|------------|
| **Python 3.10 + Django 4.2** | familiar, fast CRUD, migrations |
| **Channels 3 + Daphne 3** | WebSocket on ASGI without extra services |
| **SQLite** | simplest DB for offline testing |
| **Bootstrap 5** | quick UI prototyping |
| **ES6 modules + Vanilla JS** | easier debugging without bundlers |

*For deployment, migration to PostgreSQL, Gunicorn, and Nginx is planned.*

---

## 🚀 Installation & Local Run

```bash
git clone https://github.com/<your-user>/Monopoly.git
cd Monopoly
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
