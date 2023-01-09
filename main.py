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
def train_model(X_train, y_train, C, wlb, wub, sample_size, initial_step_size, decay_function, epsilon):
    """
        This function trains a Sec-SVM classifier model on the input training data.

    Inputs:
        X_train (numpy.ndarray): The feature values for the training data.
        y_train (numpy.ndarray): The labels for the training data.
        C (float): The regularization parameter.
        wlb (float): The lower bound on the weights.
        wub (float): The upper bound on the weights.
        sample_size (int): The size of the sample subset used to approximate the subgradients.
        initial_step_size (float): The initial gradient step size.
        decay_function (function): A function that decays the step size over time.
        epsilon (float): A small constant used to determine when to stop the training.

    Returns:
        model (sklearn.svm.LinearSVC): The trained Sec-SVM model.
    """
    # Initialize the model
    model = LinearSVC(C=C, random_state=0, tol=epsilon)
    
    # Initialize the iteration count
    t = 0
    
    # Initialize the model parameters
    v = (np.random.uniform(wlb, wub, len(X_train[0])), np.random.uniform(wlb, wub))
    
    # Compute the objective function using Eq. (7)
    L = compute_objective_function(v, X_train, y_train, C)
    
    while True:
        # Compute the subgradients using Eqs. (9) and (10)
        subgrad_w, subgrad_b = compute_subgradients(v, X_train, y_train, C, sample_size)
        
        # Increment the iteration count
        t += 1
        
        # Compute the gradient step size using the decay function and the initial step size
        step_size = decay_function(initial_step_size, t)
        
        # Update the weights
        w = v[0] - step_size * subgrad_w
        w = np.clip(w, wlb, wub)  # Project onto the feasible (box) domain
        
        # Update the bias term
        b = v[1] - step_size * subgrad_b
        
        # Update the model parameters
        v = (w, b)
        
        # Compute the objective function using Eq. (7)
        L_new = compute_objective_function(v, X_train, y_train, C)
        
        # Check if the difference in the objective function values is below the threshold
        if abs(L - L_new) < epsilon:
            break
        
        L = L_new
    
    # Set the model parameters
    model.coef_ = w
    model.intercept_ = b
    
    return model

def evaluate_model(model, X_test, y_test):
    """
        This function evaluates a model's performance on the test data by computing the accuracy, precision, and recall scores.

    Inputs:
        model (sklearn.svm.LinearSVC): The model to be evaluated.
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
        model (sklearn.svm.LinearSVC): The trained model.
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

    # Split data into features and labels
    X = df.drop(columns=['class'])
    y = df['class']

    # Preprocess data
    X_scaled, y_encoded = preprocess_data(X, y)

    # Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_encoded, test_size=0.2)

    # Train model
    model = train_model(X_train, y_train, C=1.0, wlb=-1.0, wub=1.0, sample_size=1000, initial_step_size=0.1, decay_function=lambda x, t: x / (1 + t), epsilon=1e-3)

    # Evaluate model
    accuracy, precision, recall = evaluate_model(model, X_test, y_test)
    print(f'Accuracy: {accuracy:.3f}')
    print(f'Precision: {precision:.3f}')
    print(f'Recall: {recall:.3f}')

    # Classify new APK
    apk_features = np.array([[1.0, 0.5]])
    label = classify_apk(model, apk_features)
    print(f'Predicted label for new APK: {label}')

if __name__ == '__main__':
    main()