import numpy as np
import matplotlib.pyplot as plt
from keras.models import load_model
from ela import convert_to_ela_image


def prepare_image(fname):
    image_size = (128, 128)
    return (
        np.array(convert_to_ela_image(fname[0], 90).resize(image_size)).flatten()
        / 255.0
    )  # return ela_image as a numpy array


def predict_result(fname):
    model = load_model("trained_model.h5")  # load the trained model
    class_names = ["Forged", "Authentic"]  # classification outputs
    test_image = prepare_image(fname)
    test_image = test_image.reshape(-1, 128, 128, 3)

    y_pred = model.predict(test_image)
    y_pred_class = round(y_pred[0][0])

    prediction = class_names[y_pred_class]
    if y_pred <= 0.5:
        confidence = f"{(1-(y_pred[0][0])) * 100:0.2f}"
    else:
        confidence = f"{(y_pred[0][0]) * 100:0.2f}"
    return (prediction, confidence)


def plot_loss(history):
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Model Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()


def plot_accuracy(history):
    plt.plot(history.history['accuracy'], label='Training Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.title('Model Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.show()


def evaluate_model(model, X_test, y_test):
    test_loss, test_accuracy = model.evaluate(X_test, y_test)
    print(f'Test Loss: {test_loss:.4f}')
    print(f'Test Accuracy: {test_accuracy:.4f}')
