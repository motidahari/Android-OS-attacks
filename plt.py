import matplotlib.pyplot as plt
def plotting(y_pred, y_test):
    plt.plot(y_pred, "r", label="predicted")
    plt.plot(y_test, "b", label="expected")
    plt.show()
