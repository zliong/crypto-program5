from views.add_ticker_page import add_ticker_blueprint
from views.user_api import web_api_blueprint
from views.subscribe import subscribe_blueprint
from views.core import limiter
from flask import Flask, render_template, request, session
from views.add_user import create_user_blueprint
from views.add_user_avatar import create_user_avatar_blueprint
import boto3
from boto3.dynamodb.conditions import Key, Attr

application = Flask(__name__)
application.secret_key = '153205090'
application.register_blueprint(create_user_blueprint)
application.register_blueprint(create_user_avatar_blueprint)
application.register_blueprint(add_ticker_blueprint)
application.register_blueprint(web_api_blueprint)
application.register_blueprint(subscribe_blueprint)


user = {"username": "123", "password": "123"}
application.secret_key = 'cXkaQKw8FWS5cc34'


@application.route('/', methods=['POST', 'GET'])
def home_page():
    return render_template("base.html")


@application.route('/login', methods=['POST', 'GET'])
def login():
    email = request.form['text_email']
    password = request.form['text_password']
    dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
    table = dynamodb.Table('Program5Users')
    response = table.scan(FilterExpression=Key('email').eq(email) & Attr('password').eq(password))
    if len(response['Items']) == 0:
        return render_template("base.html", login_fail='User not found')
    else:
        session['user'] = email
    return render_template("logged_in.html")


@application.route('/logout', methods=['POST','GET'])
def logout():
    session.pop('user')
    return render_template("base.html", logout='Logged out')


if __name__ == "__main__":
    application.run(debug=True)
