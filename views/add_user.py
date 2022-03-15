import re
import wtforms.validators
from flask import render_template, request, Blueprint, flash
import boto3
from wtforms import Form, StringField, PasswordField
from werkzeug.utils import secure_filename
from boto3.dynamodb.conditions import Key


class CreateUser(Form):
    email = StringField('Email:', validators=[wtforms.validators.InputRequired()])
    username = StringField('Username:', validators=[wtforms.validators.InputRequired(),
                                                    wtforms.validators.Length(min=3)])
    password = PasswordField('Password:', validators=[wtforms.validators.InputRequired(),
                                                      wtforms.validators.Length(min=5)])


create_user_blueprint = Blueprint('add_user', __name__, template_folder='templates')
s3_client = boto3.client('s3', region_name='us-west-1')
bucket_name = 'program5-pictures-zach'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


@create_user_blueprint.route('/create_user', methods=['POST', 'GET'])
def create_user():
    form = CreateUser(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data.strip()
        username = form.username.data.strip()
        password = form.password.data.strip()
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.fullmatch(regex, email):
            flash('Invalid email format.')
            return render_template('create_user.html', form=form)
        file_to_upload = request.files['filename']
        if file_to_upload and check_file_type(file_to_upload.filename):
            file_name = secure_filename(file_to_upload.filename)
            s3_client.put_object(ACL='public-read', Body=file_to_upload,
                                 Bucket=bucket_name, Key=username + '_' + file_name)
            default = False
        elif not file_to_upload:
            file_name = 'default.png'
            default = True
        else:
            flash('Please upload proper formats. Allowed file type are - png - jpeg - gif - jpg.')
            return render_template("create_user.html", form=form)
        if email == '' or password == '' or username == '':
            return render_template("base.html", place_one='fill out all fields')
        else:
            dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
            table = dynamodb.Table('Program5Users')
            response = table.scan(FilterExpression=Key('username').eq(username))
            if response['Items']:
                flash('Username already exists.')
                return render_template('create_user.html', form=form)
            response = table.scan(FilterExpression=Key('email').eq(email))
            if response['Items']:
                flash('Email already exists.')
                return render_template('create_user.html', form=form)
            elif len(response['Items']) != 1 and default is True:
                table.put_item(
                    Item={'email': email, 'password': password, 'username': username, 'pfp': file_name,
                          'subscribed': 'False'}
                )
            else:
                table.put_item(
                    Item={'email': email, 'password': password, 'username': username,
                          'pfp': username + '_' + file_name, 'subscribed': 'False'}
                )
            return render_template('create_user.html', form=form, created='User has successfully been created!')
    return render_template('create_user.html', form=form)


def file_name_split(file_name):
    name_arr = file_name.split('.')
    return name_arr[0]


def check_file_type(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
