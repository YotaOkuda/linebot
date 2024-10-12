import json
import os
import urllib.request
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

LINE_CHANNEL_ACCESS_TOKEN = os.environ['LINE_CHANNEL_ACCESS_TOKEN']

REQUEST_URL = 'https://api.line.me/v2/bot/message/reply'
REQUEST_METHOD = 'POST'
REQUEST_HEADERS = {
    'Authorization': 'Bearer ' + LINE_CHANNEL_ACCESS_TOKEN,
    'Content-Type': 'application/json'
}
REQUEST_MESSAGE = [
    {
        'type': 'text',
        'text': 'はろはろ'
    }
]

def lambda_handler(event, context):
    logger.info(event)

    # event に 'body' があるか確認し、なければそのまま処理を終了
    if 'body' not in event:
        logger.error("No 'body' in event")
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid request: No body found')
        }

    # リクエストの body をパース
    try:
        body = json.loads(event['body'])
        reply_token = body['events'][0]['replyToken']
    except (KeyError, json.JSONDecodeError) as e:
        logger.error(f"Error parsing event body: {str(e)}")
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid request: Failed to parse body')
        }

    # LINE API へのリクエストパラメータを設定
    params = {
        'replyToken': reply_token,
        'messages': REQUEST_MESSAGE
    }

    # LINE API へのリクエストを送信
    request = urllib.request.Request(
        REQUEST_URL,
        json.dumps(params).encode('utf-8'),
        method=REQUEST_METHOD,
        headers=REQUEST_HEADERS
    )

    try:
        response = urllib.request.urlopen(request, timeout=10)
        logger.info(f"Response status: {response.status}")
        return {
            'statusCode': 200,
            'body': json.dumps('Success')
        }
    except Exception as e:
        logger.error(f"Error sending reply to LINE: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps('Failed to send reply to LINE')
        }