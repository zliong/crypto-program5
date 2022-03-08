from flask import Blueprint, jsonify
from .core import limiter
import boto3
from boto3.dynamodb.conditions import Key

__TableName__ = "Program5"
dynamodb = boto3.resource("dynamodb", region_name='us-west-2')
table = dynamodb.Table(__TableName__)

web_api_blueprint = Blueprint(
    'user_api', __name__, template_folder='templates')
limiter.limit("200 per day")(web_api_blueprint)


@web_api_blueprint.route('/api/v1/<user_email>/', methods=['GET'])
def get_user_list(user_email):
    # get list from DB and return
    print(user_email)
    response = table.query(
        KeyConditionExpression=Key('email').eq(user_email)
    )
    
    profiles = response["Items"]
    tickers = {}
    for profile in profiles:
        for attribute in profile:
            print(attribute)
            if attribute != 'email' and attribute != 'password':
                tickers[profile[attribute]] = "messari.io/asset/" + attribute
         
    return jsonify(tickers)
