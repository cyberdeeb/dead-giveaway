# Dead Giveaway - AI Mystery Game API 🕵️‍♂️

A Django REST API that generates unique murder mystery cases using OpenAI's GPT-4o-mini. Players receive suspects, clues, and red herrings, then submit guesses to solve the mystery.

## 🎯 Features

- **AI-Generated Mysteries**: Each case is uniquely created using OpenAI API
- **Three Difficulty Levels**: Easy, Medium, and Hard with varying complexity
- **Smart Clue System**: Forensic, timeline, behavioral, and financial evidence
- **Red Herrings**: Misleading clues to increase challenge
- **Interactive API**: RESTful endpoints for case creation, viewing, and guess submission
- **Comprehensive Documentation**: Auto-generated OpenAPI/Swagger docs
- **Rate Limiting**: Smart throttling to manage API costs and prevent abuse

## 🛠️ Tech Stack

- **Backend**: Django 5.2.1 + Django REST Framework 3.16.1
- **AI Integration**: OpenAI API (GPT-4o-mini) with structured JSON output
- **Validation**: Pydantic 2.11.7 for data schemas
- **Documentation**: drf-spectacular for OpenAPI/Swagger
- **Database**: SQLite (development) - easily upgradeable to PostgreSQL
- **Environment**: python-dotenv for configuration management

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/cyberdeeb/dead-giveaway.git
   cd dead-giveaway
   ```

2. **Set up virtual environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   cd mystery_backend
   pip install -r requirements.txt
   ```

4. **Environment configuration**

   ```bash
   cp .env.example .env
   # Add your OpenAI API key to .env
   echo "OPENAI_API_KEY=your_api_key_here" >> .env
   echo "SECRET_KEY=your_django_secret_key" >> .env
   echo "DEBUG=True" >> .env
   ```

5. **Database setup**

   ```bash
   python manage.py migrate
   ```

6. **Run the server**
   ```bash
   python manage.py runserver
   ```

## 📖 API Documentation

Visit `http://localhost:8000/api/docs/` for interactive API documentation.

### Core Endpoints

| Method | Endpoint                 | Description                                      |
| ------ | ------------------------ | ------------------------------------------------ |
| `POST` | `/api/cases/`            | Create a new mystery case                        |
| `GET`  | `/api/cases/{id}/`       | Get case details (suspects, clues, red herrings) |
| `POST` | `/api/cases/{id}/guess/` | Submit a guess for the culprit                   |

### Example Usage

**1. Create a Mystery Case**

```bash
curl -X POST "http://localhost:8000/api/cases/?difficulty=medium" \
     -H "Content-Type: application/json"
```

**2. Get Case Details**

```bash
curl "http://localhost:8000/api/cases/1/"
```

**3. Submit a Guess**

```bash
curl -X POST "http://localhost:8000/api/cases/1/guess/" \
     -H "Content-Type: application/json" \
     -d '{"suspect_id": "S2"}'
```

## 🎮 Game Mechanics

### Difficulty Levels

- **Easy**: 3 suspects, 3 clues, 2 red herrings
- **Medium**: 4 suspects, 4 clues, 3 red herrings
- **Hard**: 5 suspects, 5 clues, 4 red herrings

### Clue Categories

- **Timeline**: When events occurred
- **Forensic**: Physical evidence
- **Behavioral**: Character actions and motivations
- **Financial**: Money-related motives

### Win Conditions

Players win by correctly identifying the culprit from the available suspects using the provided clues while avoiding red herrings.

## 🔧 Configuration

### Rate Limiting

The API includes smart throttling to manage costs and prevent abuse:

- **Case Creation**: 20/hour (uses OpenAI API)
- **Case Viewing**: 100/hour (database reads)
- **Guess Submission**: 50/hour (gameplay balance)
- **Authenticated Users**: 100/hour global limit

## 🔮 Future Enhancements

- [ ] User authentication and saved games
- [ ] Multiplayer mystery solving
- [ ] Hint system for stuck players
- [ ] Case difficulty rating based on solve rates
- [ ] Custom mystery themes (historical, sci-fi, etc.)
- [ ] Frontend React/Vue.js interface

## 📞 Contact

**Abraham** - [@cyberdeeb](https://github.com/cyberdeeb)

Project Link: [https://github.com/cyberdeeb/dead-giveaway](https://github.com/cyberdeeb/dead-giveaway)
