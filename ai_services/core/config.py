# core/config.py
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()  # Load from .env file if present

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
JWT_SECRET = os.getenv("JWT_SECRET", "super-secret")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
