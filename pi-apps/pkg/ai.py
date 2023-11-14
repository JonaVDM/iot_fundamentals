import tensorflow as tf
from pkg.database import Entry
import pandas as pd


class AI:
    model: tf.keras.Model

    def __init__(self):
        self.model = tf.keras.models.load_model('../ai/model.keras')
        self.model.summary()

    def predict(self, entry: Entry):
        input_data = pd.DataFrame({
            'hour': [entry.time.hour],
            'temperature': [int(entry.temperature * 10)],
            'humidity': [int(entry.humidity)],
            'pressure': [int(entry.pressure * 10)]
        })

        return int(self.model.predict(input_data)[0][0])
