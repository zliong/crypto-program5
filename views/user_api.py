from flask import Blueprint, jsonify
from .core import limiter

web_api_blueprint = Blueprint('user_api', __name__, template_folder='templates')
limiter.limit("1 per day")(web_api_blueprint)

@web_api_blueprint.route('/api/v1/<user_email>/', methods=['GET'])
def get_user_list(user_email):
    # get list from DB and return
   response = table.query(
      KeyConditionExpression=Key('email').eq(user_email)
   )

   profile = response["Items"]
   tickers = {}
   for attribute in profile:
      if attribute != 'username' and attribute != 'password':
         tickers[attribute] = "messari.io/asset/{attribute}"
         
   return jsonify(tickers)
