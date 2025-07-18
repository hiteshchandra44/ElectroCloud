import json
import boto3
from datetime import datetime
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')
BUCKET_NAME = "smart-meter-070525"
ANALYTICS_CSV_KEY = "analytics/summary.csv"  # Update this if your CSV path changes

def lambda_handler(event, context):
    try:
        # Parse and validate input
        body = event.get('body')
        if isinstance(body, str):
            body = json.loads(body)
        if not isinstance(body, dict):
            raise ValueError("Invalid 'body' in event")

        meter_id = body.get('meter_id')
        timestamp = body.get('timestamp')
        if not meter_id or not timestamp:
            raise ValueError("Missing required fields: meter_id or timestamp")

        # Convert timestamp and extract time parts for S3 partitioning
        dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))  # Handle UTC 'Z'
        partition_path = f"year={dt.year}/month={dt.month:02d}/day={dt.day:02d}/hour={dt.hour:02d}"
        filename = f"{dt.strftime('%Y%m%d_%H%M%S')}_{meter_id}.json"
        key = f"meter_readings/{partition_path}/{filename}"

        # Flatten the nested input structure
        flat_record = {
            "meter_id": meter_id,
            "timestamp": timestamp,
            "current_value": body['reading']['current_value'],
            "instant_usage": body['reading']['instant_usage'],
            "unit": body['reading']['unit'],
            "voltage": body['power_quality']['voltage'],
            "frequency": body['power_quality']['frequency'],
            "power_factor": body['power_quality']['power_factor'],
            "battery_level": body['status']['battery_level'],
            "signal_strength": body['status']['signal_strength'],
            "error_flags": body['status']['error_flags']
        }
        logger.info(f"Flattened record: {flat_record}")
        # Write the flat JSON record to S3
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=key,
            Body=json.dumps(flat_record),
            ContentType='application/json'
        )
        logger.info(f"Stored reading: s3://{BUCKET_NAME}/{key}")

        # Try to read the analytics CSV file from S3
        try:
            response = s3.get_object(Bucket=BUCKET_NAME, Key=ANALYTICS_CSV_KEY)
            analytics_data = response['Body'].read().decode('utf-8')
        except Exception as e:
            logger.warning(f"Could not retrieve analytics CSV: {e}")
            analytics_data = None

        # Build the response object
        response_body = {
            'message': 'Reading stored successfully',
            'location': f"s3://{BUCKET_NAME}/{key}"
        }

        if analytics_data:
            response_body['analytics_csv'] = analytics_data  # You can also parse CSV to JSON here if needed

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps(response_body)
        }

    except Exception as e:
        logger.error(f"Error: {e}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }
