# 🎯 AptiQuest

> **Learn. Practice. Analyze. Improve.**

AptiQuest is a cross-platform aptitude practice and learning platform designed to help students and job seekers practice aptitude questions consistently, track their performance, identify weak areas, and improve through personalized practice.

The platform is designed for **daily micro-learning**, making it convenient to practice whenever you have free time — while travelling, waiting, or during short breaks.

AptiQuest provides both a **mobile application** and a **web application**, powered by a common backend API.

---

## 🚀 Features

### 📚 Aptitude Practice

* Topic-wise aptitude practice
* Multiple difficulty levels

  * Easy
  * Medium
  * Hard
* Random question practice
* Practice sessions
* Question explanations
* Hints and shortcuts
* Bookmark questions
* Review previously attempted questions

### ⏱️ Test & Challenge Modes

* Timed tests
* Custom practice tests
* Daily challenges
* Topic-based tests
* Full aptitude tests
* Instant test results

### 📊 Performance Analytics

Track your progress with detailed analytics:

* Overall accuracy
* Questions attempted
* Questions answered correctly
* Average time per question
* Topic-wise performance
* Difficulty-wise performance
* Strong topics
* Weak topics
* Daily / weekly / monthly progress
* Practice history
* Performance trends

### 🎯 Personalized Recommendations

AptiQuest analyzes your practice history and recommends:

* Topics that need improvement
* Questions for revision
* Appropriate difficulty levels
* Previously incorrect questions
* Personalized daily practice

### 🔥 Gamification

Stay motivated through:

* Daily streaks
* XP and levels
* Achievements
* Daily goals
* Progress tracking
* Leaderboards
* Friend comparisons

### 🤖 AI Features

AI capabilities are planned to make AptiQuest more intelligent and personalized.

Potential AI features include:

* AI-powered question explanations
* Step-by-step solutions
* AI hints
* Similar question generation
* Personalized practice generation
* AI aptitude tutor
* Personalized study plans
* Intelligent recommendations
* Question difficulty analysis

---

# 🏗️ System Architecture

AptiQuest consists of two frontend applications and one common backend.

```text
                         ┌──────────────────────┐
                         │   Flutter Mobile     │
                         │   Android / iOS      │
                         └──────────┬───────────┘
                                    │
                                    │ REST API
                                    │
                         ┌──────────▼───────────┐
                         │ React + TypeScript    │
                         │      Web App          │
                         └──────────┬───────────┘
                                    │
                                    │
                                    ▼
                     ┌───────────────────────────┐
                     │     FastAPI Backend       │
                     │          Python           │
                     │                           │
                     │    Layered Architecture   │
                     └─────────────┬─────────────┘
                                   │
                                   ▼
                          ┌─────────────────┐
                          │ SQLAlchemy ORM  │
                          └────────┬────────┘
                                   │
                                   ▼
                          ┌─────────────────┐
                          │  SQL Server DB  │
                          │  AptiQuestDb    │
                          └─────────────────┘
```

---

# 🛠️ Technology Stack

## Frontend

### Mobile

* **Flutter**
* Dart
* Riverpod
* REST API integration
* Local storage / caching
* Responsive UI

### Web

* **React**
* **TypeScript**
* Vite
* React Router
* REST API integration
* Charting and analytics
* Responsive design

---

## Backend

* **Python**
* **FastAPI**
* Pydantic
* SQLAlchemy
* Alembic
* JWT Authentication
* RESTful APIs
* Pytest

---

## Database

* **Microsoft SQL Server**
* SQLAlchemy ORM
* Alembic migrations

---

## AI & Intelligent Features

The AI layer will be implemented using the Python ecosystem and will be designed to support:

* LLM integration
* AI-generated explanations
* Question generation
* Recommendation systems
* Embeddings
* Vector search / RAG
* AI tutoring

AI providers and models can be integrated independently without tightly coupling them to the core application.

---

# 🏛️ Backend Architecture

AptiQuest uses a **Layered Architecture**.

```text
┌──────────────────────────────┐
│        Controller Layer      │
│       API / HTTP Requests    │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│         Service Layer        │
│        Business Logic        │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│       Repository Layer       │
│       Database Operations    │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│        SQLAlchemy ORM        │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│        SQL Server DB         │
└──────────────────────────────┘
```

### Backend Layers

| Layer      | Responsibility                                           |
| ---------- | -------------------------------------------------------- |
| Controller | Handles HTTP requests and responses                      |
| Service    | Contains business logic                                  |
| Repository | Handles database operations                              |
| Model      | Represents database entities                             |
| Schema     | Handles API request/response validation                  |
| Database   | Database connection and session management               |
| Core       | Configuration, security, exceptions and common utilities |

---

# 📁 Project Structure

```text
AptiQuest/
│
├── Backend/
│   └── AptiQuest.Backend/
│       │
│       ├── app/
│       │   │
│       │   ├── controllers/
│       │   ├── services/
│       │   ├── repositories/
│       │   ├── models/
│       │   ├── schemas/
│       │   │
│       │   ├── core/
│       │   │   ├── config.py
│       │   │   ├── security.py
│       │   │   ├── exceptions.py
│       │   │   └── logging.py
│       │   │
│       │   └── database/
│       │       ├── connection.py
│       │       └── session.py
│       │
│       ├── migrations/
│       ├── tests/
│       ├── main.py
│       ├── .env
│       ├── pyproject.toml
│       └── README.md
│
├── Mobile/
│   └── AptiQuest.Mobile/
│       ├── lib/
│       │   ├── app/
│       │   ├── core/
│       │   ├── features/
│       │   ├── shared/
│       │   └── main.dart
│       │
│       ├── assets/
│       └── pubspec.yaml
│
├── Web/
│   └── AptiQuest.Web/
│       ├── src/
│       │   ├── app/
│       │   ├── assets/
│       │   ├── components/
│       │   ├── core/
│       │   ├── features/
│       │   ├── hooks/
│       │   ├── layouts/
│       │   ├── pages/
│       │   ├── routes/
│       │   ├── services/
│       │   ├── types/
│       │   └── utils/
│       │
│       ├── package.json
│       └── tsconfig.json
│
├── Database/
│
├── Docs/
│
├── Postman/
│
└── README.md
```

---

# 🧩 Core Backend Modules

The backend will be divided into independent functional modules.

```text
Authentication
Users
Topics
Questions
Practice
Tests
Analytics
Recommendations
Achievements
Friends
Notifications
AI
Admin
```

### Authentication

* User registration
* Login
* JWT authentication
* Token management
* Password management
* Authentication security

### Questions

* Topics
* Subtopics
* Questions
* Options
* Difficulty levels
* Explanations
* Hints
* Question tags

### Practice

* Start practice
* Submit answers
* Skip questions
* Track time
* Calculate score
* Track attempts
* Resume sessions

### Tests

* Timed tests
* Mock tests
* Daily challenges
* Test results
* Test history

### Analytics

* Accuracy
* Speed
* Topic performance
* Difficulty performance
* Progress trends
* Weak/strong areas

### Recommendations

* Personalized practice
* Weak-topic recommendations
* Revision questions
* Difficulty adjustment

### Gamification

* XP
* Levels
* Streaks
* Achievements
* Daily goals
* Leaderboards

---

# 🗄️ Database

The application uses **Microsoft SQL Server** as the primary relational database.

Initial database entities will include:

```text
Users
Roles
Topics
SubTopics
Questions
QuestionOptions
PracticeSessions
PracticeAnswers
Tests
TestQuestions
TestResults
Bookmarks
Mistakes
UserStats
DailyGoals
Achievements
UserAchievements
Friends
Notifications
RefreshTokens
```

Database schema changes will be managed using **Alembic migrations** rather than manually modifying the production database.

---

# 🔌 API Architecture

Both frontend applications communicate with the same backend.

```text
Flutter ────────┐
                │
                ├── REST API ──► FastAPI
                │
React ──────────┘
```

Example API endpoints:

```text
/api/auth/login
/api/auth/register

/api/users/profile

/api/topics
/api/questions

/api/practice/start
/api/practice/answer
/api/practice/result

/api/tests
/api/tests/start
/api/tests/submit

/api/dashboard
/api/analytics
/api/recommendations

/api/achievements
/api/friends
/api/notifications

/api/ai/explanation
/api/ai/hint
/api/ai/generate
```

---

# 🔐 Security

Security will be considered across all layers.

Planned features include:

* JWT-based authentication
* Secure password hashing
* Role-based authorization
* Input validation
* API request validation
* Environment-based secrets
* CORS configuration
* Rate limiting
* Secure database access
* Exception handling

Sensitive configuration will be stored using environment variables and will **not be committed to Git**.

---

# 📱 Mobile Application

The Flutter application is designed primarily for **quick daily practice**.

Typical use cases:

```text
Travelling
   ↓
Open AptiQuest
   ↓
Quick Practice
   ↓
5 / 10 Questions
   ↓
Instant Results
   ↓
Progress Updated
```

The mobile application will also support offline-friendly functionality where appropriate.

---

# 🌐 Web Application

The React + TypeScript application will provide a richer interface for:

