# -*- coding: utf-8 -*-

# 投稿内容に応じて返事を投げる


import os
import json
import urllib.request
import configparser

# creating dict (key:channel_id, value:channel_url)
conf = configparser.ConfigParser()
conf.read('slack_bot_config.config')
channel_id = conf.get("slackchannel", "channel_id").split(",")
channel_url = conf.get("slackchannel", "channel_url").split(",")
channel_dict = dict(zip(channel_id, channel_url))


# メッセージ返却
def post_message_to_channel(channel, message):
    # channel idをkeyにurlを取得
    # get()ならkeyがなければNoneにしてくれる
    url = channel_dict.get(channel)
    
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "Authorization": "Bearer {0}".format(os.environ["SLACK_BOT_USER_ACCESS_TOKEN"])
    }
    if url is not None:
        data = {
            "token": os.environ["SLACK_BOT_VERIFY_TOKEN"],
            "channel": channel,
            "text":  message,
        }
    else:
        # 認識していないチャンネルからメッセージがきたらMasterにアラート
        url = os.environ["CHANNEL_URL_MASTER"]
        error_message = '【ERROR】botが認識していないチャンネルからの投稿が試みられました。チャンネル名: '
        data = {
            "token": os.environ["SLACK_BOT_VERIFY_TOKEN"],
            "channel": os.environ["CHANNEL_ID_MASTER"],
            "text": error_message + "<#" + channel + "> ",
        }

    req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), method="POST", headers=headers)
    urllib.request.urlopen(req)


# メンション付きメッセージ返却
def post_message_to_user_in_channel(user, channel, message):
    # channel idをkeyにurlを取得
    # get()ならkeyがなければNoneにしてくれる
    url = channel_dict.get(channel)
    
    # error handling & creating json
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "Authorization": "Bearer {0}".format(os.environ["SLACK_BOT_USER_ACCESS_TOKEN"])
    }
    if url is not None:
        data = {
            "token": os.environ["SLACK_BOT_VERIFY_TOKEN"],
            "channel": channel,
            "text": "<@" + user + "> " + message,
        }
    else:
        # 認識していないチャンネルからメッセージがきたらMasterにアラート
        url = os.environ["CHANNEL_URL_MASTER"]
        error_message = '【ERROR】botが認識していないチャンネルからの投稿が試みられました。チャンネル名: '
        data = {
            "token": os.environ["SLACK_BOT_VERIFY_TOKEN"],
            "channel": os.environ["CHANNEL_ID_MASTER"],
            "text": error_message + "<#" + channel + "> ",
        }

    # slackへpost
    req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), method="POST", headers=headers)
    urllib.request.urlopen(req)