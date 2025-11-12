from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from database import get_db, create_document, get_documents
from schemas import Lead, Developer

app = FastAPI(title="Quenlix API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Quenlix API running"}


@app.get("/test")
async def test_db():
    try:
        db = await get_db()
        collections = await db.list_collection_names()
        return {
            "backend": "fastapi",
            "database": "mongodb",
            "database_url": "hidden",
            "database_name": db.name,
            "connection_status": "ok",
            "collections": collections,
        }
    except Exception as e:
        return {"backend": "fastapi", "database": "mongodb", "connection_status": f"error: {e}"}


# Leads
@app.post("/leads")
async def create_lead(lead: Lead):
    lead_id = await create_document("lead", lead.model_dump())
    return {"id": lead_id, "status": "received"}


# Developers sample list (could be seeded or dynamic). For now, allow reading from DB; if empty, return placeholders.
SAMPLE_DEVS = [
    Developer(name="Aarav Shah", stack=["React", "Node", "TypeScript"], experience_years=3, rate_per_month=1200, availability="Immediate", tags=["startup-ready", "web"], location="India"),
    Developer(name="Neha Gupta", stack=["Solidity", "Next.js", "Ethers.js"], experience_years=4, rate_per_month=1800, availability="2 weeks", tags=["Web3", "smart contracts"], location="India"),
    Developer(name="Rohit Verma", stack=["Flutter", "Firebase", "Dart"], experience_years=5, rate_per_month=1500, availability="Immediate", tags=["mobile", "MVP"], location="India"),
    Developer(name="Sara Iyer", stack=["Python", "FastAPI", "LLMs"], experience_years=6, rate_per_month=2200, availability="1 month", tags=["AI", "backend"], location="India"),
]


@app.get("/developers", response_model=List[Developer])
async def list_developers():
    docs = await get_documents("developer", {}, limit=20)
    if docs:
        # map to Developer
        return [Developer(**{**d, "rate_per_month": int(d.get("rate_per_month", 0))}) for d in docs]
    return SAMPLE_DEVS


class ContactForm(BaseModel):
    name: str
    email: str
    company: str | None = None
    needs: str | None = None
    page: str | None = None


@app.post("/contact")
async def submit_contact(payload: ContactForm):
    _id = await create_document("lead", payload.model_dump())
    return {"status": "ok", "id": _id}
