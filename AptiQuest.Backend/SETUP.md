# AptiQuest Backend

Backend API for **AptiQuest**, a cross-platform aptitude practice and learning application.

The backend is built with **Python + FastAPI** using a **Layered Architecture** and **SQL Server** as the relational database.

---

## 🛠️ Technology Stack

- **Language:** Python 3.14
- **Framework:** FastAPI
- **ASGI Server:** Uvicorn / FastAPI CLI
- **ORM:** SQLAlchemy
- **Database Migration:** Alembic
- **Database:** Microsoft SQL Server
- **SQL Server Driver:** ODBC Driver 18 for SQL Server
- **Password Hashing:** Argon2 via `pwdlib`
- **API Documentation:** Swagger UI / OpenAPI
- **Testing:** Pytest (planned / to be expanded)

---

## 🏗️ Architecture

AptiQuest Backend follows a **Layered Architecture**:

```text
Client
  │
  │ REST API
  ▼
Controller Layer
  │
  ▼
Service Layer
  │
  ▼
Repository Layer
  │
  ▼
SQLAlchemy Models
  │
  ▼
SQL Server
```

### Layers

| Layer | Responsibility |
|---|---|
| Controllers | API endpoints, HTTP requests and responses |
| Services | Business logic and validation |
| Repositories | Database access and queries |
| Models | SQLAlchemy database models |
| Schemas | Pydantic request/response models |
| Database | SQLAlchemy engine and database sessions |
| Core | Security, configuration and common utilities |

---

## 📁 Project Structure

```text
AptiQuest.Backend/
│
├── app/
│   ├── __init__.py
│   │
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── user_controller.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── user_service.py
│   │
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── user_repository.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── topic.py
│   │   ├── subtopic.py
│   │   ├── question.py
│   │   └── question_option.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── user_schema.py
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   └── database.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   └── security.py
│   │
│   └── main.py
│
├── migrations/
│   ├── versions/
│   ├── env.py
│   ├── README
│   └── script.py.mako
│
├── tests/
│
├── alembic.ini
├── requirements.txt
├── .gitignore
└── README.md
```

---

# 🚀 Setup on a New Windows System

Follow these steps when setting up AptiQuest Backend on a new computer.

## 1. Prerequisites

Install the following:

### Python

Install **Python 3.14 (64-bit)**.

Verify:

```powershell
python --version
```

Expected:

```text
Python 3.14.x
```

Verify pip:

```powershell
pip --version
```

> Python itself is free and open source.

---

## 2. Install Microsoft SQL Server

Install **Microsoft SQL Server** and make sure the SQL Server service is running.

The current development environment uses:

```text
Server: localhost
Instance: MSSQLSERVER
Database: AptiQuestDb
Authentication: Windows Authentication
```

Create the database in SQL Server if it does not already exist:

```sql
CREATE DATABASE AptiQuestDb;
GO
```

You can use **SQL Server Management Studio (SSMS)** to connect and manage the database.

---

## 3. Install SQL Server ODBC Driver

Install:

```text
ODBC Driver 18 for SQL Server
```

The backend currently uses:

```text
ODBC Driver 18 for SQL Server
```

Make sure the driver is installed before running the application.

---

# 📥 Clone the Repository

Open PowerShell or Git Bash:

```powershell
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

Move into the backend directory:

```powershell
cd AptiQuest.Backend
```

Check the files:

```powershell
dir
```

You should see files/folders such as:

```text
app
migrations
alembic.ini
requirements.txt
README.md
```

---

# 🐍 Create Python Virtual Environment

Create a project-specific virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

After activation, the terminal should show:

```text
(.venv)
```

For example:

```text
(.venv) PS C:\Project\git\AptiQuest\AptiQuest.Backend>
```

---

## If PowerShell blocks activation

If you receive an execution-policy error, you can activate using Command Prompt instead:

```cmd
.venv\Scripts\activate.bat
```

Or use the Python executable directly without activating the environment:

```powershell
.\.venv\Scripts\python.exe --version
```

---

# 📦 Install Backend Dependencies

Make sure the virtual environment is active.

Install all dependencies from `requirements.txt`:

```powershell
pip install -r requirements.txt
```

If `requirements.txt` does not exist yet, install the main dependencies manually:

```powershell
pip install "fastapi[standard]"
pip install sqlalchemy
pip install alembic
pip install pyodbc
pip install "pwdlib[argon2]"
pip install email-validator
```

Then generate the requirements file:

```powershell
pip freeze > requirements.txt
```

---

# 🔧 Configure Database Connection

The backend uses SQLAlchemy to connect to SQL Server.

The development connection currently targets:

```text
localhost
```

and:

```text
AptiQuestDb
```

with Windows Authentication.

The SQLAlchemy connection uses:

```text
mssql+pyodbc
```

and:

```text
ODBC Driver 18 for SQL Server
```

### Important

Do not commit database passwords, API keys, JWT secrets, or other sensitive credentials to GitHub.

The project should eventually use:

```text
.env
```

for environment-specific configuration.

`.env` should be included in `.gitignore`.

---

# 🗄️ Database Migrations

AptiQuest uses **Alembic** to manage database schema changes.

Do not manually create application tables in SSMS when a migration should be used.

The migration workflow is:

```text
SQLAlchemy Model
       ↓
Alembic Autogenerate
       ↓
Migration File
       ↓
Review Migration
       ↓
Alembic Upgrade
       ↓
