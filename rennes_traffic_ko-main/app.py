from flask import Flask, render_template, request
from keras.models import load_model

from src.get_data import GetData
from src.utils import create_figure, prediction_from_model 
import logging
import flask_monitoringdashboard as dashboard

# logging configuration - can be s
logging.basicConfig(
    level=logging.ERROR,
    format="{asctime} - {levelname} - {message}", 
    style="{",
    filename="logs/flask_app.log",
    encoding="utf-8",
    filemode="a")

# Set the logging level for the werkzeug logger from Flask to ERROR
logging.getLogger('werkzeug').setLevel(logging.ERROR)

app = Flask(__name__)

data_retriever = GetData(url="https://data.rennesmetropole.fr/api/explore/v2.1/catalog/datasets/etat-du-trafic-en-temps-reel/exports/json?lang=fr&timezone=Europe%2FBerlin&use_labels=true&delimiter=%3B")
data = data_retriever()

model = load_model('model.h5')

fig_map = create_figure(data)
graph_json = fig_map.to_json()

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':

        selected_hour = request.form['hour']

        cat_predict = prediction_from_model(model, selected_hour)

        color_pred_map = {0:[f"Prédiction pour {selected_hour}h : fluide", "green"], 1:[f"Prédiction pour {selected_hour}h : dense", "orange"], 2:[f"Prédiction pour {selected_hour}h : bloqué", "red"]}

        return render_template('home.html', graph_json=graph_json, text_pred=color_pred_map[cat_predict][0], color_pred=color_pred_map[cat_predict][1])

    else:

        return render_template('home.html', graph_json=graph_json)


if __name__ == '__main__':
    app.run(debug=True)

# monitoring dashboard configuration
dashboard.config.init_from(file='config/dashboard_config.cfg')
dashboard.bind(app)