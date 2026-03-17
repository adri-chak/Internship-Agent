# scraper/scrape.py
import requests
from bs4 import BeautifulSoup
import hashlib
import json
import os
from playwright.sync_api import sync_playwright

# These sites are known to be dynamic (JS-rendered)
# Playwright will be used for these automatically
DYNAMIC_SITES = [
    "google", "microsoft", "amazon", "linkedin",
    "jpmorgan", "goldmansachs", "accenture", "cisco",
    "walmart", "netflix", "sap", "bosch", "celonis",
    "dynatrace", "cognizant", "capgemini", "deloitte",
    "techmahindra", "hcltech", "ltimindtree"
]


def is_dynamic(url):
    """Check if a URL belongs to a known dynamic site."""
    url_lower = url.lower()
    return any(site in url_lower for site in DYNAMIC_SITES)


def get_page_text_static(url):
    """
    For static websites — fast and lightweight.
    Uses requests + BeautifulSoup.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)
        return text

    except Exception as e:
        print(f"    Static fetch error: {e}")
        return ""


def get_page_text_dynamic(url):
    """
    For dynamic/JS-rendered websites — uses real browser.
    Playwright actually runs JavaScript like a real user.
    """
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # Set a real browser identity
            page.set_extra_http_headers({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            })

            # Go to page and wait for content to load
            page.goto(url, timeout=30000)

            # Wait for page to fully render
            page.wait_for_load_state("domcontentloaded", timeout=30000)

            # Get all visible text
            text = page.inner_text("body")
            browser.close()
            return text

    except Exception as e:
        print(f"    Dynamic fetch error: {e}")
        return ""


def get_page_text(url):
    """
    Smart router — automatically picks static or dynamic
    scraping based on the URL.
    """
    if is_dynamic(url):
        print(f"    (using browser for JS-rendered page)")
        return get_page_text_dynamic(url)
    else:
        return get_page_text_static(url)


def hash_text(text):
    """Fingerprints page text for change detection."""
    return hashlib.md5(text.encode()).hexdigest()


def load_seen_hashes():
    """Loads previously saved fingerprints."""
    if os.path.exists("data/hashes.json"):
        with open("data/hashes.json") as f:
            return json.load(f)
    return {}


def save_seen_hashes(hashes):
    """Saves current fingerprints for next time."""
    with open("data/hashes.json", "w") as f:
        json.dump(hashes, f, indent=2)


def scrape_companies():
    """
    Main scraping function.
    Automatically uses browser for dynamic sites,
    lightweight requests for static sites.
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
                "text": text[:3000]
            })
            seen_hashes[name] = current_hash
        else:
            print(f"  No changes at {name}.")

    save_seen_hashes(seen_hashes)
    print(f"\nDone! Found {len(updated_companies)} updated companies.")
    return updated_companies


if __name__ == "__main__":
    results = scrape_companies()