from flask import Flask, render_template, request
from views.add_user import create_user_blueprint
from views.add_user_avatar import create_user_avatar_blueprint

import boto3
from boto3.dynamodb.conditions import Key, Attr

application = Flask(__name__)
application.secret_key = '153205090'
application.register_blueprint(create_user_blueprint)
application.register_blueprint(create_user_avatar_blueprint)


@application.route('/', methods=['POST', 'GET'])
def home_page():
    return render_template("base.html")


@application.route('/login', methods=['POST', 'GET'])
def login():
    email = request.form['text_email']


if __name__ == "__main__":
    application.run(debug=True)
