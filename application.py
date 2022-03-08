from flask import Flask, render_template, request
from views.add_user import create_user_blueprint
from views.add_user_avatar import create_user_avatar_blueprint
<<<<<<< Updated upstream
=======
import boto3
from boto3.dynamodb.conditions import Key, Attr
>>>>>>> Stashed changes

application = Flask(__name__)
application.secret_key = '153205090'
application.register_blueprint(create_user_blueprint)
application.register_blueprint(create_user_avatar_blueprint)
<<<<<<< Updated upstream
=======

>>>>>>> Stashed changes



@application.route('/', methods=['POST', 'GET'])
def home_page():
    return render_template("base.html")


<<<<<<< Updated upstream
def submit_user_info():   #eventually going to have this completed in this file,since it's the base view
=======
@application.route('/login', methods=['POST', 'GET'])
def login():
>>>>>>> Stashed changes
    email = request.form['text_email']



if __name__ == "__main__":
    application.run(debug=True)
