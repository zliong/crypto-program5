from email import message
from flask import Blueprint, render_template, request, redirect, url_for, session
import boto3
import logging
import time
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)
sns_client = boto3.client('sns')

subscribe_blueprint = Blueprint(
    'subscribe', __name__, template_folder='templates')


@subscribe_blueprint.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    if request.method == "GET":
        return render_template("subscribe.html")
    else:
        # find a way to get the email from session
        topic = 'arn:aws:sns:us-west-2:440026663620:testTopic'
        protocol = 'Email'
        endpoint = 'ejkj699@gmail.com'
        try:
            subscription = sns_client.subscribe(
                TopicArn=topic, Protocol=protocol, Endpoint=endpoint, ReturnSubscriptionArn=True)
            logger.info("Subscribed %s %s to topic %s.", protocol, endpoint, topic)
            mes = "Subscribed {} {} to topic {}.".format(protocol, endpoint, topic)
            #session['messages'] = mes
            #return redirect("/subscribe_confirmation")
            #return subscribe_confirmation(topic, protocol, endpoint)
            return redirect(url_for('subscribe_confirmation', page = "name"))
        except ClientError:
            print("here")
            logger.exception(
                "Couldn't subscribe %s %s to topic %s.", protocol, endpoint, topic)
            print("couldn't do the subscription")

@subscribe_blueprint.route('/subscribe_confirmation/<page>', methods=['GET'])
def subscribe_confirmation(page):
    return "<h1>{}<h1>".format(page)

