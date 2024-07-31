# (WIP) [実践] AWS上でDifyを使ったセキュリティオペレーション自動化


TODO: 以下は雑なメモで要修正

## 自己紹介


## Difyサーバの構築

### EC2インスタンス作成
- AMI: Amazon Linux 2023
- Instance type: t3.medium (2vCPU, 4GB MEMが必要)
- セキュリティグループ: インバウンドルールにHTTP(80)を追加
- その他は任意で

### docker install
```bash
$ sudo dnf install docker git
$ sudo usermod -a -G docker ssm-user # またはec2-user
$ sudo systemctl enable docker
$ sudo systemctl start docker
$ docker -v
Docker version 25.0.3, build 4debf41

# ここで一度ログアウトして、再度ログインする。（グループが反映されてdockerコマンドが使えるようになる）
```

### docker-compose install
https://matsuand.github.io/docs.docker.jp.onthefly/compose/install/

```bash
$ DOCKER_CONFIG=${DOCKER_CONFIG:-$HOME/.docker}
$ mkdir -p $DOCKER_CONFIG/cli-plugins
$ curl -SL https://github.com/docker/compose/releases/download/v2.29.1/docker-compose-linux-x86_64 -o $DOCKER_CONFIG/cli-plugins/docker-compose
$ chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose
$ docker compose version
Docker Compose version v2.29.1
```

### Difyインストール
https://github.com/langgenius/dify.git
```bash
$ git clone https://github.com/langgenius/dify.git
$ cd dify/docker
$ cp .env.example .env
$ docker compose up -d
```

### 接続
- ここまでで、Difyサーバの立ち上げは完了
- httpsでのアクセスはデフォルトでは対応していない
  - お使いの環境にあわせていくつかの選択肢がある
    - Dify内のnginx設定を修正して直接SSL/TLS終端する
    - ALBを使ってSSL/TLS終端してからDifyサーバにルーティングする
    - VPNで内部ネットワークにトンネルしてhttpでアクセスする
  - オススメはALBを使う方法で、ALB側でOIDC認証（Cognitoなど）を挟むことができる
  - Difyサーバを直接インターネットフェーシングさせずに済むためよりセキュア


### ALBの設定

- ターゲットグループの作成
  - ターゲットの種類は「インスタンス」を指定し、先ほど作成したEC2インスタンスを登録
  - ヘルスチェックは以下にする
    - パス: /signin
    - ステータス: 200
- ALBの設定
  - 先ほどのターゲットグループを指定
  - 適切なセキュリティグループを指定
    - IP制限をかける場合はここで設定（オプション）
  - リスナールールを追加
    - ここで認証の設定も可能（オプション）

- Difyにアクセス
  - https://{ALBのDNS名またはIPアドレス}/install
  - 管理者ユーザを作成してログイン


## Difyの設定

### Bedrockの設定
- 事前にBedrockでClaudeモデルとTitanモデルを利用できるよう有効化しておきます
- 以下のポリシーでIAMロールを作成し、Difyサーバー（EC2）に割り当てます
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "bedrock:InvokeModel*",
            "Resource": [
                "*"
            ]
        }
    ]
}
```
- Dify側でBedrockを有効化します（有効にしたRegionを指定）

### ナレッジの登録

GuardDutyのドキュメント(EC2とIAMだけ)
- https://docs.aws.amazon.com/ja_jp/guardduty/latest/ug/guardduty_finding-types-ec2.html
- https://docs.aws.amazon.com/ja_jp/guardduty/latest/ug/guardduty_finding-types-iam.html


### ワークフローを作成





