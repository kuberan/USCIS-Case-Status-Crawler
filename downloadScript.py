import requests
import re
import sys
import boto3
import datetime
import pytz
dynamodb = boto3.resource('dynamodb', region_name='us-east-2', aws_access_key_id='', aws_secret_access_key='')
table = dynamodb.Table('')
print(table.creation_date_time)
for x in range(0,10000):
    if len(sys.argv) > 1:
        series = sys.argv[1];
    else:
        series = "36";
    receiptNumber = "MSC2190" + series + str(x).zfill(4);
    url = "https://egov.uscis.gov/casestatus/mycasestatus.do";
    #receiptNumber = 'MSC2190364473';
    print (receiptNumber);
    requestParams = {'appReceiptNum':receiptNumber};
    x = requests.post(url, data=requestParams);
    html = x.text;
    #print (html);
    status = re.findall(r'h1>(.*)<',html)[0];
    print (status);
    if status == 'Case Was Updated To Show Fingerprints Were Taken':
        parsed = re.findall(r'As of (.*), fingerprints relating to your Form (.*), [A,P]',html);
        print (parsed);
        form = parsed[0][1];
        dt = parsed[0][0];
    elif status == 'Notice Was Returned To USCIS Because The Post Office Could Not Deliver It':
        parsed = re.findall(r'On (.*), the Post Office returned a notice we sent you for your Form (.*), [A,P,N]',html);
        print (parsed);
        form = parsed[0][1];
        dt = parsed[0][0];
    elif status == 'Card Was Delivered To Me By The Post Office':
        parsed = re.findall(r'On (.*), the Post Office delivered your new card for Receipt Number',html);
        print (parsed);
        dt = parsed[0][0];
        form = '';
    elif status == 'Card Is Being Returned to USCIS by Post Office':
        parsed = re.findall(r'On (.*), the Post Office reported that they are returning your new card',html);
        print (parsed);
        dt = parsed[0][0];
        form = '';
    elif status == 'Card Was Picked Up By The United States Postal Service':
        parsed = re.findall(r'On (.*), the Post Office picked up mail containing your new card',html);
        print (parsed);
        dt = parsed[0][0];
        form = '';
    elif status == 'New Card Is Being Produced':
        parsed = re.findall(r'On (.*), we ordered your new card for Receipt Number', html);
        print (parsed);
        dt = parsed[0][0];
        form = '';
    elif status == 'Document Was Mailed To Me':
        parsed = re.findall(r'On (.*), we mailed your document for Receipt', html);
        print (parsed);
        dt = parsed[0][0];
        form = '';
    elif status == 'Expedite Request Denied':
        parsed = re.findall(r'On (.*), we denied your request for expedited processing of your (.*), [A,P]', html);
        print (parsed);
        dt = parsed[0][0];
        form = parsed[0][1];
    elif status == 'CASE STATUS':
        dt = '';
        form = '';
    elif status == '':
        dt = '';
        form = '';
    elif status == 'Card Was Returned To USCIS':
        parsed = re.findall(r'On (.*), the Post Office returned your new card for Form (.*), A', html);
        print (parsed);
        dt = parsed[0][0];
        form = parsed[0][1];
    elif status == 'Interview Was Completed And My Case Must Be Reviewed':
        parsed = re.findall(r'Form (.*), Application to Register Permanent Residence or Adjust Status, Receipt Number (.*), was',html);
        print (parsed);
        dt = '';
        form = parsed[0][0];
    elif status == 'Correspondence Was Received And USCIS Is Reviewing It':
        parsed = re.findall(r'On (.*), we received your correspondence for (.*), A',html);
        print (parsed);
        dt = parsed[0][0];
        form = parsed[0][1];
    elif status == 'Case is Ready to Be Scheduled for An Interview':
        parsed = re.findall(r'As of (.*), we are ready to schedule your Form (.*), App', html);
        print (parsed);
        dt = parsed[0][0];
        form = parsed[0][1];
    elif status == 'Card Was Received By USCIS Along With My Letter':
        parsed = re.findall(r'On (.*), we received your card for Receipt Number ', html);
        print (parsed);
        dt = parsed[0][0];
        form = '';
    else:
        parsed = re.findall(r'On (.*), we (.*) your Form (.*), [A,P,N]',html);
        print (parsed);
        form = parsed[0][2];
        dt = parsed[0][0];

    downloadPstTime = pytz.utc.localize(datetime.datetime.utcnow()).astimezone(pytz.timezone('US/Pacific')).strftime("%m/%d/%Y, %H:%M:%S")
    print (downloadPstTime);
    dbRecord = {
            'receiptNumber': receiptNumber,
            'downloadDateTime': downloadPstTime,
            'caseStatus': status,
            'date': dt,
            'form': form
    }
    table.put_item(Item=dbRecord)
    #break;
