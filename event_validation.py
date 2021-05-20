# -*- coding: utf-8 -*-

# 投稿をバリデーションする


import os


# トークンをチェック    
def is_verify_token(token):
    if token != os.environ["SLACK_BOT_VERIFY_TOKEN"]:
        return False
    return True


# botへのメンションか
def is_message_mention(posted_message):
    return "<@" + os.environ["CHANNEL_ID_SLACK_BOT"] + "> " in posted_message


# 発言者がbotかどうか
def is_bot(event) -> bool:
    return event.get("body").get("event").get("subtype") == "bot_message"

    
# 投稿が編集かどうか
def is_edit(event):
    return event.get("body").get("event").get("subtype") == "message_changed"