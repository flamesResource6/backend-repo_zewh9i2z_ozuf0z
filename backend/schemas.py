from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional

# Each class implies a MongoDB collection with the class name lowercased.

class Lead(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    company: Optional[str] = None
    needs: Optional[str] = None
    source: Optional[str] = None
    page: Optional[str] = None

class Developer(BaseModel):
    name: str
    stack: List[str]
    experience_years: int = Field(..., ge=0, le=40)
    rate_per_month: int = Field(..., ge=100)
    availability: str
    location: str = "India"
    tags: List[str] = []

