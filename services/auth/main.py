from fastapi import FastAPI, HTTPException, Request
import requests

app = FastAPI()

SUPABASE_URL = "<your-supabase-url>"
SUPABASE_ANON_KEY = "<your-supabase-key>"

@app.get("/verify")
def verify_token(request: Request):
    jwt_token = request.headers.get("Authorization")
    if not jwt_token:
        raise HTTPException(status_code=401, detail="Missing token")
    
    # Basic check (in real use, decode + verify JWT)
    headers = {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": jwt_token
    }
    response = requests.get(f"{SUPABASE_URL}/auth/v1/user", headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(status_code=403, detail="Invalid token")

    return {"message": "Token verified", "user": response.json()}
