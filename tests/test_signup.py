import pytest


class TestSignup:
    """Test signup endpoint: POST /activities/{activity_name}/signup"""

    def test_successful_signup(self, client):
        """Test successful signup for a new participant"""
        email = "newstudent@mergington.edu"
        activity = "Chess Club"
        
        response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )
        
        assert response.status_code == 200
        assert email in response.json()["message"]
        
        # Verify participant was added
        activities = client.get("/activities").json()
        assert email in activities[activity]["participants"]

    def test_duplicate_signup_prevention(self, client):
        """Test that duplicate signups are prevented"""
        email = "michael@mergington.edu"  # Already signed up for Chess Club
        activity = "Chess Club"
        
        response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )
        
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_nonexistent_activity(self, client):
        """Test signup for activity that doesn't exist"""
        email = "student@mergington.edu"
        activity = "Nonexistent Activity"
        
        response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )
        
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_signup_same_student_different_activity(self, client):
        """Test that same student can signup for different activities"""
        email = "michael@mergington.edu"  # Already in Chess Club
        activity = "Programming Class"  # Different activity
        
        response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )
        
        assert response.status_code == 200
        
        # Verify added to new activity
        activities = client.get("/activities").json()
        assert email in activities[activity]["participants"]
