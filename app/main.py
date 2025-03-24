from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.core.logging import setup_logging
from app.api.routes import router


setup_logging()
logger = logging.getLogger(__name__)


app = FastAPI(
    title="Weather API with LLM",
    description="Provides current weather information along with a human-readable report generated using Gemini.",
    version="3.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000)