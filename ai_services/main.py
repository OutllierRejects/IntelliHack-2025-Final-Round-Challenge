from fastapi import FastAPI
from api.endpoints import users, incidents

app = FastAPI()

app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(incidents.router, prefix="/api", tags=["Incidents"])

