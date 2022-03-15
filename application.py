from flask import Flask, render_template, request, session, redirect, url_for
from views.add_user import create_user_blueprint
from views.add_user_avatar import create_user_avatar_blueprint
from views.user_api import web_api_blueprint
from views.subscribe import subscribe_blueprint
import boto3
from boto3.dynamodb.conditions import Key, Attr
from datetime import timedelta


application = Flask(__name__)
application.secret_key = '153205090'
application.register_blueprint(create_user_blueprint)
application.register_blueprint(create_user_avatar_blueprint)
application.register_blueprint(web_api_blueprint)
application.register_blueprint(subscribe_blueprint)
application.permanent_session_lifetime = timedelta(minutes=90)
user = {"username": "123", "password": "123"}
application.secret_key = 'cXkaQKw8FWS5cc34'


@application.route('/', methods=['POST', 'GET'])
def home_page():
    return render_template("base.html")


@application.route('/logged_in', methods=['POST', 'GET'])
def logged_in_page():
    pfp_link = 'https://program5-pictures-zach.s3.us-west-1.amazonaws.com/' + session['pfp']
    # email = session['user']
    # # print(email)
    # dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
    # table = dynamodb.Table('Program5Users')
    # response = table.scan(FilterExpression=Key('email').eq(email))
    # # print(response['Items'])
    # pfp_link = response['Items'][0].get('pfp')
    #
    # if pfp_link is None:
    #     pfp_link = 'https://program5-pictures-zach.s3.us-west-1.amazonaws.com/default.png'
    # else:
    print(pfp_link)
    return render_template('logged_in.html', usr_avatar=pfp_link, user=session['user_name'])


@application.route('/login', methods=['POST', 'GET'])
def login():
    email = request.form['text_email']
    password = request.form['text_password']
    print('During login: ' + email)
    dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
    table = dynamodb.Table('Program5Users')
    response = table.scan(FilterExpression=Key('email').eq(email) & Attr('password').eq(password))
    if len(response['Items']) == 0:
        return render_template("base.html", login_fail='User not found')
    else:
        if response['Items'][0].get('pfp') is None:
            session['pfp'] = 'https://program5-pictures-zach.s3.us-west-1.amazonaws.com/default.png'
        else:
            session['pfp'] = response['Items'][0].get('pfp')
        session['user_name']= response['Items'][0].get('username')
        session['user'] = email
    return redirect(url_for('logged_in_page'))


@application.route('/logout', methods=['POST','GET'])
def logout():
    session.pop('user')
    return render_template("base.html", logout='Logged out')


if __name__ == "__main__":
    application.run(debug=True)
