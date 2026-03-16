import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    STRIPE_ACCESS_SECRET_KEY = os.getenv("STRIPE_ACCESS_SECRET_KEY")
    PORT = int(os.getenv("PORT", 3000))

config = Config()
