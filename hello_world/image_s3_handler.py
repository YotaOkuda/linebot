import os
import logging
import tempfile
import boto3
from linebot import LineBotApi
from linebot.models import TextSendMessage

s3 = boto3.resource('s3')
channel_access_token = os.getenv('CHANNEL_ACCESS_TOKEN')
bucket_name = os.getenv('BUCKET_NAME')
line_bot_api = LineBotApi(channel_access_token)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def lambda_handler(event, context):
    logger.info('Image event received')
    image_id = event["imageid"]
    reply_token = event["replytoken"]
    user_id = event["user_id"]
    image = line_bot_api.get_message_content(image_id)

    with tempfile.TemporaryFile() as tmp:
        for chunk in image.iter_content():
            tmp.write(chunk)
        tmp.seek(0)

        bucket = s3.Bucket(bucket_name)
        bucket.put_object(
            Body=tmp,
            Key=f'{image_id}.png'
        )

    line_bot_api.reply_message(
        reply_token,
        TextSendMessage(text='Image upload successful!')
    )

    return {
        "bucketname": bucket_name,
        "imagename": f"{image_id}.png",
        "user_id": user_id
    }
