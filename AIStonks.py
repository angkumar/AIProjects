import yfinance as yf
stock_data = yf.download('NVDA', start='2015-6-10', end='2025-6-11')
stock_data
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(stock_data['Close'].values.reshape(-1,1))
import numpy as np

def create_dataset(data, time_step):
  X, y = [], []
  for i in range(len(data) - time_step - 1):
    X.append(data[i:(i+time_step), 0])
    y.append(data[i+time_step, 0])

  return np.array(X), np.array(y)

time_step = 100

X, y = create_dataset(scaled_data, time_step)
train_size = 0.8

X_train, X_test = X[:int(X.shape[0]*train_size)], X[int(X.shape[0]*train_size):]
y_train, y_test = y[:int(y.shape[0]*train_size)], y[int(y.shape[0]*train_size):]

import tensorflow as tf

from keras.models import Sequential
from keras.layers import Dense, LSTM

model = Sequential()
model.add(LSTM(64, return_sequences = True, input_shape = (time_step, 1)))
model.add(LSTM(64))
model.add(Dense(64))
model.add(Dense(1))

model.compile(optimizer="adam", loss="mean_squared_error")
model.fit(X_train, y_train, epochs=10, batch_size=64)

test_loss = model.evaluate(X_test, y_test)
test_loss

predictions = model.predict(X_test)
predictions = scaler.inverse_transform(predictions)

original_data = stock_data["Close"].values
predicted_data = np.empty_like(original_data)
predicted_data[:] = np.nan
predicted_data[-len(predictions):] = predictions.reshape(-1, 1)

import matplotlib.pyplot as plt

plt.plot(original_data)
plt.plot(predicted_data)

new_predictions = model.predict(X_test[-90:])
new_predictions = scaler.inverse_transform(new_predictions)

predicted_data = np.append(predicted_data, new_predictions)
predicted_data[-90:]

plt.plot(original_data, label='Original Data')
plt.plot(predicted_data, label='Predicted Data')
plt.legend()
plt.show()