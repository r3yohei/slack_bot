# -*- coding: utf-8 -*-

import sys
import logging
import json
import random
import configparser
import datetime

import event_validation, post_to_slack, make_message

# ログ設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handle_slack_event(event, context):
    # 受信データをCloud Watchログに出力
    logging.info(json.dumps(event))
    
    # SlackのEvent APIの認証
    if "challenge" in event:
        return event.get("challenge")
    
    # リトライならば、無視する
    if "X-Slack-Retry-Reason" in event.get("headers"):
        logging.info("Slack側のEvents APIによるリトライを無視します。")
        return "OK"
        
    # tokenのチェック
    token = event.get("body").get("token")
    if not event_validation.is_verify_token(token):
        return "OK"
        
    if event_validation.is_bot(event):
        # 発言者がbotの場合スルー
        return "OK"
        
    # 新規投稿か編集かによってメッセージおよびユーザID取得元が異なる
    if not event_validation.is_edit(event):
        # 新規ならevent下に入っている
        posted_message = event.get("body").get("event").get("text")
        user = event.get("body").get("event").get("user")    
    else:
        # 編集ならevent.message下に入っている
        posted_message = event.get("body").get("event").get("message").get("text")
        user = event.get("body").get("event").get("message").get("user")
    
    # channelはいつもここ
    channel = event.get("body").get("event").get("channel")
    
    # botへのメンション時
    if event_validation.is_message_mention(posted_message):
        logging.info("botにメンションされました。")
        # Amazon Comprehendで感情認識
        return_message = make_message.make_emotional_message(posted_message)
        post_to_slack.post_message_to_user_in_channel(user, channel, return_message)
    
    
    return "OK"