from flask import Blueprint, jsonify, render_template
import boto3
from boto3.dynamodb.conditions import Key

__TableName__ = 'Program5Users'
dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
table = dynamodb.Table(__TableName__)

web_api_blueprint = Blueprint('user_api', __name__, template_folder='templates')


@web_api_blueprint.route('/api/v1/', methods=['GET'])
def api_home():
    return render_template('user_api_home.html')


@web_api_blueprint.route('/api/v1/information/<user>/', methods=['GET'])
def get_user_list(user):
    response = table.scan(FilterExpression=(Key('email').eq(user) | Key('username').eq(user)))
    profiles = response['Items']
    json_attributes = {}
    tickers = {}
    for profile in profiles:
        for attribute in profile:
            if attribute != 'email' and attribute != 'password' and attribute != 'username' and attribute != 'pfp' and \
                    attribute != 'subscribed':
                tickers[attribute] = "https://www.messari.io/asset/" + attribute
            elif attribute != 'password' and attribute != 'subscribed' and attribute != 'pfp':
                json_attributes[attribute] = profile[attribute]
            elif attribute == 'pfp':
                json_attributes[attribute] = 'https://program5-pictures-zach.s3.us-west-1.amazonaws.com/' + \
                                             profile[attribute]
    return jsonify(user_info=json_attributes, tracked_cryptos=tickers)
