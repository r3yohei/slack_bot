# -*- coding: utf-8 -*-

# 投稿内容の感情認識

import boto3
import json
import logging
import configparser
import random

# ログ設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)
# configファイルの読み込み
conf = configparser.SafeConfigParser()
conf.read("slack_bot_config.config")


def make_emotional_message(posted_message):
    # Comprehend constant
    REGION = "us-west-2"
    language_code = "ja"
    
    message_positive = conf.get("Message", "MESSAGE_POSITIVE").split(",")
    message_negative = conf.get("Message", "MESSAGE_NEGATIVE").split(",")
    message_neutral = conf.get("Message", "MESSAGE_NEUTRAL").split(",")
    
    comprehend = boto3.client('comprehend', region_name=REGION)
    response = comprehend.detect_sentiment(Text=posted_message, LanguageCode=language_code)
    logging.info("Comprehendからの戻り値；" + str(response))
    
    if response.get("Sentiment") == "POSITIVE":
        return_message = random.choice(message_positive)
    elif response.get("Sentiment") == "NEGATIVE":
        return_message = random.choice(message_negative)
    else:
        return_message = random.choice(message_neutral)
    
    return return_message
    