import main
import boto3
from boto3.dynamodb.conditions import Key

"""
lambda実行
"""
def lambda_handler(event, context):

    # DBを指定
    dynamodb = boto3.resource('dynamodb')

    # テーブルを取得
    table = dynamodb.Table('liveInfo')
    response = table.query(
        KeyConditionExpression=Key('id').eq(1)
    )
    oldLiveTime = response["Items"][0]['liveTime']

    result = main.twitchMain(oldLiveTime)

    # 日時更新処理
    if result is not None:
        table.update_item(
            Key= {
                'id': 1
            },
            UpdateExpression="set liveTime = :lt",
            ExpressionAttributeValues={
            ':lt': result[3]
            }
        )

    return 'success'