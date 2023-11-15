import pandas as pd
from sklearn.model_selection import train_test_split
import tensorflow as tf

raw_data = pd.read_csv('data/knmi.csv')
raw_data.dropna(inplace=True)
raw_data['rainfall'] = raw_data['rainfall'].astype(int);

features = raw_data.drop(['rainfall', 'station', 'precipitation_duration', 'precipitation_amount', 'date'], axis=1)
target = raw_data['rainfall']
x_train, x_test, y_train, y_test = train_test_split(features, target, test_size=0.1, random_state=56)

layers = tf.keras.layers

model = tf.keras.Sequential([
    layers.Input(shape=(4,), dtype=tf.int32),
    layers.Dense(16, activation='relu'),
    layers.Dense(8, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

model.fit(
    x_train, y_train,
    epochs=50,
    verbose=1,
    validation_data=(x_test, y_test)
)

model.save("out.keras")