from flask import Flask, render_template
from app.add_page import add_ticker

application = Flask(__name__)
application.register_blueprint(add_ticker)


@application.route('/', methods=['POST', 'GET'])
def home_page():
    return render_template("base.html")


if __name__ == "__main__":
    application.run()
