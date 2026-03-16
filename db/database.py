# db/database.py
import sqlite3
import os

DB_PATH = "db/jobs.db"

def init_db():
    """
    Creates the database and tables if they don't exist yet.
    Run this once at the start of every agent session.
    """
    os.makedirs("db", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS opportunities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            roles TEXT,
            match_score REAL,
            skill_gaps TEXT,
            deadlines TEXT,
            summary TEXT,
            url TEXT,
            bookmarked INTEGER DEFAULT 0,
            reminder_sent INTEGER DEFAULT 0,
            date_found TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
    print("Database ready!")


def save_opportunities(scored_companies):
    """
    Saves all newly found opportunities to the database.
    Skips duplicates - won't save the same company twice.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    saved = 0
    for company in scored_companies:
        # Check if this company's opportunity already exists
        cursor.execute(
            "SELECT id FROM opportunities WHERE company = ? AND roles = ?",
            (company["name"], company["roles"])
        )
        exists = cursor.fetchone()

        if not exists:
            cursor.execute("""
                INSERT INTO opportunities 
                (company, roles, match_score, skill_gaps, deadlines, summary, url)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                company["name"],
                company["roles"],
                company["match_score"],
                company["skill_gaps"],
                company["deadlines"],
                company["summary"],
                company["url"]
            ))
            saved += 1

    conn.commit()
    conn.close()
    print(f"Saved {saved} new opportunities to database!")


def bookmark_opportunity(opportunity_id):
    """
    Marks an opportunity as bookmarked.
    Agent will send reminders for bookmarked opportunities.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE opportunities SET bookmarked = 1 WHERE id = ?",
        (opportunity_id,)
    )

    conn.commit()
    conn.close()
    print(f"Opportunity {opportunity_id} bookmarked!")


def get_bookmarked():
    """
    Returns all bookmarked opportunities that
    haven't had a reminder sent yet.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, company, roles, deadlines, url 
        FROM opportunities 
        WHERE bookmarked = 1 AND reminder_sent = 0
    """)

    rows = cursor.fetchall()
    conn.close()

    # Convert to list of dictionaries for easy use
    bookmarks = []
    for row in rows:
        bookmarks.append({
            "id": row[0],
            "company": row[1],
            "roles": row[2],
            "deadlines": row[3],
            "url": row[4]
        })

    return bookmarks


def mark_reminder_sent(opportunity_id):
    """
    After sending a reminder, marks it so
    we don't send the same reminder again.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE opportunities SET reminder_sent = 1 WHERE id = ?",
        (opportunity_id,)
    )

    conn.commit()
    conn.close()


def get_all_opportunities():
    """
    Returns all opportunities ever found, newest first.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, company, roles, match_score, deadlines, bookmarked, date_found 
        FROM opportunities 
        ORDER BY match_score DESC, date_found DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    opportunities = []
    for row in rows:
        opportunities.append({
            "id": row[0],
            "company": row[1],
            "roles": row[2],
            "match_score": row[3],
            "deadlines": row[4],
            "bookmarked": row[5],
            "date_found": row[6]
        })

    return opportunities


if __name__ == "__main__":
    # Test the database
    print("Setting up database...")
    init_db()

    # Insert a fake opportunity to test
    test_data = [{
        "name": "Google",
        "roles": "Machine Learning Intern",
        "match_score": 9.0,
        "skill_gaps": "TensorFlow",
        "deadlines": "April 30, 2025",
        "summary": "Great match for your profile!",
        "url": "https://careers.google.com"
    }]

    save_opportunities(test_data)

    # Bookmark it
    bookmark_opportunity(1)

    # Fetch bookmarked
    bookmarks = get_bookmarked()
    print(f"\nBookmarked opportunities: {len(bookmarks)}")
    for b in bookmarks:
        print(f"  - {b['company']}: {b['roles']} | Deadline: {b['deadlines']}")

    # Fetch all
    all_ops = get_all_opportunities()
    print(f"\nAll opportunities in database: {len(all_ops)}")
    for op in all_ops:
        print(f"  [{op['id']}] {op['company']} - {op['roles']} | Score: {op['match_score']} | Bookmarked: {bool(op['bookmarked'])}")