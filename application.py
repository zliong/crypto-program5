from flask import Flask, render_template, request
import requests
from wtforms import Form, StringField


application = Flask(__name__)


class AddTicker(Form):
    ticker = StringField('Crypto Ticker:')


@application.route('/', methods=['POST', 'GET'])
def home_page():
    return render_template("base.html")


@application.route('/home', methods=['POST', 'GET'])
def home():
    form = AddTicker(request.form)
    if request.method == 'POST':
        requested_ticker = form.ticker.data.strip()
        if len(requested_ticker) != 0 and requested_ticker is not None and requested_ticker != '':
            fetch_req = requests.get(f'https://data.messari.io/api/v1/assets/{requested_ticker}/metrics')
            if fetch_req.status_code != 200:
                pass  # render error
            else:
                pass  # we know that this is a valid ticker, add it to db
        else:
            return render_template("home.html", form=form, ticker_not_filled='Please fill in the ticker field.')
    return render_template("home.html", form=form)


if __name__ == "__main__":
    application.run(debug=True)
