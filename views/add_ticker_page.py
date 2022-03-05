from flask import render_template, request, Blueprint
import math
import requests
from wtforms import Form, StringField


class AddTicker(Form):
    ticker = StringField('Crypto Ticker/Name:')


add_ticker_blueprint = Blueprint('add_page', __name__, template_folder='templates')


@add_ticker_blueprint.route('/add_ticker', methods=['POST', 'GET'])
def add_ticker():
    form = AddTicker(request.form)
    if request.method == 'POST':
        if request.form.get('fetch') == 'Fetch':
            requested_ticker = form.ticker.data.strip()
            if len(requested_ticker) != 0 and requested_ticker is not None and requested_ticker != '':
                # check if ticker is already in user list
                fetch_req = requests.get(f'https://data.messari.io/api/v1/assets/{requested_ticker}/metrics')
                if fetch_req.status_code != 200:
                    return render_template('add_ticker.html', form=form,
                                           invalid_ticker_error='This ticker is invalid or not supported.')
                else:
                    market_data = fetch_req.json()['data']['market_data']
                    usd_price = market_data['price_usd']
                    if usd_price is not None:
                        usd_price = str('{:,}'.format(math.floor(float(usd_price) * 10 ** 2) / 10 ** 2))
                        if len(usd_price.split('.')[1]) == 1:
                            usd_price = usd_price + '0'
                    else:
                        return render_template('add_ticker.html', form=form,
                                               invalid_ticker_error='This ticker is invalid or not supported.')
                    return render_template('add_ticker.html', form=form,
                                           fetched_asset=[str(requested_ticker).upper(), usd_price])
            else:
                return render_template('add_ticker.html', form=form,
                                       ticker_not_filled_error='Please fill in the ticker field.')
        elif request.form.get('add_asset') == 'Add asset to your list':
            # add to user list db
            return render_template('add_ticker.html', form=form, fetched_asset='Dummy,Coin,1010', added_ticker='Added')
    return render_template('add_ticker.html', form=form)
