import os
import tempfile
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine
from src.app import app
from src.db import engine

client = TestClient(app)


def test_get_activities_returns_seeded_entries():
    r = client.get("/activities")
    assert r.status_code == 200
    data = r.json()
    assert "Chess Club" in data


def test_signup_and_unregister():
    email = "teststudent@example.com"
    r = client.post("/activities/Chess Club/signup", params={"email": email})
    assert r.status_code == 200
    r2 = client.get("/activities")
    assert email in r2.json()["Chess Club"]["participants"]

    r3 = client.delete("/activities/Chess Club/unregister", params={"email": email})
    assert r3.status_code == 200
    r4 = client.get("/activities")
    assert email not in r4.json()["Chess Club"]["participants"]
