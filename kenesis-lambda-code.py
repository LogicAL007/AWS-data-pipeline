from __future__ import print_function

import base64
import json
import boto3
from datetime import datetime

s3_client = boto3.client('s3')

dateTimeObj = datetime.now()

#format the string
timestampStr = dateTimeObj.strftime("%d-%b-%Y-%H%M%S")

kinesisRecords = []

def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))
    for record in event['Records']:

        payload = base64.b64decode(record['kinesis']['data'])


        # append each record to a list
        kinesisRecords.append(payload)
        # this is just for logging
        # print("Decoded payload: " + payload)

    ex_string = '\n'.join(kinesisRecords)

    # generate the name for the file with the timestamp
    mykey = 'output-' + timestampStr + '.txt'

    response = s3_client.put_object(Body=ex_string, Bucket='aws-de-project', Key= mykey)

    return 'Successfully processed {} records.'.format(len(event['Records']))