SQL Server
```

---

## Apply Existing Migrations

After cloning the project and configuring SQL Server:

```powershell
alembic upgrade head
```

This applies all committed migrations to the database.

The initial migration creates the current Sprint 1 tables:

```text
Users
Topics
SubTopics
Questions
QuestionOptions
```

---

## Check Migration Status

```powershell
alembic current
```

To see migration history:

```powershell
alembic history
```

---

## Create a New Migration

After modifying a SQLAlchemy model:

```powershell
alembic revision --autogenerate -m "Describe the change"
```

Example:

```powershell
alembic revision --autogenerate -m "Add date of birth to users"
```

Always inspect the generated migration before applying it.

Then run:

```powershell
alembic upgrade head
```

---

# ▶️ Run the FastAPI Backend

From the project root:

```powershell
fastapi dev app/main.py
```

Alternatively:

```powershell
python -m uvicorn app.main:app --reload
```

The development server should run at:

```text
http://127.0.0.1:8000
```

---

# 📚 API Documentation

FastAPI automatically provides Swagger UI.

Open:

```text
http://127.0.0.1:8000/docs
```

Alternative API documentation:

```text
http://127.0.0.1:8000/redoc
```

---

# ❤️ Health Check

The backend contains a health endpoint:

```http
GET /health
```

Open:

```text
http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "healthy"
}
```

---

# 👤 Current API — User Registration

The first implemented API is user registration.

```http
POST /api/users/register
```

Example request:

```json
{
  "first_name": "John",
  "last_name": "Doe",
  "username": "johndoe",
  "email": "john@example.com",
  "password": "StrongPassword123!"
}
```

The password is **not stored as plain text**.

It is hashed using **Argon2** before being stored in SQL Server.

```text
Plain Password
      ↓
    Argon2
      ↓
Password Hash
      ↓
SQL Server
```

The original password cannot be decrypted from the stored hash.

The API response does not expose the password or password hash.

---

# 🗃️ Current Database Tables

The current Sprint 1 database contains:

### Users

Stores application users and account information.

### Topics

Stores major aptitude categories.

Example:

```text
Quantitative Aptitude
Logical Reasoning
Verbal Ability
```

### SubTopics

Stores topics within a major topic.

Example:

```text
Quantitative Aptitude
 ├── Percentage
 ├── Profit & Loss
 ├── Time & Work
 └── Probability
```

### Questions

Stores aptitude questions.

### QuestionOptions

Stores the options associated with each question.

A multiple-choice question currently supports four options through application/business rules.

---

# 🔐 Git & Security

The following files/directories should **not** be committed:

```text
.venv/
.idea/
__pycache__/
*.pyc
.env
```

The following should be committed:

```text
app/
migrations/
alembic.ini
requirements.txt
README.md
.gitignore
```

### Important

Never commit:

```text
Database passwords
API keys
JWT secrets
AI provider keys
Private credentials
```

Use `.env` for secrets and provide an `.env.example` file containing only placeholder values.

---

# 🧪 Development Workflow

When developing a new feature:

```text
1. Create / modify SQLAlchemy Model
            ↓
2. Create Pydantic Schema
            ↓
3. Create Repository
            ↓
4. Create Service
            ↓
5. Create Controller
            ↓
6. Create / update Alembic migration
            ↓
7. Apply migration
            ↓
8. Test API using Swagger
```

Example:

```text
Question Feature
      ↓
Question Model
      ↓
Question Schema
      ↓
Question Repository
      ↓
Question Service
      ↓
Question Controller
      ↓
SQL Server
```

---

# 🧭 Current Development Roadmap

## Sprint 1 — Foundation

- [x] FastAPI project setup
- [x] Layered architecture
- [x] SQLAlchemy setup
- [x] SQL Server connection
- [x] Alembic setup
- [x] User model
- [x] Topic model
- [x] SubTopic model
- [x] Question model
- [x] QuestionOption model
- [x] Initial database migration
- [x] User registration API
- [x] Password hashing with Argon2

## Sprint 2 — Authentication

- [ ] User login
- [ ] Password verification
- [ ] JWT access token
- [ ] Refresh token
- [ ] Authentication dependencies
- [ ] Protected endpoints

## Sprint 3 — Question Management

- [ ] Create question API
- [ ] Update question API
- [ ] Delete question API
- [ ] Get question API
- [ ] Topic APIs
- [ ] SubTopic APIs
- [ ] Question filtering
- [ ] Difficulty filtering

## Sprint 4 — Practice Engine

- [ ] Practice sessions
- [ ] Submit answers
- [ ] Answer history
- [ ] Score calculation
- [ ] Timer tracking

## Sprint 5 — Analytics

- [ ] Accuracy
- [ ] Topic performance
- [ ] Difficulty performance
- [ ] Time analysis
- [ ] Progress tracking
- [ ] Dashboard APIs

## Future

- [ ] Gamification
- [ ] Streaks
- [ ] Achievements
- [ ] Friends
- [ ] Leaderboards
- [ ] Personalized recommendations
- [ ] AI explanations
- [ ] AI hints
- [ ] AI-generated questions
- [ ] AI tutor
- [ ] RAG / knowledge base

---

# 👨‍💻 Development Notes

This project is currently under active development.

The backend is intentionally being developed as a **modular monolithic application using Layered Architecture**. Microservices are not required at the current stage and can be considered later if the application's scale justifies them.

The backend is designed to serve both:

```text
Flutter Mobile App
        │
        ▼
    FastAPI
        ▲
        │
React + TypeScript Web App
```

Both frontend applications will consume the same REST API.

---

## 📌 Quick Start

For an already-configured new machine:

```powershell
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd AptiQuest.Backend

python -m venv .venv
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt

alembic upgrade head

fastapi dev app/main.py
```

Then open:

```text
http://127.0.0.1:8000/docs
```

---

## 📄 License

License information will be added when the project is ready for public distribution.
