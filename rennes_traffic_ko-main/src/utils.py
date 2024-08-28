import plotly.express as px
import numpy as np
import logging


def create_figure(data):

    traffic_mapping = {
        'freeFlow': 'fluide',
        'heavy': 'dense',
        'congested': 'bloqué'
    }

    data['traffic actuel'] = data['traffic'].map(traffic_mapping)

    fig_map = px.scatter_mapbox(
            data,
            title="Traffic en temps réel - mis à jour toutes les heures",
            color="traffic actuel",
            lat="lat",
            lon="lon",
            color_discrete_map={'fluide':'green', 'dense':'orange', 'bloqué':'red'},
            zoom=10,
            height=500,
            mapbox_style="carto-positron"
    )

    return fig_map


def prediction_from_model(model, hour_to_predict):

    input_pred = np.array([0]*24)
    input_pred[int(hour_to_predict)] = 1

    cat_predict = np.argmax(model.predict(np.array([input_pred])))

    return cat_predict


def logger_error(name):
    '''
    logging method to use through all app
    '''
    logger = logging.getLogger(name)
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler("logs/flask_app.log", mode="a", encoding="utf-8")
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger