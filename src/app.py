"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

from typing import List
from sqlmodel import select

# Initialize DB on startup
from .db import init_db, get_session, engine
from .models import Activity, Participant

init_db()

# Seed initial activities if DB is empty
from sqlmodel import Session

with Session(engine) as session:
    count = session.exec(select(Activity)).first()
    if count is None:
        seed_activities = [
            Activity(name="Chess Club", description="Learn strategies and compete in chess tournaments", schedule="Fridays, 3:30 PM - 5:00 PM", max_participants=12),
            Activity(name="Programming Class", description="Learn programming fundamentals and build software projects", schedule="Tuesdays and Thursdays, 3:30 PM - 4:30 PM", max_participants=20),
            Activity(name="Gym Class", description="Physical education and sports activities", schedule="Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM", max_participants=30),
        ]
        session.add_all(seed_activities)
        session.commit()


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    with get_session() as session:
        activities = session.exec(select(Activity)).all()
        result = {}
        for a in activities:
            participants = session.exec(select(Participant).where(Participant.activity_id == a.id)).all()
            result[a.name] = {
                "description": a.description,
                "schedule": a.schedule,
                "max_participants": a.max_participants,
                "participants": [p.email for p in participants]
            }
        return result


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    with get_session() as session:
        activity = session.exec(select(Activity).where(Activity.name == activity_name)).first()
        if not activity:
            raise HTTPException(status_code=404, detail="Activity not found")

        participants = session.exec(select(Participant).where(Participant.activity_id == activity.id)).all()

        if any(p.email == email for p in participants):
            raise HTTPException(status_code=400, detail="Student is already signed up")

        if len(participants) >= activity.max_participants:
            raise HTTPException(status_code=400, detail="Activity is full")

        new_p = Participant(email=email, activity_id=activity.id)
        session.add(new_p)
        session.commit()
        return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""
    with get_session() as session:
        activity = session.exec(select(Activity).where(Activity.name == activity_name)).first()
        if not activity:
            raise HTTPException(status_code=404, detail="Activity not found")

        participant = session.exec(select(Participant).where(Participant.activity_id == activity.id, Participant.email == email)).first()
        if not participant:
            raise HTTPException(status_code=400, detail="Student is not signed up for this activity")

        session.delete(participant)
        session.commit()
        return {"message": f"Unregistered {email} from {activity_name}"}
