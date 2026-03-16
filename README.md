# 🤖 Internship Agent

> An AI-powered autonomous agent that monitors company career pages, 
> scores opportunities against your skill profile, and delivers a 
> personalized daily digest straight to your inbox — completely free.

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![GitHub Actions](https://img.shields.io/badge/Automated-GitHub%20Actions-black?style=flat-square&logo=github)
![AI](https://img.shields.io/badge/AI-Llama%203.1-orange?style=flat-square)

---

## 🎯 Problem It Solves

Every day thousands of students waste hours manually checking 
company career pages, only to find either nothing relevant or 
deadlines that have already passed.

**Internship Agent automates this entirely:**
- Monitors 10+ company career pages automatically every day
- Uses AI to score opportunities against YOUR skill profile
- Sends a ranked digest email with skill gap analysis
- Reminds you about bookmarked opportunities before deadlines

---

## ✨ Features

- 🕷️ **Smart Scraping** — Directly scrapes company career pages, 
  no middleman
- 🔍 **Change Detection** — Only triggers AI when a page actually 
  updates, saving API costs
- 🧠 **AI Scoring** — Llama 3.1 scores each opportunity 0-10 
  against your skills
- 📊 **Skill Gap Analysis** — Tells you exactly what you're missing 
  for each role
- 📧 **Beautiful Email Digest** — Ranked HTML digest delivered daily
- ⏰ **Deadline Reminders** — Bookmark opportunities and get reminded 
  automatically
- 💾 **Persistent Memory** — SQLite database tracks everything found
- ⚙️ **Fully Autonomous** — Runs daily via GitHub Actions, zero 
  manual effort
- 💰 **100% Free** — Groq API + GitHub Actions + Gmail SMTP

---

## 🏗️ Architecture
```
companies.json → Scraper → Change Detector → LLM Scorer (Groq)
                                                    ↓
                                             SQLite Database
                                                    ↓
                                          Email Digest Engine
                                                    ↓
                                          Your Inbox 📧
```

---

## 🛠️ Tech Stack

| Component | Technology | Cost |
|---|---|---|
| Language | Python 3.11+ | Free |
| Web Scraping | BeautifulSoup + Requests | Free |
| AI Scoring | Groq API (Llama 3.1) | Free |
| Database | SQLite | Free |
| Email | Gmail SMTP | Free |
| Automation | GitHub Actions | Free |
| **Total** | | **₹0/month** |

---

## 🚀 Setup Guide

### 1. Clone the repository
```bash
git clone https://github.com/adri-chak/Internship-Agent.git
cd Internship-Agent
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create `.env` file
```
GROQ_API_KEY=your_groq_api_key
GMAIL_ADDRESS=your_sending_gmail
GMAIL_APP_PASSWORD=your_16_char_app_password
RECIPIENT_EMAIL=your_receiving_email
```

### 5. Update your profile in `config.py`
```python
YOUR_NAME = "Your Name"
YOUR_EMAIL = "your@email.com"
YOUR_SKILLS = ["Python", "Machine Learning", ...]
KEYWORDS = ["internship", "intern", "fresher", ...]
```

### 6. Run the agent
```bash
python main.py
```

---

## ⚙️ Automation Setup

Fork this repository, add your secrets in:
`Settings → Secrets → Actions`

Required secrets:
- `GROQ_API_KEY`
- `GMAIL_ADDRESS`
- `GMAIL_APP_PASSWORD`
- `RECIPIENT_EMAIL`

The agent runs automatically every day at **9:00 AM IST**.

---

## 📁 Project Structure
```
internship-agent/
├── scraper/
│   └── scrape.py          # Web scraping + change detection
├── brain/
│   └── scorer.py          # LLM scoring + skill gap analysis
├── emailer/
│   └── send_email.py      # Email digest + reminder engine
├── db/
│   └── database.py        # SQLite database operations
├── data/
│   └── companies.json     # Company career page URLs
├── .github/
│   └── workflows/
│       └── run_agent.yml  # GitHub Actions automation
├── config.py              # Your profile and settings
├── main.py                # Master agent runner
└── requirements.txt       # Dependencies
```

---

## 🔮 Future Improvements

- [ ] Web dashboard to manage bookmarks
- [ ] WhatsApp/Telegram notifications
- [ ] Predictive hiring signals (funding news, headcount growth)
- [ ] Resume match scoring
- [ ] Support for 100+ companies

---

## 👩‍💻 Author

**Adrija Chakraborty**  
 Student | IEM Kolkata  
[GitHub](https://github.com/adri-chak)

---

## 📄 License

MIT License — free to use, fork, and build upon.

---

> Built with 🤖 Python, ❤️ and zero budget.