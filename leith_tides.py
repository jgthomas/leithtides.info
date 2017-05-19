

from flask import Flask, render_template
from flask_ask import Ask, statement

from tide_response import load_tide_data, get_date_object, build_message
from constants import TIDE_FILE


app = Flask(__name__)

ask = Ask(app, "/alexa_skill")


@app.route('/')
def show_tides():
    low_tides, high_tides = load_tide_data(TIDE_FILE)
    return render_template('base.html', low_tides=low_tides, high_tides=high_tides)


@ask.launch
def tide_report():
    tides = get_date_object(TIDE_FILE)
    welcome_msg = build_message(tides)
    return statement(welcome_msg)


if __name__ == '__main__':

    app.run()
