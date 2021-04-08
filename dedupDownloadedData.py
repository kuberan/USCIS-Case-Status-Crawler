import requests
import re
import sys
import boto3
import datetime
import pytz
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
dynamodb = boto3.resource('dynamodb', region_name='us-east-2', aws_access_key_id='', aws_secret_access_key='')
table = dynamodb.Table('')
for x in range(0,10000):
    for series in range(34,39):
        receiptNumber = "MSC2190" + str(series) + str(x).zfill(4);
        try:
            response = table.query(KeyConditionExpression=Key('receiptNumber').eq(receiptNumber))
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            if(len(response['Items']) > 1):
                #print(response['Items'])
                table.delete_item(Key={'receiptNumber':receiptNumber,'downloadDateTime':response['Items'][0]['downloadDateTime']})
                print(receiptNumber)
