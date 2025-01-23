# ElectroCloud
Project Steps:
Set up AWS S3 Bucket:

Created an S3 bucket to store data files.
Organized the data into the data/ folder for uploading raw files.
Lambda Function Development:

Developed an AWS Lambda function to process data.
Configured the Lambda function to process incoming files from the S3 bucket.
Set up the function to write processed data into the processed-data/ folder in the S3 bucket.
API Gateway Configuration:

Created an API Gateway to serve as an interface for external devices to send data.
Configured the API Gateway to trigger the Lambda function on data upload or API calls.
Implemented Data Processing Logic in Lambda:

The Lambda function formats and cleans incoming data (e.g., parsing JSON, formatting timestamps, validating fields).
Processed data is stored back into S3 for further use.
Real-Time Data Fetching:

Added a Python script to fetch real-time data from smart meters.
Script sends readings to the API Gateway for further processing by the Lambda function.
EC2 Instance Setup (Pending Approval for Resources):

Planned to use an EC2 instance for further machine learning model development.
Encountered resource limits and awaiting approval to proceed.
