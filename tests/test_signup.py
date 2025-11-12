"""
Tests for signup functionality
"""
import pytest


def test_signup_new_participant(client, reset_activities):
    """Test signing up a new participant for an activity"""
    response = client.post(
        "/activities/Chess%20Club/signup?email=newstudent@mergington.edu",
        follow_redirects=True
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "Signed up" in data["message"]


def test_signup_and_participant_appears(client, reset_activities):
    """Test that newly signed up participant appears in activities list"""
    email = "newstudent@mergington.edu"
    
    # Sign up for an activity
    response = client.post(
        f"/activities/Chess%20Club/signup?email={email}",
        follow_redirects=True
    )
    assert response.status_code == 200
    
    # Fetch activities and verify participant was added
    response = client.get("/activities")
    data = response.json()
    
    assert email in data["Chess Club"]["participants"]


def test_signup_duplicate_email(client, reset_activities):
    """Test that duplicate signup is rejected"""
    email = "michael@mergington.edu"  # Already registered in Chess Club
    
    response = client.post(
        f"/activities/Chess%20Club/signup?email={email}",
        follow_redirects=True
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "already registered" in data["detail"]


def test_signup_nonexistent_activity(client, reset_activities):
    """Test signup for non-existent activity"""
    response = client.post(
        "/activities/Fake%20Activity/signup?email=student@mergington.edu",
        follow_redirects=True
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_signup_with_invalid_email(client, reset_activities):
    """Test signup with invalid email"""
    response = client.post(
        "/activities/Chess%20Club/signup?email=",
        follow_redirects=True
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "Invalid email" in data["detail"]


def test_signup_case_insensitive_email(client, reset_activities):
    """Test that email comparison is case-insensitive"""
    email_lowercase = "testuser@mergington.edu"
    email_uppercase = "TESTUSER@MERGINGTON.EDU"
    
    # First signup with lowercase
    response = client.post(
        f"/activities/Chess%20Club/signup?email={email_lowercase}",
        follow_redirects=True
    )
    assert response.status_code == 200
    
    # Second signup with uppercase should fail
    response = client.post(
        f"/activities/Chess%20Club/signup?email={email_uppercase}",
        follow_redirects=True
    )
    assert response.status_code == 400
    data = response.json()
    assert "already registered" in data["detail"]


def test_signup_activity_at_capacity(client, reset_activities):
    """Test signup fails when activity is at capacity"""
    from src.app import activities
    
    # Create a test activity with max_participants = 1 and one participant
    test_activity_name = "TestCapacityActivity"
    activities[test_activity_name] = {
        "description": "Test activity",
        "schedule": "Test time",
        "max_participants": 1,
        "participants": ["existing@mergington.edu"]
    }
    
    # Try to add another participant (should fail)
    response = client.post(
        f"/activities/{test_activity_name}/signup?email=new@mergington.edu",
        follow_redirects=True
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "Activity is full" in data["detail"]


def test_multiple_signups_same_email_different_activities(client, reset_activities):
    """Test that same email can signup for different activities"""
    email = "multisport@mergington.edu"
    
    # Sign up for Chess Club
    response1 = client.post(
        f"/activities/Chess%20Club/signup?email={email}",
        follow_redirects=True
    )
    assert response1.status_code == 200
    
    # Sign up for Programming Class
    response2 = client.post(
        f"/activities/Programming%20Class/signup?email={email}",
        follow_redirects=True
    )
    assert response2.status_code == 200
    
    # Verify both signups
    response = client.get("/activities")
    data = response.json()
    
    assert email in data["Chess Club"]["participants"]
    assert email in data["Programming Class"]["participants"]
