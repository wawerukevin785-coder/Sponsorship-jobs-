import os

# ---- Skills / job categories to search for ----
SKILL_KEYWORDS = [
    "construction",
    "warehouse",
    "warehouse operative",
    "driver",
    "hgv driver",
    "truck driver",
    "electrician",
    "security guard",
    "security officer",
]

# ---- Extra keywords that must appear for a listing to count as "sponsorship" ----
SPONSORSHIP_KEYWORDS = [
    "visa sponsorship",
    "work permit",
    "relocation assistance",
    "sponsorship available",
    "lmia",
]

# ---- Countries this bot searches ----
COUNTRIES = ["canada", "germany", "netherlands", "romania"]

# ---- WhatsApp delivery (via Twilio WhatsApp API) ----
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN", "")
TWILIO_WHATSAPP_FROM = os.environ.get("TWILIO_WHATSAPP_FROM", "")
MY_WHATSAPP_NUMBER = os.environ.get("MY_WHATSAPP_NUMBER", "")

# ---- Database ----
DB_PATH = os.path.join(os.path.dirname(__file__), "data", "seen_jobs.db")
