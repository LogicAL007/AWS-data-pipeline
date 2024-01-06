import json
import boto3


def lambda_handler(event, context):
    print("MyEvent:")
    print(event)

    mycontext = event.get("context")
    method = mycontext.get("http-method")

    if method == "GET":
        dynamo_client = boto3.client('dynamodb')

        im_customerID = event['params']['querystring']['CustomerID']
        print(im_customerID)

        try:
            response = dynamo_client.get_item(TableName='Customers', Key={'CustomerID': {'N': im_customerID}})
            item = response.get('Item')

            if item:
                print(item)
                return {
                    'statusCode': 200,
                    'body': json.dumps(item)
                }
            else:
                return {
                    'statusCode': 404,
                    'body': json.dumps(f"Item with CustomerID {im_customerID} not found.")
                }
        except Exception as e:
            print(f"Error reading from DynamoDB: {e}")
            return {
                'statusCode': 500,
                'body': json.dumps(f"Error reading from DynamoDB: {e}")
            }

    elif method == "POST":
        print('writing to kinesis: ')
        try:
            client = boto3.client('kinesis')
            p_record = event['body-json']
            recordstring = json.dumps(p_record)

            response = client.put_record(
                StreamName='api_stream_line',
                Data=recordstring,
                PartitionKey='string'  # Consider using a meaningful value for the partition key
            )

            return {
                'statusCode': 200,
                'body': json.dumps(p_record)
            }
        except Exception as e:
            print(f"Error writing to Kinesis: {e}")
            return {
                'statusCode': 500,
                'body': json.dumps(f"Error writing to Kinesis: {e}")
            }

    else:
        return {
            'statusCode': 501,
            'body': json.dumps("Server Error")
        }
