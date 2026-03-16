# brain/scorer.py
from groq import Groq
from config import GROQ_API_KEY, YOUR_SKILLS, KEYWORDS

client = Groq(api_key=GROQ_API_KEY)

def score_company(company):
    """
    Takes a company's scraped text and asks the AI to:
    1. Find relevant internship/job opportunities
    2. Score them against your skills
    3. Identify skill gaps
    4. Extract deadlines
    """

    prompt = f"""
You are an intelligent internship opportunity analyzer.

STUDENT PROFILE:
- Skills: {', '.join(YOUR_SKILLS)}
- Looking for: {', '.join(KEYWORDS)}

CAREER PAGE CONTENT FROM {company['name']}:
{company['text']}

Analyze this career page and respond in this EXACT format:

OPPORTUNITIES_FOUND: yes or no
ROLE_TITLES: list the role names you found, comma separated
MATCH_SCORE: give a score from 0 to 10 based on how well it matches the student's skills
SKILL_GAPS: what skills does the student lack for these roles
DEADLINES: any application deadlines mentioned, or "not mentioned"
SUMMARY: write 2-3 sentences explaining why this is or isn't a good match
APPLY_URL: {company['url']}

Be concise and honest. If no relevant opportunities exist, say OPPORTUNITIES_FOUND: no
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=500
        )

        raw_response = response.choices[0].message.content
        return parse_response(raw_response, company)

    except Exception as e:
        print(f"AI error for {company['name']}: {e}")
        return None


def parse_response(raw, company):
    """
    Converts the AI's text response into a clean dictionary
    that the rest of our agent can use easily.
    """
    result = {
        "name": company["name"],
        "url": company["url"],
        "opportunities_found": False,
        "roles": "",
        "match_score": 0,
        "skill_gaps": "",
        "deadlines": "",
        "summary": "",
    }

    lines = raw.strip().split("\n")
    for line in lines:
        if "OPPORTUNITIES_FOUND:" in line:
            result["opportunities_found"] = "yes" in line.lower()
        elif "ROLE_TITLES:" in line:
            result["roles"] = line.split(":", 1)[1].strip()
        elif "MATCH_SCORE:" in line:
            try:
                score = line.split(":", 1)[1].strip()
                result["match_score"] = float(''.join(filter(lambda x: x.isdigit() or x == '.', score)))
            except:
                result["match_score"] = 0
        elif "SKILL_GAPS:" in line:
            result["skill_gaps"] = line.split(":", 1)[1].strip()
        elif "DEADLINES:" in line:
            result["deadlines"] = line.split(":", 1)[1].strip()
        elif "SUMMARY:" in line:
            result["summary"] = line.split(":", 1)[1].strip()

    return result


def score_all(updated_companies):
    """
    Runs AI scoring on all updated companies
    and returns only the ones with actual opportunities,
    sorted from best match to worst.
    """
    print("\nAI is analyzing opportunities...")
    scored = []

    for company in updated_companies:
        print(f"  Analyzing {company['name']}...")
        result = score_company(company)

        if result and result["opportunities_found"]:
            scored.append(result)
            print(f"    Match score: {result['match_score']}/10")
        else:
            print(f"    No relevant opportunities found.")

    # Sort by match score, best first
    scored.sort(key=lambda x: x["match_score"], reverse=True)
    print(f"\nFound {len(scored)} companies with relevant opportunities!")
    return scored


if __name__ == "__main__":
    # Test with one fake company to verify AI is working
    test_company = {
        "name": "Test Company",
        "url": "https://example.com",
        "text": """
        We are hiring! Open positions:
        - Machine Learning Intern (Python, TensorFlow, Data Science)
          Apply by April 30, 2025
        - Data Science Intern (SQL, Python, Statistics)
          Apply by May 15, 2025
        We are looking for freshers and students.
        """
    }

    print("Testing AI brain with sample data...\n")
    result = score_company(test_company)

    if result:
        print("AI Response:")
        for key, value in result.items():
            print(f"  {key}: {value}")