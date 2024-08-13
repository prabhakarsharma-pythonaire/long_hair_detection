import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Load the models
hair_length_model = load_model('hair_length_model.h5')
gender_classification_model = load_model('gender_classification_model.h5')
age_model = load_model('age_prediction_model.h5')

# Define the prediction function
def predict_age_hair_gender(image):
    img_resized = cv2.resize(image, (64, 64))
    img_normalized = img_resized / 255.0
    img_normalized = np.expand_dims(img_normalized, axis=0)  # Add batch dimension

    predicted_age = age_model.predict(img_normalized)[0][0]

    if 20 <= predicted_age <= 30:
        predicted_hair_label = hair_length_model.predict(img_normalized)[0][0]
        gender = 'Male' if predicted_hair_label < 0.5 else 'Female'
        hair_length = 'Short' if predicted_hair_label < 0.5 else 'Long'
    else:
        predicted_gender_label = gender_classification_model.predict(img_normalized)[0][0]
        gender = 'Male' if predicted_gender_label < 0.5 else 'Female'
        hair_length = 'N/A'

    return {
        'Predicted Age': predicted_age,
        'Gender': gender,
        'Hair Length': hair_length
    }

# Create the GUI
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Prediction")
        self.root.geometry("600x400")  # Set the window size to 600x400 pixels

        # Set the window icon
        self.set_icon("OIP.jpeg")

        # Add a title label for "Long Hair Detection"
        self.title_label = tk.Label(root, text="Long Hair Detection", font=("Arial", 24, "bold"), fg="blue")
        self.title_label.pack(pady=20)  # Add some vertical padding for spacing

        # Add a description or instruction label
        self.label = tk.Label(root, text="Upload an image to predict age, gender, and hair length", font=("Arial", 12))
        self.label.pack(pady=10)

        # Upload button
        self.upload_btn = tk.Button(root, text="Upload Image", command=self.upload_image, font=("Arial", 12))
        self.upload_btn.pack(pady=10)

        # Label to display prediction results
        self.result_label = tk.Label(root, text="", font=("Arial", 14))
        self.result_label.pack(pady=20)

    def set_icon(self, icon_path):
        # Load the image
        icon_image = Image.open(icon_path)
        icon_photo = ImageTk.PhotoImage(icon_image)
        # Set the window icon
        self.root.iconphoto(True, icon_photo)

    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                image = cv2.imread(file_path)
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                
                results = predict_age_hair_gender(image_rgb)
                
                result_text = f"Predicted Age: {results['Predicted Age']:.2f} years\n" \
                              f"Gender: {results['Gender']}\n" \
                              f"Hair Length: {results['Hair Length']}"
                self.result_label.config(text=result_text)
            except Exception as e:
                messagebox.showerror("Error", "Failed to process the image.")
                print(f"Exception occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
