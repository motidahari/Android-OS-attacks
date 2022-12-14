from sklearn.model_selection import train_test_split
from setting import config
from utils import get_random_number, load_data, count_apps
from classification_utils import preprocess_data
from classification import train_model, evaluate_model
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
# need to
global c_val, epsilon_val, test_size_val, random_state_val
global c_val_max, epsilon_val_max, random_state_val_max
global accuracy_max, precision_max, recall_max
global num_benign_apps, num_malicious_apps


def initialization(malicious_count, benign_count):
    test_size_val = 0.1  # Static 0.1
    c_val = 0.021  # 1.0
    epsilon_val = 1e-3

    random_state_val = 0
    c_val_max = 0
    epsilon_val_max = 0
    test_size_val_max = 0
    random_state_val_max = random_state_val

    accuracy_max = 0
    precision_max = 0
    recall_max = 0
    return test_size_val, c_val, epsilon_val, random_state_val,\
        c_val_max, epsilon_val_max, test_size_val_max,\
        random_state_val_max, accuracy_max, precision_max, recall_max


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
    df, malicious_count, benign_count = load_data(
        path)

    df = df.rename(columns={'label': 'class'})

    # Split data into features and labels
    X = df.drop(columns=['class'])
    y = df['class']

    test_size_val, c_val, epsilon_val, random_state_val,\
        c_val_max, epsilon_val_max, test_size_val_max,\
        random_state_val_max, accuracy_max, precision_max, recall_max = initialization(
            malicious_count, benign_count)

    # Preprocess data
    X_scaled, y_encoded = preprocess_data(X, y)

    # Optimization for results
    # for x in range(1, 100):

    #     # Random c and epsilon and test_size
    #     test_size_val = get_random_number(0, 1, isInt=False)  # Static 0.1
    #     c_val = get_random_number(1, 100)
    #     epsilon_val = get_random_number(0, 1, isInt=False)

    # Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y_encoded, test_size=test_size_val, shuffle=True)

    # Train model
    model = train_model(X_train, y_train, C=c_val,
                        epsilon=epsilon_val, random_state_val=random_state_val)

    # Evaluate model
    accuracy, precision, recall = evaluate_model(model, X_test, y_test)
    if (accuracy + precision + recall > accuracy_max + precision_max + recall_max):
        c_val_max = c_val
        accuracy_max = accuracy
        precision_max = precision
        recall_max = recall
        epsilon_val_max = epsilon_val
        test_size_val_max = test_size_val
        print(f'c_val_max: {c_val_max:.3f}')
        print(f'epsilon_val_max: {epsilon_val_max:.10f}')
        print(f'test_size_val_max: {test_size_val_max:.3f}')
        print(f'accuracy_max: {accuracy_max:.3f}')
        print(f'precision_max: {precision_max:.3f}')
        print(f'recall_max: {recall_max:.3f}')
        print(f'Evaluate new model data and searching for a better results...')
        print()

    print(f' ******************************** Results ********************************')
    print(f'Results:')
    print(f'c_val_max: {c_val_max:.3f}')
    print(f'epsilon_val_max: {epsilon_val_max:.10f}')
    print(f'test_size_val_max: {test_size_val_max:.3f}')
    print(f'accuracy_max: {accuracy_max:.3f}')
    print(f'precision_max: {precision_max:.3f}')
    print(f'recall_max: {recall_max:.3f}')
    print(f'Accuracy: {accuracy:.3f}')
    print(f'Precision: {precision:.3f}')
    print(f'Recall: {recall:.3f}')


if __name__ == '__main__':
    main()
