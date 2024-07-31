import json
import os
import requests

def lambda_handler(event, context):
    finding = event['detail']
    finding_type = finding.get('type', 'Unknown')
    finding_severity = finding.get('severity', 'Unknown')
    print(f"Got GuardDuty Finding: type={finding_type}, severity={finding_severity}")

    host = os.getenv('HOST')
    api_key = os.getenv('API_KEY')
    if not host or not api_key:
        print("HOST or API_KEY environment variables are not set")
        return {
            'statusCode': 500,
            'body': json.dumps('HOST or API_KEY environment variables are not set')
        }

    url = f"http://{host}/v1/workflows/run"
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    payload = {
        "inputs": {
            "type": finding_type,
            "severity": finding_severity,
            "finding": json.dumps(finding)
        },
        "response_mode": "blocking",
        "user": "AnalyzeGuardDuty"
    }
    response = requests.post(url, headers=headers, json=payload)
    print(f"API response: {response.status_code} - {response.text}")

    return {
        'statusCode': 200,
        'body': json.dumps('GuardDuty event processed successfully')
    }
