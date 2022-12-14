from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.svm import LinearSVC
from plt import plotting
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


def train_model(X_train, y_train, C, epsilon, random_state_val):
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
    model = LinearSVC(C=C, random_state=random_state_val, tol=epsilon)
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
    # plotting(y_pred[:100], y_test[:100])

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
