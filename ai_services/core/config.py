# core/config.py
import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env file if present

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./disaster_response.db")
DATABASE_ECHO = os.getenv("DATABASE_ECHO", "false").lower() == "true"

# Supabase Configuration (Optional)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

# JWT Configuration
JWT_SECRET = os.getenv("JWT_SECRET", "disaster-response-super-secret-jwt-key-2025")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# Redis Configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
