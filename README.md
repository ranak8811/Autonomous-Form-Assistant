# Autonomous Form Assistant - AI-First CRM HCP Module

An intelligent, stateful CRM assistant designed for Healthcare Representatives to log interactions with Healthcare Professionals (HCPs) through natural conversation. Powered by **FastAPI**, **React**, **Redux**, and **LangGraph**, this application demonstrates a seamless "AI-First" architecture where a stateful agent drives the user interface.

## 🚀 Key Features

- **AI-Driven Form Automation:** Use natural language to populate complex forms instantly.
- **Surgical State Updates:** Tell the AI to change specific fields (e.g., "Change the sentiment to positive") without affecting other data.
- **LangGraph Multi-Tool Agent:** A stateful agent with 5 specialized tools:
  1. `get_hcp_list`: Fetches real-time doctor data from PostgreSQL.
  2. `get_product_list`: Retrieves available products from the database.
  3. `log_interaction`: Extracts structured entities from conversational text.
  4. `edit_interaction`: Performs precise updates on specific Redux state fields.
  5. `submit_interaction`: Finalizes and persists data to the database.
- **Real-time UI Synchronization:** Full Redux Toolkit integration ensuring the form "listens" to the AI's thoughts.
- **Granular Notifications:** Individual Toast notifications (via `react-toastify`) for every field changed by the AI.
- **Professional Split-Screen Layout:** Independent scrolling for the AI chat panel and the interaction form.

---

## 🛠️ Tech Stack

### Backend

- **Framework:** FastAPI (Python)
- **AI Orchestration:** LangGraph & LangChain
- **LLM:** NVIDIA Nemotron-3 Super (via OpenRouter API)
- **ORM:** SQLAlchemy
- **Database:** PostgreSQL
- **Validation:** Pydantic

### Frontend

- **Framework:** React (Vite)
- **State Management:** Redux Toolkit (RTK)
- **Styling:** Tailwind CSS
- **Notifications:** React-Toastify
- **API Client:** Axios

---

## 📁 Project Structure

```text
/
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI Routers (HCPs, Products, Chat)
│   │   ├── core/         # Database and Config setup
│   │   ├── models/       # SQLAlchemy Database Models
│   │   ├── schemas/      # Pydantic API Schemas
│   │   ├── services/     # LangGraph Agent & AI Tools logic
│   │   └── main.py       # Application Entry Point
│   ├── .env              # Environment Variables
│   └── requirements.txt  # Python Dependencies
├── frontend/
│   ├── src/
│   │   ├── app/          # Redux Store configuration
│   │   ├── components/   # UI Components (Form, Chat Panel)
│   │   ├── features/     # Redux Slices (Form, Chat)
│   │   ├── layout/       # Main Layout & Structure
│   │   └── services/     # API Client logic
│   └── package.json      # Node.js Dependencies

```

---

## ⚙️ Installation & Setup

### 1. Database Setup

Ensure PostgreSQL is running and create a database named `autonomous_form_assistant`.

### 2. Backend Setup

```bash
cd backend
# Create virtual environment
python3 -m venv form_env
source form_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure .env
# Create a .env file with:
# DB_USER=your_user
# DB_PASSWORD=your_pass
# DB_HOST=localhost
# DB_PORT=5432
# DB_NAME=autonomous_form_assistant
# OPENROUTER_API_KEY=your_key

# Initialize and Seed Database
python3 -m app.init_db

# Start Server
uvicorn app.main:app --reload
```

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

---

**Quick Test:**

1. Type: _"Who are the doctors?"_ (Verify Tool 1)
2. Type: _"I met Dr. Smith today for a call. Sentiment was positive."_ (Verify Tool 3 & Form Sync)
3. Type: _"Actually, it was Dr. Emily and the sentiment was neutral."_ (Verify Tool 4 - Surgical Edit)
4. Type: _"Save this interaction."_ (Verify Tool 5 - Database Persistence)

---

## 👤 Author

**Anwar Hossain**
_CSE Graduate, BRAC University_
_Software Engineer with a passion for AI-First products._

---

_This project was built as a technical assignment for [HCP Interaction Module]._

---

These are the prompts we can use whether the AI Assistant working or not:

1. Who are the doctors in our system?

2. What products do we have?

3. I had a meeting with Dr. Emily today at 2 PM. Dr. John and Nurse Joy were also there. We talked about Product Y market entry. The doctor was very
   interested, so we agreed to start a trial next month. I need to send the trial protocols by Monday. The overall vibe was positive.

4. Add Dr. Smith to the attendees.

5. Actually, remove Dr. John and only keep Dr. Smith and Dr. Emily as attendees.

6. Change the time to 9 AM.

7. This looks good, please save it.