* Detailed analytics
* Performance dashboards
* Practice sessions
* Tests
* Leaderboards
* Question browsing
* Profile management
* Administration
* Question management
* Data visualization

---

# 📊 Dashboard

The dashboard will provide a complete overview of the user's progress.

```text
┌──────────────────────────────────────────┐
│              AptiQuest Dashboard         │
├──────────────────────────────────────────┤
│                                          │
│  🔥 Streak       ⭐ XP       🎯 Goal     │
│                                          │
│  Questions Solved       Accuracy         │
│        1,250              82%             │
│                                          │
│  ───────── Topic Performance ─────────   │
│                                          │
│  Percentage              92%             │
│  Time & Work             76%             │
│  Probability             54%             │
│                                          │
│  ──────── Weekly Progress ─────────      │
│                                          │
│             📈 Chart                     │
│                                          │
└──────────────────────────────────────────┘
```

---

# 🤖 Future AI Architecture

AI functionality will be introduced incrementally.

### Phase 1

```text
User
 ↓
AI Request
 ↓
FastAPI
 ↓
LLM
 ↓
Response
```

### Phase 2

```text
User Performance
       ↓
Analytics
       ↓
Recommendation Engine
       ↓
AI
       ↓
Personalized Practice
```

### Phase 3

```text
                 ┌── LLM
                 │
User ──► AI ─────┼── RAG
                 │
                 ├── Embeddings
                 │
                 └── Question Database
```

Potential AI capabilities:

* AI tutor
* Personalized explanations
* Question generation
* Similar question generation
* Smart hints
* Adaptive difficulty
* Personalized learning plans

---

# 🛣️ Development Roadmap

## Phase 1 — Foundation

* [ ] Project repository setup
* [ ] Backend structure
* [ ] Flutter project
* [ ] React project
* [ ] SQL Server setup
* [ ] Database design
* [ ] API architecture
* [ ] Environment configuration

## Phase 2 — Authentication

* [ ] Registration
* [ ] Login
* [ ] JWT authentication
* [ ] User profile
* [ ] Authorization

## Phase 3 — Question System

* [ ] Topics
* [ ] Subtopics
* [ ] Question management
* [ ] Difficulty levels
* [ ] Question explanations
* [ ] Question import system

## Phase 4 — Practice Engine

* [ ] Practice sessions
* [ ] Answer submission
* [ ] Timer
* [ ] Scoring
* [ ] Question history
* [ ] Bookmarks
* [ ] Mistakes

## Phase 5 — Analytics

* [ ] Dashboard
* [ ] Accuracy tracking
* [ ] Topic analytics
* [ ] Difficulty analytics
* [ ] Time analysis
* [ ] Progress charts

## Phase 6 — Gamification

* [ ] Streaks
* [ ] XP
* [ ] Levels
* [ ] Achievements
* [ ] Daily goals
* [ ] Leaderboards

## Phase 7 — Personalization

* [ ] Weak-area detection
* [ ] Recommended questions
* [ ] Adaptive difficulty
* [ ] Personalized practice

## Phase 8 — AI

* [ ] AI explanations
* [ ] AI hints
* [ ] Similar question generation
* [ ] AI tutor
* [ ] Personalized study plans
* [ ] RAG / knowledge base
* [ ] Intelligent question generation

---

# 🧪 Testing

Backend testing will use **Pytest**.

Testing will cover:

* Unit tests
* Service layer tests
* Repository tests
* API endpoint tests
* Authentication tests
* Business logic tests
* Integration tests

Frontend applications will also include appropriate unit and integration testing.

---

# 🔄 Development Philosophy

AptiQuest is being developed with the following principles:

* Clean and maintainable code
* Separation of concerns
* Reusable components
* API-first architecture
* Secure development practices
* Testable business logic
* Scalable database design
* Modular feature development
* Continuous improvement

The initial implementation will use a **modular monolithic backend** rather than microservices. Individual components can be separated into independent services later if the scale and requirements justify it.

---

# 🎯 Long-Term Vision

AptiQuest aims to evolve from a simple aptitude practice application into a **personalized AI-powered learning platform**.

The long-term goal is to combine:

```text
Practice
   +
Analytics
   +
Personalization
   +
Gamification
   +
AI
   =
Intelligent Learning Platform
```

The platform can eventually expand beyond aptitude into:

* Coding practice
* Technical interview preparation
* Logical reasoning
* Verbal ability
* Placement preparation
* Interview questions
* Personalized learning paths

---

# 👨‍💻 Author

**AptiQuest**

Built as a personal learning project with the goal of developing a production-quality, scalable learning platform.

---

# 📄 License

This project is currently under development.

License information will be added when the project is ready for public distribution.
