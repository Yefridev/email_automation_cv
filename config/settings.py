from dotenv import load_dotenv
import os

load_dotenv()

GMAIL_USER = os.getenv("GMAIL_USER")
CHECK_INTERVAL_MINUTES = int(os.getenv("CHECK_INTERVAL_MINUTES",30))
MAX_EMAILS_PER_RUN = int(os.getenv("MAX_EMAILS_PER_RUN", 20))
CV_PATH = os.getenv("CV_PATH", "docs/CV_Yefri_Arisa.pdf")
MIN_PRIORITY_TO_REPLY = os.getenv("MIN_PRIORITY_TO_REPLY", "alta")