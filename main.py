from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

API_KEY = "ak_n7uc62fio82ojrkvtqbfxm6d"
EMAIL = "23f1002944@ds.study.iitm.ac.in"      # <-- Replace with your IITM login email


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Event(BaseModel):
    user: str
    amount: float
    ts: int


class RequestBody(BaseModel):
    events: List[Event]


@app.get("/")
def home():
    return {"message": "running"}


@app.post("/analytics")
def analytics(
    body: RequestBody,
    x_api_key: str = Header(None)
):

    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    total_events = len(body.events)

    unique_users = len(set(event.user for event in body.events))

    revenue = sum(event.amount for event in body.events if event.amount > 0)

    totals = {}

    for event in body.events:
        if event.amount > 0:
            totals[event.user] = totals.get(event.user, 0) + event.amount

    top_user = max(totals, key=totals.get) if totals else ""

    return {
        "email": EMAIL,
        "total_events": total_events,
        "unique_users": unique_users,
        "revenue": revenue,
        "top_user": top_user
    }