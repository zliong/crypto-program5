from flask import Flask, render_template
from views.add_ticker_page import add_ticker_blueprint
from views.user_api import web_api_blueprint

application = Flask(__name__)
application.register_blueprint(add_ticker_blueprint)
application.register_blueprint(web_api_blueprint)


@application.route('/', methods=['POST', 'GET'])
def home_page():
    return render_template("base.html")


if __name__ == "__main__":
    application.run(debug=True)
