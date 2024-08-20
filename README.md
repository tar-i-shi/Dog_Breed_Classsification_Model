# Dog_Breed_Classsification_Model

Overview

This project is a web-based application (majorly backend + little frontend) that classifies dog breeds using a deep learning model. The application allows users to upload an image of a dog, and the model predicts the breed. The project is built using Python, TensorFlow, Flask, and HTML/CSS for the web interface.

It handle following routes -

1. GET  /model : Retrieve information about the model.
   
2. POST /img : Accept a image and returns a JSON response as follows
{
"category": "labrador",
"uid": "1519151980"
}

3. GET /images : Return all the uploaded images along with its UIDs.
{
{
"uid": "6569841",
"type": "labrador"
},
}

4. POST /img/{uid} : Download the image that matches the UID.

5. GET /categories : All the categories that were created along with the number of
images in each category. Below is the response
{
"labrador" : "2",
"bulldog": "12",
}


Dataset used for creating this project - 
https://www.kaggle.com/datasets/jessicali9530/stanford-dogs-dataset. 

To set up and run the project locally, follow these steps:

1. Download the Repository

   Download all the folders and files included in this repository.

2. Run the Jupyter Notebook

   Open the 80.5.ipynb file in your Jupyter Notebook environment. Ensure you replace the dataset path with the correct path on your system.

3. Start the Flask Application

   Open the Anaconda prompt, navigate to your project's folder, and run the following command:
   'python app.py'
   
4. Access the Website

   After running the command, open your web browser and access the website through the URL displayed in the terminal.

Directory Structure 

|-- app.py            # Flask application file

|-- 80.5.ipynb        # Jupyter Notebook for training and testing the model

|-- templates/        # HTML templates for the web interface

|-- uploads/          # Folder for uploaded images

|-- 80.5.h5           # Trained model file
