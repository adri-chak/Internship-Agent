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
    "Web Development",
    "Artificial Intelligence",
    "Machine Learning",
    "C Programming",
    "Java",
    "Object Oriented Programming",
    "Data Structures and Algorithms",
    "SQL",
    "Git",
    "Github",
    "Web Scraping",
    "REST APIs",
    "Prompt Engineering",
    "HTML",
    "CSS",
    "Problem Solving",
    "Project Management",
    "Data Science",
    "Data Analytics",
    "Data Visualization",
    "Frontend",
    "UI/UX"
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
GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")