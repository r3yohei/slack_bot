# Slack bot on AWS Lambda
- AWS Lambda + API Gatewayを使用して動作するSlack botの本体ソースコードです
- slack_event_handler.handle_slack_event()が本体
- Lambda側で設定する環境変数
    - CHANNEL_ID_MASTER: マスタユーザのslackチャンネルid (webブラウザでアクセスするとurl末尾に記載されている)
    - CHANNEL_URL_MASTER: マスタユーザのincoming webhook url
    - SLACK_BOT_USER_ACCESS_TOKEN: slack botが所属するワークスペースのOAuth Tokens
    - SLACK_BOT_VERIFY_TOKEN: slack apiのbasic infomation>app credentialsにあるverification token
    - CHANNEL_ID_SLACK_BOT: slack botのチャンネルid
- API Gatewayの設定
    - POSTで作成
    - 統合リクエストのマッピングテンプレートはテンプレートが定義されていない場合 (推奨) を選択し、Content-Typeにapplication/jsonを指定する
- slack apiでのbotアプリ作成概要
    - slack apiへアクセスしてcreate new appからアプリ作成
    - Event Subscriptions>enable eventsのrequest urlへAPI Gatewayのエンドポイントを指定してチャレンジ
    - incoming webhookで好きなチャンネルを追加する
    - Event Subscriptions>Subscribe to bot eventsのmessage.channels, message.groups, message.imを追加(それぞれpublic, private, dmが来た時にそれをLambdaへ投げるための設定)
    - Basic Information>Install your appで自分のワークスペースにアプリをインストール