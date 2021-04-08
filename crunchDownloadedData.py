import requests
import re
import sys
import boto3
import datetime
import pytz
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
dynamodb = boto3.resource('dynamodb', region_name='us-east-2', aws_access_key_id='', aws_secret_access_key=')
table = dynamodb.Table('')
dataCrunch = {}
for series in range(36,37):
    print(series)
    for x in range(0,10000):
        print (x);
        receiptNumber = "MSC2190" + str(series) + str(x).zfill(4);
        try:
            response = table.query(KeyConditionExpression=Key('receiptNumber').eq(receiptNumber) & Key('downloadDateTime').begins_with('03/07'))
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            if len(response['Items']) == 0:
                print (receiptNumber);
            else:
                if response['Items'][0]['caseStatus'] in dataCrunch:
                    dataCrunch[response['Items'][0]['caseStatus']] = dataCrunch[response['Items'][0]['caseStatus']] + 1;
                else:
                    dataCrunch[response['Items'][0]['caseStatus']] = 1;
for key in dataCrunch.keys():
    print(key,':',dataCrunch[key]);
