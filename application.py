from flask import Flask, render_template


application = Flask(__name__)


@application.route('/', methods=['POST', 'GET'])
def home_page():
    return render_template("base.html")


if __name__ == "__main__":
    application.run()