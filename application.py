from flask import Flask, render_template, request
from views.add_user import create_user_blueprint

application = Flask(__name__)
application.register_blueprint(create_user_blueprint)


@application.route('/', methods=['POST', 'GET'])
def home_page():
    return render_template("base.html")


def submit_user_info():   #eventually going to have this completed in this file,since it's the base view
    email = request.form['text_email']


if __name__ == "__main__":
    application.run()
