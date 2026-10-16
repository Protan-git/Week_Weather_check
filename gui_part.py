from flask import Flask, request, render_template, jsonify, send_file
import plotly.graph_objects as go
import os
from get_api import get_forecast
# from flask_sqlalchemy import SQLAlchemy
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
# db = SQLAlchemy(app)

base_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, template_folder=os.path.join(base_dir, 'templates'))


@app.route('/')
@app.route('/home')
def main():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/user/<string:name>/<int:id>')
def user(name, id):
    return f'User page {name} - {id}'


@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/chart')
def chart():
    data = get_forecast('Rostov-on-Don', 'ru')

    if data is None:
        return 'Не удалось получить прогноз погоды', 500

    times = []
    temperatures = []

    for item in data['list']:
        times.append(item['dt_txt'])
        temperatures.append(item['main']['temp'])

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=times,
        y=temperatures,
        mode='lines+markers',
        name='Температура'
    ))

    fig.update_layout(
        title='Прогноз температуры на 5 дней в городе Rostov-on-Don',
        xaxis_title='Дата и время',
        yaxis_title='Температура, °C',
        template='plotly_white',
        hovermode='x unified'
    )

    graph = fig.to_html(
        full_html=False,
        include_plotlyjs='cdn'
    )

    return render_template('chart.html', graph=graph)



def start():
    app.run(debug=True)


if __name__ == '__main__':
    start()
