import wtforms
from wtforms import Form, StringField, PasswordField
from views.add_ticker_page import add_ticker_blueprint
from views.user_api import web_api_blueprint
from views.subscribe import subscribe_blueprint
from views.help import help_blueprint
from flask import Flask, render_template, request, session, redirect, url_for
from views.add_user import create_user_blueprint
import boto3
from boto3.dynamodb.conditions import Key, Attr
from datetime import timedelta
import requests
import math


class LoginUser(Form):
    email_username = StringField('Email/Username:', validators=[wtforms.validators.InputRequired()])
    password = PasswordField('Password:', validators=[wtforms.validators.InputRequired()])


application = Flask(__name__)
application.permanent_session_lifetime = timedelta(minutes=90)
application.secret_key = 'cXkaQKw8FWS5cc34'
application.register_blueprint(create_user_blueprint)
application.register_blueprint(add_ticker_blueprint)
application.register_blueprint(web_api_blueprint)
application.register_blueprint(subscribe_blueprint)
application.register_blueprint(help_blueprint)
dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
table = dynamodb.Table('Program5Users')


@application.route('/', methods=['POST', 'GET'])
def home_page():
    try:
        _ = session['user']
        return redirect(url_for('logged_in_page'))
    except KeyError:
        pass
    form = LoginUser(request.form)
    if request.method == 'POST':
        email_username = form.email_username.data.strip()
        password = form.password.data.strip()
        response = table.scan(FilterExpression=(Key('email').eq(email_username) | Key('username').eq(email_username))
                              & Attr('password').eq(password))
        if len(response['Items']) == 0:
            return render_template('base.html', login_fail='Invalid email/username or password.', form=form)
        else:
            if response['Items'][0].get('pfp') is None:
                session['pfp'] = 'https://program5-pictures-zach.s3.us-west-1.amazonaws.com/accountpicture.png'
            else:
                session['pfp'] = 'https://program5-pictures-zach.s3.us-west-1.amazonaws.com/' + \
                                 response['Items'][0].get('pfp')
            session['user_name'] = response['Items'][0].get('username')
            session['user'] = response['Items'][0].get('email')
        return redirect(url_for('logged_in_page'))
    return render_template('base.html', form=form)


@application.route('/logged_in', methods=['POST', 'GET'])
def logged_in_page():
    try:
        email = session['user']
    except KeyError:
        return redirect(url_for('home_page'))
    pfp_link = session['pfp']
    check_exists = table.get_item(
        Key={
            'email': email
        }
    )
    item = check_exists['Item']
    assets = []
    for key in item:
        if key != 'password' and key != 'username' and key != 'email' and key != 'pfp' and key != 'subscribed':
            assets.append([key, item[key]])
    if request.method == 'POST':
        if request.form.get('refresh') == 'Refresh Prices':
            for asset in assets:
                fetch_req = requests.get(f'https://data.messari.io/api/v1/assets/{asset[0]}/metrics')
                usd_price = fetch_req.json()['data']['market_data']['price_usd']
                usd_price = str('{:,}'.format(math.floor(float(usd_price) * 10 ** 2) / 10 ** 2))
                if len(usd_price.split('.')[1]) == 1:
                    usd_price = usd_price + '0'
                table.update_item(
                    Key={
                        'email': email
                    },
                    UpdateExpression=f'SET {asset[0]} = :ticker',
                    ExpressionAttributeValues={
                        ':ticker': usd_price
                    }
                )
            return redirect(url_for('logged_in_page'))
    return render_template('logged_in.html', user_avatar=pfp_link, user=session['user_name'], item=assets)


@application.route('/logout', methods=['GET'])
def logout():
    try:
        _ = session['user']
    except KeyError:
        return redirect(url_for('home_page'))
    session.pop('user')
    return redirect(url_for('home_page'))


@application.errorhandler(404)
def invalid_route(e):
    return redirect(url_for('home_page'))


if __name__ == '__main__':
    application.run(debug=True)
