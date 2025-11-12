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

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    # Sports-related activities
    "Soccer Team": {
        "description": "Competitive soccer practices and matches",
        "schedule": "Mondays, Wednesdays, 4:00 PM - 6:00 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    "Swimming Club": {
        "description": "Lap training, technique, and swim meets",
        "schedule": "Tuesdays and Thursdays, 5:00 PM - 6:30 PM",
        "max_participants": 16,
        "participants": ["ava@mergington.edu", "isabella@mergington.edu"]
    },
    # Artistic activities
    "Drama Club": {
        "description": "Acting, stagecraft, and school productions",
        "schedule": "Tuesdays, 4:00 PM - 6:00 PM",
        "max_participants": 25,
        "participants": ["charlotte@mergington.edu", "amelia@mergington.edu"]
    },
    "Choir": {
        "description": "Vocal training, ensemble rehearsals, and performances",
        "schedule": "Wednesdays, 3:45 PM - 5:15 PM",
        "max_participants": 30,
        "participants": ["henry@mergington.edu", "ethan@mergington.edu"]
    },
    # Intellectual activities
    "Debate Team": {
        "description": "Practice formal debate, research, and tournaments",
        "schedule": "Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 18,
        "participants": ["oliver@mergington.edu", "jack@mergington.edu"]
    },
    "Math Club": {
        "description": "Problem solving, math competitions, and peer tutoring",
        "schedule": "Fridays, 2:30 PM - 4:00 PM",
        "max_participants": 20,
        "participants": ["lucas@mergington.edu", "mia@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Normalize and validate email
    if not email or not isinstance(email, str):
        raise HTTPException(status_code=400, detail="Invalid email")
    email = email.strip().lower()

    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Check if already registered (case-insensitive)
    participants = activity.get("participants", [])
    if any(p.strip().lower() == email for p in participants):
        raise HTTPException(status_code=400, detail="Student already registered for this activity")

    # Check capacity
    max_p = activity.get("max_participants")
    if isinstance(max_p, int) and len(participants) >= max_p:
        raise HTTPException(status_code=400, detail="Activity is full")

    # Add student
    activity.setdefault("participants", []).append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
