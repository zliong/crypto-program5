from flask import render_template, request, Blueprint
import requests
from wtforms import Form, StringField


class AddTicker(Form):
    ticker = StringField('Crypto Ticker:')


add_ticker = Blueprint('add_page', __name__, template_folder='templates')


@add_ticker.route('/add', methods=['POST', 'GET'])
def add():
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
            return render_template("add.html", form=form, ticker_not_filled='Please fill in the ticker field.')
    return render_template("add.html", form=form)
