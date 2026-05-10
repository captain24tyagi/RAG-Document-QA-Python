# main.py

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from api.routes import router
from middleware.rate_limiter import limiter, rate_limit_exceeded_handler
from middleware.rate_limiter import RateLimitExceeded


load_dotenv()  

app = FastAPI(
    title="RAG Document Q&A",
    description="Basic RAG from scratch — no frameworks",
    version="1.0.0"
)


app.state.limiter = limiter

app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

# Allow the React frontend to communicate with this backend
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

@app.on_event("startup")
def validate_config():
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError(
            "OPENAI_API_KEY not found in environment. "
            "Add it to backend/.env"
        )

@app.get("/health")
def health():
    return {"status": "ok"}
