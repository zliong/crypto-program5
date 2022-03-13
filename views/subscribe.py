from email import message
from operator import sub
from flask import Blueprint, render_template, request, redirect, url_for, session
import boto3
import logging
import time
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

logger = logging.getLogger(__name__)
sns_client = boto3.client('sns')
__TableName__ = 'Program5'
dynamodb = boto3.resource("dynamodb", region_name='us-west-2')
table = dynamodb.Table(__TableName__)
dynamodb_client = boto3.client('dynamodb')

subscribe_blueprint = Blueprint(
    'subscribe', __name__, template_folder='templates')


@subscribe_blueprint.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    user_email = 'euan.james.canoy@gmail.com' # change to session email!!!!!!
    # user_email = session['user'] uncomment this when session is connected
    if request.method == "GET":
        # get status if they are subscribed
        response = table.query(
        KeyConditionExpression=Key('email').eq(user_email)
        )
        profiles = response["Items"]
        # do we have to deal with there not being any account?
        user = profiles[0]
        subscribe = False
        if 'subscribed' in user and user['subscribed'] != 'False':
            subscribe = True
        return render_template("subscribe.html", subscribed = subscribe)
    else:
        if "subscribe" in request.form:
                    # find a way to get the email from session
            topic = 'arn:aws:sns:us-west-2:440026663620:testTopic'
            protocol = 'Email'
            endpoint = user_email
            try:
                subscription = sns_client.subscribe(
                    TopicArn=topic, Protocol=protocol, Endpoint=endpoint, ReturnSubscriptionArn=True)
                print(subscription)
                logger.info("Subscribed %s %s to topic %s.", protocol, endpoint, topic)
                dynamodb_client.update_item(
                    TableName = __TableName__,
                    Key = {
                        'email':{'S':user_email}
                    },
                    ExpressionAttributeNames = {
                        '#sub':'subscribed'
                    },
                    UpdateExpression="set #sub = :subs",
                    ExpressionAttributeValues={
                        ':subs': {
                            'S':subscription['SubscriptionArn']
                        }
                    }
                )
                mes = "Subscribed {} {} to topic {}.".format(protocol, endpoint, topic)
                return f"""<h1> {mes} <h1>
                            <a href="/subscribe">go back to subscribe<a>"""
            except ClientError:
                logger.exception(
                    "Couldn't subscribe %s %s to topic %s.", protocol, endpoint, topic)
                return f"""<h1>Could not subscribe go back to the subscribe page to try again<h1>
                            <a href="/subscribe">go back to subscribe/unsubscribe page<a>"""
        else:
            response = table.query(
                KeyConditionExpression=Key('email').eq(user_email)
            )
            profiles = response["Items"]
            # do we have to deal with there not being any account?
            user = profiles[0]
            subscription_Arn = user['subscribed']
            try:
                sns_client.unsubscribe(SubscriptionArn=subscription_Arn)
                dynamodb_client.update_item(
                    TableName = __TableName__,
                    Key = {
                        'email':{'S':user_email}
                    },
                    ExpressionAttributeNames = {
                        '#sub':'subscribed'
                    },
                    UpdateExpression="set #sub = :subs",
                    ExpressionAttributeValues={
                        ':subs': {
                            'S':'False'
                        }
                    }
                )

                return """<h1> unsubscribed from arn:aws:sns:us-west-2:440026663620:testTopic <h1>
                        <a href="/subscribe">go back to subscribe/unsubscribe page<a>"""
            except ClientError:
                # logger.exception("Couldn't unsubscribe to {subscription_arn}.")
                # raise
                return """<h1> you must confirm subscription before unsubscribing <h1>
                            <a href="/subscribe">go back to subscribe/unsubscribe page <a>"""



@subscribe_blueprint.route('/subscribe_confirmation/<page>', methods=['GET'])
def subscribe_confirmation():
    return "<h1>{}<h1>".format()

