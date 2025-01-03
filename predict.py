import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image

# Load the trained model
model = tf.keras.models.load_model('Binary_CNN_Model_5')

# Function to preprocess the image
def preprocess_image(image_path):
    img = image.load_img(image_path, target_size=(256, 256))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

# Function to make predictions
def predict_image(image_path):
    img_array = preprocess_image(image_path)
    prediction = model.predict(img_array)
    print("prediction",prediction)
    if prediction[0][0] < 0.5:
        return "Creepy"
    else:
        return "Not Creepy"

# Example usage:
# image_path = '777.jpg'
def main(img):
    result = predict_image(f"D:\\01_AKHIL\\2024\\MA\\hateSpeech\\static\\test\\{img}")
    print("Prediction:", result)
    return result
