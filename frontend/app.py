from fastapi import FastAPI, Request
import json
import boto3
from datetime import datetime
import uuid

app = FastAPI()

s3 = boto3.client("s3")
BUCKET_NAME = "smart-meter-070525"
FILENAME = "data/simulated_consumption.json"

@app.post("/upload")
async def upload_data(request: Request):
    data = await request.json()
    
    # Add timestamp and unique ID
    data["recorded_at"] = datetime.utcnow().isoformat()
    data["record_id"] = str(uuid.uuid4())
    
    # Upload to S3
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=f"{FILENAME}",
        Body=json.dumps(data),
        ContentType="application/json"
    )
    
    return {"message": "Data uploaded to S3", "record_id": data["record_id"]}
