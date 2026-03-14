# scraper/scrape.py
import requests
from bs4 import BeautifulSoup
import hashlib
import json
import os

def get_page_text(url):
    """
    Opens a URL and returns all the visible text on that page.
    Like reading a webpage but as plain text.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Remove script and style tags - we dont need them
        for tag in soup(["script", "style"]):
            tag.decompose()
        
        text = soup.get_text(separator=" ", strip=True)
        return text
    
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""


def hash_text(text):
    """
    Converts any text into a short unique fingerprint.
    If the page changes, the fingerprint changes.
    This is how we detect updates without reading everything twice.
    """
    return hashlib.md5(text.encode()).hexdigest()


def load_seen_hashes():
    """
    Loads previously saved page fingerprints from memory.
    So we know what pages looked like last time.
    """
    if os.path.exists("data/hashes.json"):
        with open("data/hashes.json") as f:
            return json.load(f)
    return {}


def save_seen_hashes(hashes):
    """
    Saves current page fingerprints for next time.
    """
    with open("data/hashes.json", "w") as f:
        json.dump(hashes, f, indent=2)


def scrape_companies():
    """
    Main function - goes through every company,
    checks if their career page changed,
    returns only the ones that are new or updated.
    """
    with open("data/companies.json") as f:
        companies = json.load(f)
    
    seen_hashes = load_seen_hashes()
    updated_companies = []

    for company in companies:
        name = company["name"]
        url = company["careers_url"]
        
        print(f"Checking {name}...")
        text = get_page_text(url)
        
        if not text:
            print(f"  Could not read {name}, skipping.")
            continue
        
        current_hash = hash_text(text)
        previous_hash = seen_hashes.get(name)

        if current_hash != previous_hash:
            print(f"  NEW or UPDATED content found at {name}!")
            updated_companies.append({
                "name": name,
                "url": url,
                "text": text[:3000]  # first 3000 chars is enough for AI to read
            })
            seen_hashes[name] = current_hash
        else:
            print(f"  No changes at {name}.")
    
    save_seen_hashes(seen_hashes)
    print(f"\nDone! Found {len(updated_companies)} updated companies.")
    return updated_companies


if __name__ == "__main__":
    results = scrape_companies()