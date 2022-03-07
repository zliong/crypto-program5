from flask import render_template, request, Blueprint, flash, url_for, redirect
import requests
import boto3
from werkzeug.utils import secure_filename

create_user_avatar_blueprint = Blueprint('add_user_avatar', __name__, template_folder='templates')  # add to blueprint
s3_client = boto3.client('s3', region_name='us-west-1')
bucket_name = 'program5-pictures-zach'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


@create_user_avatar_blueprint.route('/', methods=['POST', 'GET'])
def index():
    return render_template('base.html')


@create_user_avatar_blueprint.route('/create_user_submit', methods=['POST', 'GET'])
def user_avatar():
    print("hello!")
    if request.method == 'POST':
        if request.form['submit_form'] == 'Submit':
            print("Made it to submit file")
            file_to_upload = request.files['filename']    # name of the file in html
            if file_to_upload and check_file_type(file_to_upload.filename):
                file_name = secure_filename(file_to_upload.filename)
                response = s3_client.put_object(ACL='public-read', Body=file_to_upload, Bucket=bucket_name, Key=file_name)
                print("file uploaded!")
                flash(f'Success - {file_to_upload} Is uploaded to {bucket_name}', 'success')
            else:
                print("file failed to upload")
                flash(f'Allowed file type are - png - jpeg - gif - jpg.Please upload proper formats...', 'danger')


def check_file_type(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

