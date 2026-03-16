# main.py
from scraper.scrape import scrape_companies
from brain.scorer import score_all
from db.database import init_db, save_opportunities, get_bookmarked, mark_reminder_sent
from emailer.send_email import send_digest, send_reminders
from config import YOUR_NAME, TOP_N_RESULTS

def run_agent():
    print(f"\n{'='*50}")
    print(f"  Internship Agent starting for {YOUR_NAME}...")
    print(f"{'='*50}\n")

    # Step 1: Initialize database
    print("[1/5] Setting up database...")
    init_db()

    # Step 2: Scrape all company career pages
    print("\n[2/5] Scraping company career pages...")
    updated_companies = scrape_companies()

    if not updated_companies:
        print("\nNo career page updates found today.")
        print("Checking bookmarks for reminders anyway...")
    else:
        print(f"\nFound {len(updated_companies)} updated career pages!")

        # Step 3: AI scoring
        print("\n[3/5] AI analyzing opportunities...")
        scored = score_all(updated_companies)

        if scored:
            # Step 4: Save to database
            print("\n[4/5] Saving to database...")
            save_opportunities(scored)

            # Step 5: Send email digest
            print("\n[5/5] Sending email digest...")
            send_digest(scored[:TOP_N_RESULTS])
        else:
            print("\nNo relevant opportunities found in updates.")

    # Always check bookmarks and send reminders
    print("\nChecking bookmarked opportunities for reminders...")
    bookmarks = get_bookmarked()

    if bookmarks:
        print(f"Found {len(bookmarks)} bookmarked opportunities - sending reminders!")
        send_reminders(bookmarks)
        for b in bookmarks:
            mark_reminder_sent(b["id"])
    else:
        print("No pending reminders.")

    print(f"\n{'='*50}")
    print("  Agent finished! Check your inbox.")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    run_agent()