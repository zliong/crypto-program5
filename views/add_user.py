from flask import render_template, request, Blueprint, url_for
import requests
import boto3
from werkzeug.utils import redirect
from wtforms import Form, StringField

create_user_blueprint = Blueprint('add_user', __name__, template_folder='templates') #add to blueprint


@create_user_blueprint.route('/create_user', methods=['POST', 'GET'])
def create_user():
    if request.method == 'POST':
        return redirect(url_for('base'))

    return render_template("create_user.html", place_one='Enter email', place_two='Enter Password',
                           place_three='Enter Username')  #add text for place holder


@create_user_blueprint.route('/create_user_submit', methods=['POST', 'GET'])
def create_user_submit():
    email = request.form['text_email']  #get user inputs
    password = request.form['text_password']
    username = request.form['text_username']
    if email == '' or (password == '') or (username == ''):
        return render_template("create_user.html", place_one='fill out all fields')  # If one field is empty
    else:  # add user to DynamoDB                                                    #notify user
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('Program5Users')  #get table
        response = table.put_item(
            Item={'email': email, 'password': password, 'username': username}
        )          #put item into table, email, password, and username
    return render_template("create_user.html") #stay on same page
