# 🏙️ Monopoly

Цифровой клон настольной «Монополии».  
Игроки подключаются к комнате, получают по-очерёдный ход, бросают кубик и перемещаются по клеткам поля в реальном времени через WebSocket.

> **Текущий статус:**  
> MVP-демо с живым полем, очередностью ходов и синхронной анимацией кубика/фишек.  
> Нет покупки собственности и аренды — запланировано в следующих итерациях.

---

## 📸 Скриншот

| Лобби комнаты и поле (2 игрока) |
|---------------------------------|
| ![image](https://github.com/user-attachments/assets/e6c86a27-99ca-48e8-9714-2f3ff2444776) |

---

## ⚙️ Технологии

| Стек | Зачем выбран |
|------|--------------|
| **Python 3.10 + Django 4.2** | знакомый, быстрый CRUD, миграции |
| **Channels 3 + Daphne 3** | WebSocket на ASGI без внешних сервисов |
| **SQLite** | простейшая БД для офлайн-тестов |
| **Bootstrap 5** | быстрый прототип UI |
| **ES6 modules + Vanilla JS** | легче дебажить без сборщиков |

*При деплое планируется перейти на PostgreSQL, Gunicorn и Nginx.*

---

## 🚀 Установка и запуск (локально)

```bash
git clone https://github.com/<your-user>/Monopoly.git
cd Monopoly
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
