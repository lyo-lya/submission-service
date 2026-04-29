from fastapi import FastAPI
from sqlalchemy import text
from db import engine
from datetime import datetime
from service_bus_sender import send_message

app = FastAPI(title="Submission Service")

SCHEMA = "Volha_Platnitskaya_submission"
TABLE = f"{SCHEMA}.Submission"
STATUS_TABLE = f"{SCHEMA}.SubmissionStatus"

@app.get("/submissions")
def get_submissions():
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM Volha_Platnitskaya_submission.Submission")
        )
        return [dict(row._mapping) for row in result]


@app.get("/api/submissions/{id}")
def get_submission(id: int):
    query = text(f"""
        SELECT * FROM {TABLE}
        WHERE submissionID = :id
    """)

    with engine.connect() as conn:
        result = conn.execute(query, {"id": id}).fetchone()

    return dict(result._mapping) if result else {"error": "Not found"}

@app.post("/api/submissions")
def create_submission(submission: dict):
    """
    Expected JSON:
    {
        "submissionID": 1,
        "projectId": 1,
        "userId": 101,
        "statusId": 1
    }
    """

    query = text(f"""
        INSERT INTO {TABLE} (submissionID, projectId, userId, statusId, createdAt)
        VALUES (:submissionID, :projectId, :userId, :statusId, GETDATE())
    """)

    with engine.connect() as conn:
        conn.execute(query, submission)
        conn.commit()

    return {"message": "Submission created"}

@app.get("/api/submissions")
def get_submissions(status: int = None):

    base_query = f"SELECT * FROM {TABLE}"
    params = {}

    if status is not None:
        base_query += " WHERE statusId = :status"
        params["status"] = status

    with engine.connect() as conn:
        result = conn.execute(text(base_query), params)
        return [dict(row._mapping) for row in result]

@app.patch("/api/submissions/{id}/status")
def update_status(id: int, body: dict):
    """
    Expected JSON:
    {
        "statusId": 2
    }
    """

    query = text(f"""
        UPDATE {TABLE}
        SET statusId = :statusId
        WHERE submissionID = :id
    """)

    with engine.connect() as conn:
        conn.execute(query, {"id": id, "statusId": body["statusId"]})
        conn.commit()

    return {"message": "Status updated"}

@app.post("/submissions/send")
def send_submission_event():
    event = {
        "submissionId": 1,
        "projectId": 1,
        "userId": 101,
        "status": "Pending",
        "eventType": "SubmissionCreated",
        "issueDateTimeUTC": datetime.utcnow().isoformat()
    }

    send_message(event)

    return {"message": "Event sent to queue"}