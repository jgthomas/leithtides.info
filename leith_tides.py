from flask import Flask, render_template
from flask_ask import Ask, statement

from tide_response import load_tide_data, get_date_object, build_message, tide_message
from constants import TIDE_FILE


app = Flask(__name__)

ask = Ask(app, "/alexa_skill")


@app.route('/')
def show_tides():
    low_tides, high_tides = load_tide_data(TIDE_FILE)
    return render_template('base.html',
                           low_tides=low_tides,
                           high_tides=high_tides)


@ask.launch
def tide_report():
    tides = get_date_object(TIDE_FILE)
    response = tide_message(tides)
    return statement(response)

@ask.intent("TodaysTides")
def get_tides():
    tides = get_date_object(TIDE_FILE)
    response = tide_message(tides)
    return statement(response)

@ask.intent("LowTide")
def low_tide_reponse():
    low_tides, _ = get_date_object(TIDE_FILE)
    reponse = tide_message(low_tides, specific_tide="low")
    return statement(response)

@ask.intent("HighTide")
def low_tide_reponse():
    _, high_tides = get_date_object(TIDE_FILE)
    reponse = tide_message(high_tides, specific_tide="high")
    return statement(response)


if __name__ == '__main__':

    app.run()
