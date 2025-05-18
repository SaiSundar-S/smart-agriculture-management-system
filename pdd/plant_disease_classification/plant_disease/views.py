from django.shortcuts import render
import numpy as np
import tensorflow as tf
import os
import json
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.applications.vgg16 import preprocess_input

# Load class indices
with open('E:\SAMS\pdd\plant_disease_classification\class_indices.json', 'r') as f:
    class_indices = json.load(f)

# Load TensorFlow Lite model and initialize the interpreter
model_path = r"E:\SAMS\pdd\plant_disease_classification\model.tflite"
interpreter = tf.lite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()

# Get model input details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def preprocess_image(image_path, target_size=(224, 224)):
    """Preprocess image before feeding it to the model."""
    img = load_img(image_path, target_size=target_size)
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0  # Normalize image
    return img_array

def predict_disease(request):
    if request.method == 'POST' and request.FILES['image']:
        image = request.FILES['image']
        image_path = os.path.join('media', 'uploads', image.name)

        # Create directories if they don't exist
        os.makedirs(os.path.dirname(image_path), exist_ok=True)

        # Save uploaded image
        with open(image_path, 'wb+') as dest:
            for chunk in image.chunks():
                dest.write(chunk)

        # Preprocess the image for prediction
        img_array = preprocess_image(image_path)

        # Set the input tensor for the interpreter
        interpreter.set_tensor(input_details[0]['index'], img_array)

        # Run inference
        interpreter.invoke()
        prediction = interpreter.get_tensor(output_details[0]['index'])
        
        # Get the predicted class
        predicted_class = np.argmax(prediction)

        # Map predicted class index to label
        predicted_label = class_indices.get(str(predicted_class), "Unknown")

        # Generate the URL for the image to display in the template
        image_url = f'/media/uploads/{image.name}'

        # Return the prediction result along with the image URL
        return render(request, 'plant_disease/result.html', {
            'predicted_label': predicted_label,
            'image_url': image_url
        })

    return render(request, 'plant_disease/index.html')


def index(request):
    return render(request, 'plant_disease/index.html')
