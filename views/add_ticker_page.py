import boto3
from flask import Blueprint, render_template, redirect, request, session, url_for
import math
import requests
from wtforms import Form, StringField


class AddTicker(Form):
    ticker = StringField('Crypto Ticker/Name:')


add_ticker_blueprint = Blueprint('add_ticker_page', __name__, template_folder='templates')
dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
table = dynamodb.Table('Program5Users')


@add_ticker_blueprint.route('/add_ticker', methods=['POST', 'GET'])
def add_ticker():
    try:
        email = session['user']
    except KeyError:
        return redirect(url_for('home_page'))
    pfp_link = session['pfp']
    form = AddTicker(request.form)
    check_exists = table.get_item(
        Key={
            'email': email
        }
    )
    item = check_exists['Item']
    assets = []
    for key in item:
        if key != 'password' and key != 'username' and key != 'email' and key != 'pfp' and key != 'subscribed':
            assets.append(key)
    if request.method == 'POST':
        if request.form.get('fetch') == 'Fetch' and form.validate():
            requested_ticker = form.ticker.data.strip()
            if len(requested_ticker) != 0 and requested_ticker is not None and requested_ticker != '':
                fetch_req = requests.get(f'https://data.messari.io/api/v1/assets/{requested_ticker}/metrics')
                if fetch_req.status_code != 200:
                    return render_template('add_ticker.html', form=form,
                                           invalid_ticker_error='This crypto ticker/name is invalid or not supported.',
                                           item=assets, user=session['user_name'], user_avatar=pfp_link)
                else:
                    data = fetch_req.json()['data']
                    market_data = data['market_data']
                    symbol = data['symbol']
                    slug = data['slug']
                    usd_price = market_data['price_usd']
                    if usd_price is not None:
                        usd_price = str('{:,}'.format(math.floor(float(usd_price) * 10 ** 2) / 10 ** 2))
                        if len(usd_price.split('.')[1]) == 1:
                            usd_price = usd_price + '0'
                    else:
                        return render_template('add_ticker.html', form=form,
                                               invalid_ticker_error='This crypto '
                                                                    'ticker/name is invalid or not supported.',
                                               user=session['user_name'], user_avatar=pfp_link)
                    if item.get(str(requested_ticker).upper()) is not None or item.get(str(symbol).upper()) \
                            is not None or item.get(str(slug).upper()) is not None:
                        return render_template('add_ticker.html', form=form,
                                               fetched_asset=[str(symbol).upper(), usd_price, False,
                                                              f'https://messari.io/asset/{requested_ticker}'],
                                               item=assets, user=session['user_name'], user_avatar=pfp_link)
                    elif len(item) == 10:
                        return render_template('add_ticker.html', form=form,
                                               fetched_asset=[str(symbol).upper(), usd_price, 'Max Items',
                                                              f'https://messari.io/asset/{requested_ticker}'],
                                               item=assets, user=session['user_name'], user_avatar=pfp_link)
                    else:
                        return render_template('add_ticker.html', form=form,
                                               fetched_asset=[str(symbol).upper(), usd_price, True,
                                                              f'https://messari.io/asset/{requested_ticker}'],
                                               item=assets, user=session['user_name'], user_avatar=pfp_link)
            else:
                return render_template('add_ticker.html', form=form,
                                       ticker_not_filled_error='Please fill in the ticker/name field.', item=assets,
                                       user=session['user_name'], user_avatar=pfp_link)
        elif request.form.get('add_asset') == 'Add asset to your list':
            data = request.form.get('ticker_and_price').split(': ')
            ticker = data[0]
            cur_price = str(data[1])[1:].strip()
            table.update_item(
                Key={
                    'email': email
                },
                UpdateExpression=f'SET {ticker} = :ticker',
                ExpressionAttributeValues={
                    ':ticker': cur_price
                }
            )
            return redirect(url_for('add_ticker_page.add_ticker'))
        elif request.form.get('delete_asset') == 'Delete asset from your list':
            data = request.form.get('ticker_and_price').split(': ')
            ticker = data[0]
            table.update_item(
                Key={
                    'email': email
                },
                UpdateExpression=f'REMOVE {ticker}'
            )
            return redirect(url_for('add_ticker_page.add_ticker'))
        elif request.form.get('remove_all') == 'Remove All':
            for asset in assets:
                table.update_item(
                    Key={
                        'email': email
                    },
                    UpdateExpression=f'REMOVE {asset}'
                )
            return redirect(url_for('add_ticker_page.add_ticker'))
        elif request.form.get('remove').startswith('Remove'):
            ticker = request.form.get('remove').split()[1]
            table.update_item(
                Key={
                    'email': email
                },
                UpdateExpression=f'REMOVE {ticker}'
            )
            return redirect(url_for('add_ticker_page.add_ticker'))
    return render_template('add_ticker.html', form=form, item=assets, user=session['user_name'], user_avatar=pfp_link)
