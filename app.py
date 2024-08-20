from flask import Flask, request, jsonify, send_file, redirect, url_for, render_template
import os
from werkzeug.utils import secure_filename
import uuid
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Allowed file extensions for upload
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Load the model
try:
    model = load_model('C:\\Users\\taris\\Dog Breed Classification\\80.5.h5')
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def predict_image(img_path):
    if model is None:
        return "Model is not loaded", 500
    
    try:
        img = image.load_img(img_path, target_size=(299, 299,3))  # Ensure target size matches model input size
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0

        predictions = model.predict(img_array)
        # Assuming predictions is an array of probabilities for each class
        predicted_class_index = np.argmax(predictions[0])
        
        # List of class names corresponding to model output indices
        class_names = [
            'Afghan_hound', 'African_hunting_dog', 'Airedale', 'American_Staffordshire_terrier',
            'Appenzeller', 'Australian_terrier', 'Bedlington_terrier', 'Bernese_mountain_dog',
            'Blenheim_spaniel', 'Border_collie', 'Border_terrier', 'Boston_bull', 'Bouvier_des_Flandres',
            'Brabancon_griffon', 'Brittany_spaniel', 'Cardigan', 'Chesapeake_Bay_retriever', 'Chihuahua',
            'Dandie_Dinmont', 'Doberman', 'English_foxhound', 'English_setter', 'English_springer',
            'EntleBucher', 'Eskimo_dog', 'French_bulldog', 'German_shepherd', 'German_short-haired_pointer',
            'Gordon_setter', 'Great_Dane', 'Great_Pyrenees', 'Greater_Swiss_Mountain_dog', 'Ibizan_hound',
            'Irish_setter', 'Irish_terrier', 'Irish_water_spaniel', 'Irish_wolfhound', 'Italian_greyhound',
            'Japanese_spaniel', 'Kerry_blue_terrier', 'Labrador_retriever', 'Lakeland_terrier', 'Leonberg',
            'Lhasa', 'Maltese_dog', 'Mexican_hairless', 'Newfoundland', 'Norfolk_terrier', 'Norwegian_elkhound',
            'Norwich_terrier', 'Old_English_sheepdog', 'Pekinese', 'Pembroke', 'Pomeranian', 'Rhodesian_ridgeback',
            'Rottweiler', 'Saint_Bernard', 'Saluki', 'Samoyed', 'Scotch_terrier', 'Scottish_deerhound',
            'Sealyham_terrier', 'Shetland_sheepdog', 'Shih-Tzu', 'Siberian_husky', 'Staffordshire_bullterrier',
            'Sussex_spaniel', 'Tibetan_mastiff', 'Tibetan_terrier', 'Walker_hound', 'Weimaraner',
            'Welsh_springer_spaniel', 'West_Highland_white_terrier', 'Yorkshire_terrier', 'affenpinscher',
            'basenji', 'basset', 'beagle', 'black-and-tan_coonhound', 'bloodhound', 'bluetick', 'borzoi',
            'boxer', 'briard', 'bull_mastiff', 'cairn', 'chow', 'clumber', 'cocker_spaniel', 'collie',
            'curly-coated_retriever', 'dhole', 'dingo', 'flat-coated_retriever', 'giant_schnauzer',
            'golden_retriever', 'groenendael', 'keeshond', 'kelpie', 'komondor', 'kuvasz', 'malamute',
            'malinois', 'miniature_pinscher', 'miniature_poodle', 'miniature_schnauzer', 'otterhound',
            'papillon', 'pug', 'redbone', 'schipperke', 'silky_terrier', 'soft-coated_wheaten_terrier',
            'standard_poodle', 'standard_schnauzer', 'toy_poodle', 'toy_terrier', 'vizsla', 'whippet',
            'wire-haired_fox_terrier'
        ]
        
        predicted_category_name = class_names[predicted_class_index]
        
        return predicted_category_name, None  # Return predicted category name and None for error
    
    except Exception as e:
        return None, str(e)


def generate_uid():
    return str(uuid.uuid4().int)[:10]

images = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/model', methods=['GET'])
def get_model_info():
    if model:
        return jsonify({"model": "Your model name or details here"})
    else:
        return jsonify({"error": "Model not loaded"}), 500

@app.route('/img', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        category, error = predict_image(filepath)
        if error:
            return jsonify({"error": error}), 500
        
        uid = generate_uid()
        images.append({"uid": uid, "category": category, "filepath": filepath})

        return render_template('result.html', category=category, uid=uid)
    else:
        return jsonify({"error": "Invalid file type"}), 400

@app.route('/images', methods=['GET'])
def get_images():
    return jsonify(images)

@app.route('/img/<uid>', methods=['GET'])
def download_image(uid):
    image_entry = next((img for img in images if img['uid'] == uid), None)
    if image_entry:
        return send_file(image_entry['filepath'], as_attachment=True)
    return jsonify({"error": "Image not found"}), 404

@app.route('/categories', methods=['GET'])
def get_categories():
    category_counts = {}
    for img in images:
        category = img['category']
        if category in category_counts:
            category_counts[category] += 1
        else:
            category_counts[category] = 1
    return jsonify(category_counts)

if __name__ == "__main__":
    app.run(debug=True)
