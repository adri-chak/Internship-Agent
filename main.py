# This is the master file - it runs our entire agent

from config import YOUR_NAME, YOUR_SKILLS, KEYWORDS, TOP_N_RESULTS

def greet():
    print(f"Hello {YOUR_NAME}! Your agent is starting up...")
    print(f"Looking for: {KEYWORDS}")
    print(f"Your skills: {YOUR_SKILLS}")
    print(f"Will send top {TOP_N_RESULTS} results")

if __name__ == "__main__":
    greet()