# AnalyzeGuardDuty

EventBridgeからGuardDutyのイベントを受け取り、Difyで分析して、セキュリティチームに通知するLambda関数です。

## 環境変数

- HOST: Difyのホスト名
- API_KEY: DifyのAPIキー

## Difyサーバとの通信

Difyサーバがインターネット公開されてない場合には、VPC内に配置してください。

## Deploy

```
pip3 install -r requirements.txt -t .
zip -r ../dist/AnalyzeGuardDuty.zip .
```

`../dist/AnalyzeGuardDuty.zip`をLambda関数にアップロードしてください。


## Test

以下のJSONファイルでテストしてください

```json
{
  "version": "0",
  "id": "abcdef12-3456-7890-abcd-ef1234567890",
  "detail-type": "GuardDuty Finding",
  "source": "aws.guardduty",
  "account": "123456789012",
  "time": "2021-01-01T12:00:00Z",
  "region": "us-west-2",
  "resources": [],
  "detail": {
    "schemaVersion": "2.0",
    "accountId": "123456789012",
    "region": "us-west-2",
    "type": "Recon:EC2/PortProbeUnprotectedPort",
    "service": {
      "serviceName": "guardduty"
    },
    "severity": 4.0,
    "createdAt": "2021-01-01T12:00:00Z",
    "updatedAt": "2021-01-01T12:00:00Z",
    "title": "EC2 instance i-1234567890abcdef0 is being probed",
    "description": "EC2 instance i-1234567890abcdef0 is being probed on port 22.",
    "sourceIpAddress": "192.0.2.0",
    "resource": {
      "resourceType": "Instance",
      "instanceDetails": {
        "instanceId": "i-1234567890abcdef0",
        "instanceType": "t2.micro",
        "launchTime": "2021-01-01T10:00:00Z",
        "platform": "Linux"
      }
    }
  }
}
```