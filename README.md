# 🍔 AI Food Ordering Agent

> Built from scratch — one arc at a time.

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Streamlit-FF4B4B?style=for-the-badge)](https://ai-food-ordering-agent-j4fsccrafjyscp2h7cvkp9.streamlit.app/)
[![API](https://img.shields.io/badge/⚡_Live_API-Render-46E3B7?style=for-the-badge)](https://food-agent-c2az.onrender.com/docs)
[![GitHub](https://img.shields.io/badge/📂_GitHub-Repository-181717?style=for-the-badge&logo=github)](https://github.com/YendetiYashashwini/ai-food-ordering-agent)

---

## 🧠 What is this?

A plain LLM can talk about food. It cannot order it.

This project fixes that — by building an AI Food Ordering Agent from scratch that actually searches meals, filters by protein and budget, and places real orders.

Built arc by arc, documented every step.

---

## ✨ Live Demo

🔗 **Try it here → [food-agent.streamlit.app](https://ai-food-ordering-agent-j4fsccrafjyscp2h7cvkp9.streamlit.app/)**

```
"Find me a high protein meal under ₹300 and order it"
```

---

## 🗂️ Project Structure — 7 Arcs

| Arc | What it does |
|-----|-------------|
| 🧠 **Arc 1** — Brain in a Jar | Plain LLM demo — smart but no actions |
| 💊 **Arc 2** — Amnesia Fix | Message history → LLM now remembers |
| 🛠️ **Arc 3** — Agent with Tools | LLM gets tools → actually orders food |
| ⚡ **Arc 4** — FastAPI Backend | Agent becomes an HTTP server |
| 💬 **Arc 5** — Streamlit UI | Chat interface in the browser |
| 🔌 **Arc 6** — MCP Integration | Claude Desktop can use our tools directly |
| 🐳 **Arc 7** — Docker + Deploy | Containerized and deployed on Render |

---

## 🚀 How it works

```
User types a message
    ↓
Streamlit UI (Arc 5)
    ↓
FastAPI Backend (Arc 4) — deployed on Render
    ↓
LLM (Groq — Llama 3.3 70B)
    ↓
Tools: search_meals() / place_order()
    ↓
Response back to user
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| LLM | Llama 3.3 70B via Groq |
| Backend | FastAPI + Uvicorn |
| Frontend | Streamlit |
| MCP | FastMCP |
| Containerization | Docker |
| Deployment | Render (API) + Streamlit Cloud (UI) |
| Language | Python 3.11 |

---

## 🍽️ What the agent can do

- 🔍 Search meals by cuisine, protein, price, diet
- 🏆 Recommend best value meal (highest protein per rupee)
- ✅ Place orders with confirmation
- 💬 Hold full conversations with memory
- 🔌 Work directly inside Claude Desktop via MCP

---

## 📁 Folder Structure

```
ai-food-ordering-agent/
├── arc1/          # Brain in a Jar demo
├── arc2/          # Amnesia problem + fix
├── arc3/          # Agent with tools (data.py, tools.py, agent.py)
├── arc4/          # FastAPI backend
├── arc5/          # Streamlit frontend
├── arc6/          # MCP server (FastMCP)
├── arc7/          # Docker + deployment files
└── .gitignore
```

---

## ⚡ Quick Start (Local)

```bash
# Clone the repo
git clone https://github.com/YendetiYashashwini/ai-food-ordering-agent.git
cd ai-food-ordering-agent

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install openai fastapi uvicorn streamlit httpx python-dotenv fastmcp pydantic

# Add your API key
echo "OPENROUTER_API_KEY=your_groq_key_here" > .env

# Run the agent (terminal)
python arc3/agent.py

# OR run the full stack
# Terminal 1:
uvicorn arc4.arc4:app --reload
# Terminal 2:
streamlit run arc5/arc5.py
```

---

## 🔌 MCP Integration (Claude Desktop)

Add this to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "food-agent": {
      "command": "python",
      "args": ["path/to/arc6/arc6.py"]
    }
  }
}
```

Now Claude Desktop can search meals and place orders directly.

---

## 🌱 Built as part of

📅 **100 Days DSA + AI/ML Journey** — Margam Academy

Mentors: **Nikith Sir**

---

## 👩‍💻 Author

**Yashashwini Yendeti** — 3rd Year CSE (AI & ML), VVITU

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat&logo=linkedin)](https://www.linkedin.com/in/yashashwini-yendeti)

---

> *"Everyone posts their AI Agent after it works. I built mine arc by arc and documented everything."*
