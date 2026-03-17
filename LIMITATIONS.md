# 🔧 Known Limitations & Contribution Opportunities

This document lists all known limitations of the Internship Agent.
If you're a contributor, pick any item below and raise a Pull Request!

---

## 🕷️ Scraping Limitations

### 1. HCL Tech blocked (HTTP2 Protocol Error)
- **Problem**: HCL Tech's server blocks automated browsers with HTTP2 errors
- **Current behavior**: Skipped every run
- **Suggested fix**: Try using Playwright with HTTP1.1 forced, or find alternate URL
- **File to edit**: `data/companies.json` and `scraper/scrape.py`

### 2. Samsung timing out
- **Problem**: Samsung's career page takes too long to respond
- **Current behavior**: Skipped with read timeout error
- **Suggested fix**: Increase timeout specifically for Samsung or find direct India careers URL
- **File to edit**: `scraper/scrape.py`

### 3. Change detection not job-specific
- **Problem**: Any change on a career page triggers the agent — including
  cookie banners, ads, date changes, or unrelated content updates
- **Current behavior**: False positives — agent thinks there's a new job
  when actually just an ad changed
- **Suggested fix**: Extract only the job listings section of each page
  before hashing, ignore headers/footers/ads
- **File to edit**: `scraper/scrape.py`

### 4. 3000 character text limit
- **Problem**: We only send first 3000 characters of each page to the AI
- **Current behavior**: Long pages with many jobs get cut off, AI misses
  opportunities listed further down
- **Suggested fix**: Implement smarter chunking — extract only job-related
  sections instead of raw first 3000 chars
- **File to edit**: `scraper/scrape.py`, `brain/scorer.py`

### 5. No support for login-protected portals
- **Problem**: Some company portals require account login to see listings
- **Current behavior**: Agent sees only the login page, finds nothing
- **Suggested fix**: Implement session-based login with stored credentials
  for key portals
- **File to edit**: `scraper/scrape.py`

### 6. Private API portals
- **Problem**: Some modern career pages (built in React/Angular) load jobs
  via private internal APIs that require authentication tokens
- **Current behavior**: Playwright sees empty job containers
- **Suggested fix**: Intercept network requests in Playwright to capture
  API responses directly
- **File to edit**: `scraper/scrape.py`

---

## 🧠 AI Scoring Limitations

### 7. Skills list is manually maintained
- **Problem**: User must manually update `config.py` with their skills
- **Current behavior**: If user learns a new skill, agent doesn't know
  until manually updated
- **Suggested fix**: Build a resume PDF parser that automatically extracts
  skills from uploaded resume using LLM
- **File to edit**: `config.py`, new file `brain/resume_parser.py`

### 8. Keyword matching misses synonyms
- **Problem**: If job says "graduate trainee" but keywords list only has
  "intern", the AI might miss it
- **Current behavior**: Some relevant opportunities get low scores
- **Suggested fix**: Add semantic keyword expansion — use LLM to generate
  synonyms for each keyword automatically
- **File to edit**: `brain/scorer.py`

### 9. AI response parsing is fragile
- **Problem**: If Groq API returns a slightly different format, the parser
  breaks and returns empty results
- **Current behavior**: Occasional None results from scorer
- **Suggested fix**: Use structured JSON output mode instead of text parsing
- **File to edit**: `brain/scorer.py`

### 10. Single AI model dependency
- **Problem**: Entire project depends on Groq's free tier availability
- **Current behavior**: If Groq is down, no scoring happens
- **Suggested fix**: Add fallback to Google Gemini API (also free) if
  Groq fails
- **File to edit**: `brain/scorer.py`

---

## 📧 Email Limitations

### 11. SAVE bookmark reply not implemented
- **Problem**: Email tells user to reply with "SAVE 1" but no code reads
  Gmail replies and processes bookmarks
- **Current behavior**: Bookmark feature only works manually via database
- **Suggested fix**: Use Gmail API to read replies and parse SAVE commands
  automatically
- **File to edit**: new file `emailer/reply_reader.py`

### 12. No WhatsApp or Telegram notifications
- **Problem**: Email only — some users prefer instant messaging
- **Current behavior**: Only email digest supported
- **Suggested fix**: Add Telegram Bot API integration (completely free)
- **File to edit**: new file `notifier/telegram_notify.py`

---

## ⚙️ Automation Limitations

### 13. GitHub Actions has no persistent state
- **Problem**: GitHub Actions runs on a fresh server every time —
  no memory of previous scrapes
- **Current behavior**: Every automated run thinks all companies are new,
  sends emails with all companies every day
- **Suggested fix**: Use GitHub Actions cache or commit hashes.json back
  to repo after each run to persist state
- **File to edit**: `.github/workflows/run_agent.yml`

### 14. Database resets on every GitHub Actions run
- **Problem**: `jobs.db` is not persisted between GitHub Actions runs
- **Current behavior**: Bookmarks and history are lost after each run
- **Suggested fix**: Use Supabase free tier (PostgreSQL) instead of
  local SQLite for persistent cloud storage
- **File to edit**: `db/database.py`

---

## 🖥️ Missing Features (Nice to Have)

### 15. No web dashboard
- **Problem**: No visual interface to see all opportunities, manage
  bookmarks, update skills
- **Suggested fix**: Build a simple Flask or Streamlit dashboard
- **New file**: `dashboard/app.py`

### 16. No resume match scoring
- **Problem**: Agent doesn't compare your actual resume against job
  requirements
- **Suggested fix**: Add resume PDF upload and ATS-style scoring
- **New file**: `brain/resume_matcher.py`

### 17. No predictive hiring signals
- **Problem**: Agent only reacts to posted jobs, doesn't predict
  upcoming hiring
- **Suggested fix**: Monitor company news, funding announcements,
  LinkedIn headcount growth as early signals
- **New file**: `signals/predictor.py`

### 18. Companies list is manually maintained
- **Problem**: User must manually find and add career page URLs
- **Suggested fix**: Build a company discovery module that automatically
  finds career pages given just a company name
- **New file**: `data/company_finder.py`

### 19. No mobile app
- **Problem**: No way to manage bookmarks or view opportunities on phone
- **Suggested fix**: Simple PWA (Progressive Web App) frontend
- **New folder**: `frontend/`

### 20. No duplicate detection across runs
- **Problem**: Same job posted on company site AND Naukri AND LinkedIn
  appears as three separate opportunities
- **Suggested fix**: Use semantic similarity to detect and merge duplicate
  listings across sources
- **File to edit**: `db/database.py`

---

## 🤝 How to Contribute

1. Fork this repository
2. Pick any limitation above
3. Create a new branch: `git checkout -b fix/limitation-name`
4. Fix it and test it
5. Raise a Pull Request with clear description of what you fixed

### Setup for contributors:
```bash
git clone https://github.com/adri-chak/Internship-Agent.git
cd Internship-Agent
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
playwright install chromium
```

Create your own `.env` file:
```
GROQ_API_KEY=your_groq_key
GMAIL_ADDRESS=your_gmail
GMAIL_APP_PASSWORD=your_app_password
RECIPIENT_EMAIL=your_email
```

Then run:
```bash
python main.py
```

---

*Last updated: March 2026*
*Maintained by: Adrija Chakraborty — adri-chak*