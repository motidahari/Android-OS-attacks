import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score
import json
from setting import config


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


def train_model(X_train, y_train):
    """
        This function trains a random forest classifier model on the input training data.

    Inputs:
        X_train (numpy.ndarray): The feature values for the training data.
        y_train (numpy.ndarray): The labels for the training data.

    Returns:
        model (sklearn.ensemble.RandomForestClassifier): The trained random forest model.
    """
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    return model


def evaluate_model(model, X_test, y_test):
    """
        This function evaluates a model's performance on the test data by computing the accuracy, precision, and recall scores.

    Inputs:
        model (sklearn.ensemble.RandomForestClassifier): The model to be evaluated.
        X_test (numpy.ndarray): The feature values for the test data.
        y_test (numpy.ndarray): The labels for the test data.

    Returns:
        accuracy (float): The model's accuracy score.
        precision (float): The model's precision score.
        recall (float): The model's recall score.
    """
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    return accuracy, precision, recall


def classify_apk(model, apk_features):
    """
        This function makes a prediction for a new APK by using the trained model to classify the APK based on its features.

    Inputs:
        model (sklearn.ensemble.RandomForestClassifier): The trained model.
        apk_features (numpy.ndarray): The feature values for the new APK.

    Returns:
        label (int): The predicted label for the new APK.
    """
    return model.predict(apk_features)


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

    # Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        df.drop('label', axis=1), df['label'], test_size=0.2)

    # Preprocess data
    X_train, y_train = preprocess_data(X_train, y_train)
    X_test, y_test = preprocess_data(X_test, y_test)
    # print('X_train', X_train)
    # print('y_train', y_train)
    # print('X_test', X_test)
    # print('y_test', y_test)

    # Write labels to a JSON file

    # Train model
    model = train_model(X_train, y_train)

    # # Evaluate model
    accuracy, precision, recall = evaluate_model(model, X_test, y_test)
    print(f'Accuracy: {accuracy:.2f}')
    print(f'Precision: {precision:.2f}')
    print(f'Recall: {recall:.2f}')

    # Classify new APK
    # Placeholder for actual APK features
    new_apk_features = [[2.0, 3.0, 4.0, 5.0]]
    label = classify_apk(model, new_apk_features)
    print(f'Label for new APK: {label}')


if __name__ == '__main__':
    main()