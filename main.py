import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score
import json
from setting import config
from sklearn.svm import LinearSVC
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_auc_score


def is_2d(value):
    if isinstance(value, list) and all(isinstance(i, list) for i in value):
        return True
    return False


def removePropertyFromJson(property, json):
    for i in range(len(json)):
        del json[i][property]

    return json


def load_data(filename):
    """
    This function loads data from a JSON file and returns a Pandas DataFrame. If the DataFrame contains any NaN values, they are replaced with 0.

    Inputs:
        filename (str): The filepath of the JSON file to be loaded.

    Returns:
        result (pandas.DataFrame): The resulting DataFrame containing the data from the JSON file.
    """
    with open(filename, 'r') as f:
        data = json.load(f)
    data = removePropertyFromJson('sha256', data)
    result = pd.DataFrame(data)
    result = result.fillna(0)
    return result


def preprocess_data(X, y):
    """"
        This function preprocesses the input data by scaling the feature values and encoding the labels as integers.

    Inputs:
        X (pandas.DataFrame or numpy.ndarray): The feature values to be processed.
        y (pandas.Series or numpy.ndarray): The labels to be processed.

    Returns:
        X_scaled (numpy.ndarray): The scaled feature values.
        y_encoded (numpy.ndarray): The encoded labels.

    """
    # Scale the feature values using a StandardScaler
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Encode the labels as integers
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    return X_scaled, y_encoded


def compute_subgradients(v, X, y, C, sample_size):
    """
        This function computes the subgradients of the objective function for a given set of model parameters.

    Inputs:
        v (tuple): A tuple containing the weights and bias term of the model.
        X (numpy.ndarray): The feature values of the training data.
        y (numpy.ndarray): The labels of the training data.
        C (float): The regularization parameter.
        sample_size (int): The size of the sample subset used to approximate the subgradients.

    Returns:
        subgrad_w (numpy.ndarray): The subgradient of the objective function with respect to the weights.
        subgrad_b (float): The subgradient of the objective function with respect to the bias term.
    """

    w, b = v
    n = len(X)
    # if sample_size > n:
    #     sample_size = n
    # # n = len(X)
    sample_size = min(n, sample_size)
    margin = y * (np.dot(X, w) + b)
    hinge_loss = np.maximum(0, 1 - margin)
    hinge_loss[hinge_loss == 0] = 1
    sample_indices = np.random.choice(n, sample_size, replace=False)
    X_sample = X[sample_indices]
    y_sample = y[sample_indices]
    margin_sample = y_sample * (np.dot(X_sample, w) + b)
    hinge_loss_sample = np.maximum(0, 1 - margin_sample)
    subgrad_w = w - C * \
        np.sum(X_sample * y_sample[:, np.newaxis] *
               hinge_loss_sample[:, np.newaxis], axis=0)
    subgrad_b = - C * np.sum(y_sample * hinge_loss_sample)
    return subgrad_w, subgrad_b


def compute_objective_function(v, X, y, C, sample_size):
    """
    This function computes the objective function value for a given set of model parameters.

    Inputs:
        v (tuple): A tuple containing the weights and bias term of the model.
        X (numpy.ndarray): The feature values of the training data.
        y (numpy.ndarray): The labels of the training data.
        C (float): The regularization parameter.
        sample_size (int): The size of the sample subset used to approximate the objective function value.

    Returns:
        obj_value (float): The value of the objective function.
    """
    w, b = v
    n = len(X)
    # if sample_size > n:
    #     sample_size = n
    # # n = len(X)
    sample_size = min(n, sample_size)
    margin = y * (np.dot(X, w) + b)
    hinge_loss = np.maximum(0, 1 - margin)
    hinge_loss[hinge_loss == 0] = 1
    sample_indices = np.random.choice(n, sample_size, replace=False)
    X_sample = X[sample_indices]
    y_sample = y[sample_indices]
    obj_value = 0.5 * np.linalg.norm(w) ** 2 + C * np.mean(hinge_loss)
    return obj_value


def train_model(X_train, y_train, C, epsilon):
    """
        This function trains a Sec-SVM classifier model on the input training data.

    Inputs:
        X_train (numpy.ndarray): The feature values for the training data.
        y_train (numpy.ndarray): The labels for the training data.
        C (float): The regularization parameter.
        epsilon (float): A small constant used to determine when to stop the training.

    Returns:
        model (sklearn.svm.LinearSVC): The trained Sec-SVM model.
    """
    # Initialize the model
    model = LinearSVC(C=C, random_state=0, tol=epsilon)
    model.fit(X_train, y_train)
    return model


def evaluate_model(model, X_test, y_test):
    """
    This function evaluates a model on the test data.

    Inputs:
        model (sklearn.svm.LinearSVC): The trained model.
        X_test (numpy.ndarray): The feature values for the test data.
        y_test (numpy.ndarray): The labels for the test data.

    Returns:
        accuracy (float): The accuracy score of the model.
        precision (float): The precision score of the model.
        recall (float): The recall score of the model.
    """
    # Predict the labels on the test data using the model
    # y_pred = model.predict(X_test)
    threshold = 0.5
    y_pred = model.predict(X_test)
    # y_pred[y_pred >= threshold] = 1
    # y_pred[y_pred < threshold] = 0
    # Compute the accuracy, precision, and recall scores
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    plotting(y_pred[:100], y_test[:100])

    return accuracy, precision, recall


def classify_apk(model, apk_features):
    """
        This function makes a prediction for a new APK by using the trained model to classify the APK based on its features.

    Inputs:
        model (sklearn.svm.LinearSVC): The trained model.
        apk_features (numpy.ndarray): The feature values for the new APK.

    Returns:
        label (int): The predicted label for the new APK.
    """
    return model.predict(apk_features)


def plotting(y_pred, y_test):
    print('y_pred', y_pred)
    print('y_test', y_test)
    plt.plot(y_pred, "r", label="predicted")
    plt.plot(y_test, "b", label="expected")
    plt.show()


def main():
    """"
     This is the main function that executes the entire process of loading the data, preprocessing it, 
     training a model, and evaluating its performance. It also allows for the classification of a new APK.

    Inputs:
        None.
    Returns:
        None.
    """
    path = config['apksResultJsonPath']

    # Load data
    df = load_data(path)
    df = df.rename(columns={'label': 'class'})

    # Split data into features and labels
    X = df.drop(columns=['class'])
    y = df['class']

    # Preprocess data
    X_scaled, y_encoded = preprocess_data(X, y)

    # Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y_encoded, test_size=0.2, shuffle=True)

    # Train model
    model = train_model(X_train, y_train, C=1.0, epsilon=1e-3)
    # Evaluate model

    accuracy, precision, recall = evaluate_model(model, X_test, y_test)
    print(f'Accuracy: {accuracy:.3f}')
    print(f'Precision: {precision:.3f}')
    print(f'Recall: {recall:.3f}')


if __name__ == '__main__':
    main()
