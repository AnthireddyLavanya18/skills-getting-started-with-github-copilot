"""
Tests for the activities endpoints
"""
import pytest


def test_get_activities(client):
    """Test retrieving all activities"""
    response = client.get("/activities")
    
    assert response.status_code == 200
    data = response.json()
    
    # Check that activities exist
    assert isinstance(data, dict)
    assert len(data) > 0
    
    # Verify activity structure
    for activity_name, activity_details in data.items():
        assert "description" in activity_details
        assert "schedule" in activity_details
        assert "max_participants" in activity_details
        assert "participants" in activity_details
        assert isinstance(activity_details["participants"], list)


def test_get_activities_contains_chess_club(client):
    """Test that Chess Club exists in activities"""
    response = client.get("/activities")
    data = response.json()
    
    assert "Chess Club" in data
    assert data["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"


def test_get_activities_contains_programming_class(client):
    """Test that Programming Class exists in activities"""
    response = client.get("/activities")
    data = response.json()
    
    assert "Programming Class" in data
    assert data["Programming Class"]["max_participants"] == 20


def test_root_redirect(client):
    """Test that root path redirects to static/index.html"""
    response = client.get("/", follow_redirects=False)
    
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"
