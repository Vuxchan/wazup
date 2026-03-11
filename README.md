# Project Chat App

A fullstack chat application built with FastAPI (backend) and React + Vite (frontend).

---

# 1. Prerequisites

Make sure the following tools are installed:

* Python 3.10+
* Node.js 18+
* npm
* PostgreSQL 
* Git

---

# 2. Clone repository

```bash
git clone https://github.com/Vuxchan/project-chatapp.git
cd project-chatapp
```

---

# 3. Backend setup (FastAPI)

Move to backend directory:

```bash
cd backend
```

Create virtual environment:

```bash
python -m venv venv
```

Activate virtual environment:

Linux / macOS

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env` file:

Run database migrations:

```bash
alembic upgrade head
```

Run backend server:

```bash
cd src
fastapi dev main.py
```

---

# 4. Frontend setup (React + Vite)

Open a new terminal and move to frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Run development server:

```bash
npm run dev
```

---

# 5. Technologies used

Backend:

* FastAPI
* SQLAlchemy
* Alembic
* JWT Authentication

Frontend:

* React
* Vite
* TailwindCSS
