from flask import render_template, request, Blueprint, url_for, flash
import requests
import boto3
from werkzeug.utils import redirect
from wtforms import Form, StringField
from werkzeug.utils import secure_filename

create_user_blueprint = Blueprint('add_user', __name__, template_folder='templates') #add to blueprint
s3_client = boto3.client('s3', region_name='us-west-1')
bucket_name = 'program5-pictures-zach'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

@create_user_blueprint.route('/', methods=['POST', 'GET'])
def home_page():
    return render_template('base.html')


@create_user_blueprint.route('/create_user', methods=['POST', 'GET'])
def create_user():
    if request.method == 'POST':
        return redirect(url_for('home_page'))

    print('here I am')
    return render_template("create_user.html", place_one='Enter email', place_two='Enter Password',
                           place_three='Enter Username')  #add text for place holder


@create_user_blueprint.route('/create_user_submit', methods=['POST', 'GET'])
def create_user_submit():
    print('Made it to create submit')
    print("Made it to submit file")
    file_to_upload = request.files['filename']  # name of the file in html
    if file_to_upload and check_file_type(file_to_upload.filename):
        file_name = secure_filename(file_to_upload.filename)
        response = s3_client.put_object(ACL='public-read', Body=file_to_upload, Bucket=bucket_name, Key=file_name)
        print("file uploaded!")
        flash(f'Success - {file_to_upload} Is uploaded to {bucket_name}', 'success')
    else:
        print("file failed to upload")
        flash(f'Allowed file type are - png - jpeg - gif - jpg.Please upload proper formats...', 'danger')
    # email = request.form['text_email']  #get user inputs
    # password = request.form['text_password']
    # username = request.form['text_username']
    # if email == '' or (password == '') or (username == ''):
    #     return render_template("create_user.html", place_one='fill out all fields')  # If one field is empty
    # else:  # add user to DynamoDB                                                    #notify user
    #     dynamodb = boto3.resource('dynamodb')
    #     table = dynamodb.Table('Program5Users')  #get table
    #     response = table.put_item(
    #         Item={'email': email, 'password': password, 'username': username}
    #     )          #put item into table, email, password, and username
    return render_template("create_user.html") #stay on same page

def check_file_type(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS