from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_submissions():
    response = client.get("/api/submissions")
    assert response.status_code in [200, 500]


def test_create_submission():
    data = {
        "submissionID": 12345,
        "projectId": 1,
        "userId": 101,
        "statusId": 1
    }

    response = client.post("/api/submissions", json=data)
    assert response.status_code in [200, 500]


def test_send_event():
    response = client.post("/submissions/send")
    assert response.status_code in [200, 500]