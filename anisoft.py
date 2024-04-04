import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet import preprocess_input
from tensorflow.keras.applications.mobilenet import MobileNet

# Load the pre-trained MobileNet model without the top classification layer
base_model = MobileNet(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Define a function to extract features from an image
def extract_features(img_path, model):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    features = model.predict(img_array)
    return features.flatten()

# Define a function to calculate the cosine similarity between two feature vectors
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Define a function to classify an uploaded image
def classify_uploaded_image(uploaded_image_path, test_image_folders):
    # Extract features from the uploaded image
    uploaded_image_features = extract_features(uploaded_image_path, base_model)
    
    # Loop through each animal folder
    best_similarity = -1
    best_match = None
    for animal_folder in test_image_folders:
        # Loop through each image in the animal folder
        for test_image_name in os.listdir(animal_folder):
            test_image_path = os.path.join(animal_folder, test_image_name)
            # Extract features from the test image
            test_image_features = extract_features(test_image_path, base_model)
            
            # Calculate cosine similarity between the uploaded image and the test image
            similarity = cosine_similarity(uploaded_image_features, test_image_features)
            
            # Update best match if similarity is higher
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = os.path.basename(animal_folder)
    
    return best_match

def classify_and_display():
    uploaded_image_path = filedialog.askopenfilename()
    predicted_animal = classify_uploaded_image(uploaded_image_path, test_image_folders)
    result_label.config(text="Predicted Animal: " + predicted_animal)

root = tk.Tk()
root.title("Animal Classification")

# Specify the directory containing animal folders
root_directory = 'C:\\Users\\Parthasarathi D\\OneDrive\\Desktop\\nm\\sam'
# Get a list of all directories (animal folders) in the root directory
test_image_folders = [os.path.join(root_directory, folder) for folder in os.listdir(root_directory) if os.path.isdir(os.path.join(root_directory, folder))]

browse_button = tk.Button(root, text="Browse Image", command=classify_and_display)
browse_button.pack(pady=10)

result_label = tk.Label(root, text="")
result_label.pack(pady=10)

root.mainloop()
