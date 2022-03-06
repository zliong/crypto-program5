from flask import Blueprint, jsonify


web_api_blueprint = Blueprint('user_api', __name__, template_folder='templates')


@web_api_blueprint.route('/api/v1/<user_email>/', methods=['GET'])
def get_user_list(user_email):
    # get list from DB and return
    return jsonify(email=user_email)
