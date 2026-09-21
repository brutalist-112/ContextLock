# 🛡️ ContextLock
**A Self-Healing Memory Firewall for AI Agents**

ContextLock prevents AI agents from storing and using dangerous or untrusted information as persistent memory. It acts like an antivirus for an AI assistant's memory — detecting poisoned inputs, quarantining threats, and healing itself automatically.

---

## 🧠 The Problem
AI agents can store information from users, documents, websites, and tools. Untrusted content may **poison** the agent's memory and silently influence future decisions across sessions — a threat called **memory poisoning**.

## 🔒 The Solution
ContextLock assigns every memory:
- A **source** (user, document, website, agent)
- A **trust score** (0–100)
- A **risk score** (0–100)
- **Allowed contexts** (where it can be used)
- **Allowed actions** (what it can influence)
- A **security status** (active / restricted / quarantined)

Dangerous memories are quarantined. If a poisoned memory influences other memories or actions, ContextLock identifies and disables the entire affected chain — **self-healing**.

---

## 📅 Weekly Progress

### ✅ Week 1 — Development Environment
**Aim:** Set up the complete development environment and create the initial project structure.

**Completed:**
- Installed Python 3.12, Visual Studio Code, Git
- Created Python virtual environment (`.venv`)
- Installed Streamlit and Pandas
- Built the initial multi-page Streamlit dashboard
- Created full project folder structure (`agent/`, `security/`, `database/`, `tools/`, `dashboard/`, `tests/`, `docs/`)
- Initialized Git repository and pushed to GitHub

**Output:** ContextLock dashboard running on `localhost:8501` with navigation and placeholder pages.

---

### ✅ Week 2 — Memory Database & Risk Scoring Engine
**Aim:** Build the core memory storage system and implement rule-based risk analysis so ContextLock can decide what to store, restrict, or quarantine.

**Completed:**
- Designed and implemented the SQLite memory database (`contextlock.db`)
- Created `database/database.py` with full CRUD operations for memories, actions, and incidents
- Built `security/risk_engine.py` with:
  - Source-based trust scoring (user = 90, document = 70, website = 30, etc.)
  - Rule-based risk detection (dangerous phrases, unknown recipients, credential keywords)
  - Decision thresholds: Safe / Restricted / Pending Approval / Quarantined
  - SHA-256 content hashing for memory integrity verification
- Connected the risk engine to the Streamlit interface
- Added **Add Memory** page with live security analysis
- Added **Memory Explorer** page to view, manage, and update all memories
- Added **Quarantine** page to review and restore blocked memories
- Dashboard now shows live memory counts (Total / Active / Quarantined / Pending)

**Output:** Users can submit information, see its trust/risk score with reasons, and watch it automatically route to active memory or quarantine.

---

## 🗓️ Upcoming Weeks
| Week | Focus |
|------|-------|
| Week 3 | Protected AI Chat (memory-based Q&A) |
| Week 4 | Memory Read Guard & context restrictions |
| Week 5 | Mock tools & Memory Relationship Graph |
| Week 6 | Self-healing recovery engine |
| Week 7 | Streamlit dashboard improvements |
| Week 8 | Security testing & evaluation |

---

## 🛠️ Tech Stack
| Technology | Purpose |
|------------|---------|
| Python 3.12 | Core language |
| Streamlit | Web interface |
| SQLite | Memory database |
| SQLAlchemy | Database ORM (upcoming) |
| NetworkX | Memory relationship graph (upcoming) |
| Plotly | Charts and visualizations (upcoming) |

---

## 🚀 Running the Project
```bash
# Clone the repo
git clone https://github.com/brutalist-112/ContextLock.git
cd ContextLock

# Create virtual environment
py -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python -m streamlit run app.py