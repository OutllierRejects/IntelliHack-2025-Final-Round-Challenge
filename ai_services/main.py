from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.endpoints import (
    users,
    incidents,
    requests,
    tasks,
    resources,
    agents,
    websocket,
)
from core.database import init_db
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Disaster Response Coordination API",
    description="AI-powered disaster response coordination system with AGNO agents",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "https://*.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


# Include routers
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(requests.router, prefix="/api/v1", tags=["Requests"])
app.include_router(tasks.router, prefix="/api/v1", tags=["Tasks"])
app.include_router(resources.router, prefix="/api/v1", tags=["Resources"])
app.include_router(incidents.router, prefix="/api/v1", tags=["Incidents"])
app.include_router(agents.router, prefix="/api/v1", tags=["Agents"])
app.include_router(websocket.router, tags=["WebSocket"])


@app.get("/")
def root():
    return {"message": "Disaster Response Coordination API", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "disaster-response-api"}
