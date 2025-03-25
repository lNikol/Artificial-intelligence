import numpy as np
import matplotlib.pyplot as plt

from data import get_data, inspect_data, split_data

data = get_data()
inspect_data(data)

train_data, test_data = split_data(data)

# Simple Linear Regression
# predict MPG (y, dependent variable) using Weight (x, independent variable) using closed-form solution
# y = theta_0 + theta_1 * x - we want to find theta_0 and theta_1 parameters that minimize the prediction error

# We can calculate the error using MSE metric:
# MSE = SUM (from i=1 to n) (actual_output - predicted_output) ** 2

# get the columns
y_train = train_data['MPG'].to_numpy()
x_train = train_data['Weight'].to_numpy()

y_test = test_data['MPG'].to_numpy()
x_test = test_data['Weight'].to_numpy()

x_train_mean = np.mean(x_train)
y_train_mean = np.mean(y_train)

x_train_std2 = np.std(x_train)
y_train_std2 = np.std(y_train)

# TODO: calculate closed-form solution
# Reshape data to column vectors
x_train = x_train.reshape(-1, 1)
y_train = y_train.reshape(-1, 1)
x_test = x_test.reshape(-1, 1)
y_test = y_test.reshape(-1, 1)

# Add bias term (theta_0) to the feature matrix
X_train = np.hstack((np.ones((x_train.shape[0], 1)), x_train))
X_test = np.hstack((np.ones((x_test.shape[0], 1)), x_test))

# Calculate theta using the closed-form solution: theta = (X^T X)^(-1) X^T y
theta_best = np.linalg.solve(X_train.T @ X_train, X_train.T @ y_train)

# Predictions
y_train_pred = X_train @ theta_best
y_test_pred = X_test @ theta_best

# TODO: calculate error
def mse(y_pred, y):
    return np.mean((y_pred - y)**2)

mse_train = mse(y_train_pred, y_train)
mse_test = mse(y_test_pred, y_test)

print(f"Closed-form solution: {mse_train=}, {mse_test=}")

# plot the regression line
x = np.linspace(min(x_test), max(x_test), 100)
y = float(theta_best[0]) + float(theta_best[1]) * x
plt.plot(x, y, label='Closed-form solution')
plt.scatter(x_test, y_test, color='red', label='Test data')
plt.xlabel('Weight')
plt.ylabel('MPG')
plt.legend()
plt.show()

# TODO: standardization
def standardize(x, m=None, s=None):
    if m is None:
        m = np.mean(x)
    if s is None:
        s = np.std(x)
    return (x - m) / s

def destandardize(x, mean, std):
    return x * std + mean

# Standardize training data
x_train_std = standardize(x_train)
y_train_std = standardize(y_train)

# Standardize test data using mean and std from training data
x_test_std = standardize(x_test, m=np.mean(x_train), s=np.std(x_train))
y_test_std = standardize(y_test, m=np.mean(y_train), s=np.std(y_train))

# Add bias term to standardized data
X_train_std = np.hstack((np.ones((x_train_std.shape[0], 1)), x_train_std))
X_test_std = np.hstack((np.ones((x_test_std.shape[0], 1)), x_test_std))

# TODO: calculate theta using Batch Gradient Descent
eta = 0.1  # Learning rate
theta = np.random.randn(2, 1)  # Initialize theta randomly
m = X_train_std.shape[0]  # Number of training examples

for epoch in range(1000):  # Number of iterations
    y_train_pred_std = X_train_std @ theta  # Predictions
    grad = 2/m * X_train_std.T @ (y_train_pred_std - y_train_std)  # Gradient
    theta -= eta * grad  # Update theta
    if epoch % 100 == 0:  # Print MSE every 100 epochs
        print(f"Epoch {epoch}: MSE = {mse(y_train_pred_std, y_train_std)}")

theta_best = theta

# Predictions on standardized test data
y_test_pred_std = X_test_std @ theta

# Destandardize predictions
y_test_pred_destd = destandardize(y_test_pred_std, y_train_mean, y_train_std2)

# TODO: calculate error
mse_train_std = mse(y_train_pred_std, y_train_std)
mse_test_std = mse(y_test_pred_std, y_test_std)
mse_test_destd = mse(y_test_pred_destd, y_test)

print(f"Gradient Descent (standardized): {mse_train_std=}, {mse_test_std=}")
print(f"Gradient Descent (destandardized): {mse_test_destd=}")


# plot the regression line for standardized data
x_std = np.linspace(min(x_test_std), max(x_test_std), 100)
y_std = float(theta[0]) + float(theta[1]) * x_std
plt.plot(x_std, y_std, label='Gradient Descent')
plt.scatter(x_test_std, y_test_std, color='red', label='Test data (std)')
plt.xlabel('Weight (std)')
plt.ylabel('MPG (std)')
plt.legend()
plt.show()