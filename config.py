# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Your personal details
YOUR_NAME = "Adrija"
YOUR_EMAIL = "adrija.chakraborty2024@iem.edu.in"

# Your skills
YOUR_SKILLS = [
    "Python",
    "Machine Learning",
    "Data Science",
    "SQL",
    "Git"
]

# Keywords to look for
KEYWORDS = [
    "internship",
    "intern",
    "fresher",
    "entry level",
    "trainee"
]

# How many results to email
TOP_N_RESULTS = 6

# API key loaded safely from .env
GROQ_API_KEY = os.getenv("GROQ_API_KEY")