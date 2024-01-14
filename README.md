# Data Ingestion Pipeline using AWS services
## Overview
This project outlines the data ingestion pipeline used to process customer and invoice data and i used various AWS services for the seamless ingestion. The pipeline integrates with services such as Amazon API Gateway, AWS Lambda, Amazon Kinesis, and Amazon DynamoDB to ingest, process, and store data effectively.

## Architecture
<img width="601" alt="Screenshot 2024-01-14 214117" src="https://github.com/LogicAL007/AWS-data-pipeline/assets/122959675/29150d37-7e9f-40d4-9529-ddb1f05d2998">

The pipeline consists of the following steps:
1. **Input Client**: Sends JSON data to an API Gateway.

2. **API Gateway**: Acts as an entry point for the client data and forwards it to AWS Lambda.
3. **AWS Lambda**: Processes incoming POST requests and places the data into Amazon Kinesis Data Stream.
4. **Kinesis Data Stream**: Buffers the data before it is processed by another Lambda function.
5. **S3 Bucket**: Stores processed records as .txt files with timestamps for data durability and retrieval.
6. **DynamoDB**: Stores customer and invoice views for fast access and querying.


## Components
1. **Input Client:** A script to read customer data from a CSV and send it to an API endpoint in JSON format.

2. **API Gateway:** An AWS service that allows for the creation, publication, maintenance, monitoring, and securing of REST and WebSocket APIs at scale.

3. **Lambda (Data Preprocessing):** AWS Lambda functions are used for running code in response to triggers such as changes in data or system state.

4. **Amazon Kinesis Data Firehose:** Captures and loads streaming data in real time to AWS destinations such as S3 and DynamoDB.

5. **Amazon S3:** An object storage service that offers industry-leading scalability, data availability, security, and performance.

6. **Amazon DynamoDB:** A fast and flexible NoSQL database service for all applications that need consistent, single-digit millisecond latency at any scale.

## Workflow
The client script reads customer data from a CSV file and sends it as JSON to the API Gateway via a POST request. The API Gateway then invokes a preprocessing Lambda function, which can retrieve items from the DynamoDB Customers table or write data to the `api_stream_line` Kinesis stream. The Kinesis Data Stream Lambda listens to the stream, batches records, and writes them to an S3 bucket in text file format. Another Lambda function is triggered to process records, updating DynamoDB tables Customers and Invoices.

## Code Structure
### For Client 
`send_json_data`: Sends customer data in JSON format to the specified API endpoint, and `main`: Entry point for the script. It loads environment variables, reads the customer data from the CSV file, and invokes the send_json_data function.
### For DynamoDB
`lambda_handler`: Handles different HTTP methods. It reads data from DynamoDB based on a GET request or writes data to the Kinesis stream using a POST request.
### For Kinesis Data Stream
`lambda_handler:` Processes records from the Kinesis Data Stream and saves them to an S3 bucket. Records are batched and named with a timestamp.
For DynamoDB Update
`lambda_handler:` Processes records from the Kinesis Data Stream and updates DynamoDB tables. It creates or updates items in the Customers and Invoices tables based on the ingested data.
## Usage
- **Configuration:** Set up the required AWS services and ensure they are properly configured to communicate with each other.

- **Environment Setup:** Define the necessary environment variables such as `API_URL` and `CSV_PATH` in a .env file for the input client script.

- Deployment: Deploy the Lambda functions to AWS and configure triggers from API Gateway and Kinesis Data Stream.

- **Execution:** Run the client script to begin the data ingestion process.

## Additional Information
- Make sure that AWS CLI is configured with the necessary permissions to interact with the services used.
- Ensure that the DynamoDB tables have the correct schema for the expected data.

- The Kinesis stream should be configured with an adequate number of shards to handle the volume of data.
- The S3 bucket should have the necessary policies for the Lambda function to write data into it.
- Monitor the Lambda functions' logs for any errors or unexpected behavior during the processing of data.
## Error Handling
- Client-side errors during data sending are logged with the specific row that caused the issue.
- Lambda functions include try-except blocks to catch and log errors during execution.
## Conclusion
This pipeline wass designed to handle scale by leveraging AWS managed services:The API Gateway can handle a large number of incoming requests.
AWS Lambda functions can scale automatically in response to the incoming request or data volume.
Amazon Kinesis and DynamoDB are designed to handle large-scale data throughput and storage.
