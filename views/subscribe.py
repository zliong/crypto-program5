from flask import Blueprint, render_template, request, session
import boto3
import logging
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

logger = logging.getLogger(__name__)
sns_client = boto3.client('sns', region_name='us-west-1')
__TableName__ = 'Program5Users'
dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
table = dynamodb.Table(__TableName__)
dynamodb_client = boto3.client('dynamodb', region_name='us-west-1')

subscribe_blueprint = Blueprint('subscribe', __name__, template_folder='templates')


@subscribe_blueprint.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    try:
        user_email = session['user']
    except KeyError:
        return '<h1> Not logged in. </h1>'
    pfp_link = session['pfp']
    if request.method == 'GET':
        response = table.query(
            KeyConditionExpression=Key('email').eq(user_email)
        )
        profiles = response["Items"]
        user = profiles[0]
        subscribed = False
        if 'subscribed' in user and user['subscribed'] != 'False':
            subscribed = True
        return render_template('subscribe.html', subscribed=subscribed, user_avatar=pfp_link, user=session['user_name'])
    else:
        if 'subscribe' in request.form:
            topic = 'arn:aws:sns:us-west-1:139114520614:crypto_notifications'
            protocol = 'Email'
            endpoint = user_email
            try:
                subscription = sns_client.subscribe(TopicArn=topic, Protocol=protocol, Endpoint=endpoint,
                                                    ReturnSubscriptionArn=True)
                print(subscription)
                logger.info("Subscribed %s %s to topic %s.", protocol, endpoint, topic)
                dynamodb_client.update_item(
                    TableName=__TableName__,
                    Key={
                        'email': {'S': user_email}
                    },
                    ExpressionAttributeNames={
                        '#sub': 'subscribed'
                    },
                    UpdateExpression="set #sub = :subs",
                    ExpressionAttributeValues={
                        ':subs': {
                            'S': subscription['SubscriptionArn']
                        }
                    }
                )
                mes = f'Subscribed \"{endpoint}\" to the Email Notification List. ' \
                      'Please confirm the email in your inbox!'
                return f"""<h1> {mes} <h1>
                            <a href="/subscribe">Go back.<a>"""
            except ClientError:
                logger.exception(
                    "Couldn't subscribe %s %s to topic %s.", protocol, endpoint, topic)
                return f"""<h1>Could not subscribe, please go back to the subscribe page to try again.<h1>
                            <a href="/subscribe">Go back.<a>"""
        else:
            response = table.query(
                KeyConditionExpression=Key('email').eq(user_email)
            )
            profiles = response["Items"]
            user = profiles[0]
            subscription_arn = user['subscribed']
            try:
                sns_client.unsubscribe(SubscriptionArn=subscription_arn)
                dynamodb_client.update_item(
                    TableName=__TableName__,
                    Key={
                        'email': {'S': user_email}
                    },
                    ExpressionAttributeNames={
                        '#sub': 'subscribed'
                    },
                    UpdateExpression="set #sub = :subs",
                    ExpressionAttributeValues={
                        ':subs': {
                            'S': 'False'
                        }
                    }
                )

                return """<h1> Unsubscribed from the Email Notification List! You will no longer receive emails. <h1>
                          <a href="/subscribe">Go back.<a>"""
            except ClientError:
                return """<h1> You cannot unsubscribe at this time. Please confirm the subscription sent to your email 
                               before unsubscribing<h1>
                          <a href="/subscribe">Go back.<a>"""


@subscribe_blueprint.route('/subscribe_confirmation/<page>', methods=['GET'])
def subscribe_confirmation():
    return "<h1>{}<h1>".format()
