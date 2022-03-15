from flask import Blueprint, render_template, session, redirect, url_for

help_blueprint = Blueprint('help', __name__, template_folder='templates')


@help_blueprint.route('/help', methods=['GET'])
def ticker_help():
    try:
        _ = session['user']
    except KeyError:
        return redirect(url_for('home_page'))
    return render_template('help.html', user=session['user_name'], user_avatar=session['pfp'])
