from flask import Blueprint, render_template, request, redirect, url_for, send_file, flash, jsonify, request
import requests
from werkzeug.utils import secure_filename
import os
from app.optimalPath import ImageSeg, OptimalPathing
import cv2

# Initialize the Blueprint
main = Blueprint('main', __name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



# Example route
@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html')


@main.route('/object_detection')
def object_detection():
    return render_template('tree_count.html')


@main.route('/object_segmentation')
def object_segmentation():
    return render_template('object_segmentation.html')



@main.route('/tree_species')
def tree_species():
    return render_template('tree_species.html')


@main.route('/optimal_path')
def optimal_path():
    return render_template('optimal_path.html')


@main.route('/historical_data')
def historical_data():
    return render_template('weather.html')

@main.route('/about')
def about():
    return "About Us"

@main.route('/predict')
def predict():
    return render_template('predict.html')


@main.route('/upload', methods=['GET','POST'])
def upload_image():
    result_path = []
    if 'file' not in request.files:
        flash('No file part')
        return render_template('optimal_path.html')

    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return render_template('optimal_path.html')
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Save the uploaded file to the upload folder
        upload_folder = os.path.join(os.getcwd(), UPLOAD_FOLDER)
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)

        # Process the uploaded image using ImageSeg and OptimalPathing classes
        image_processor = ImageSeg(file_path)
        thresholded_image = image_processor.IsoGrayThresh()
        optimal_path_processor = OptimalPathing(thresholded_image,file_path)
        buffer_image, processed_image = optimal_path_processor.ComputeAStar()

        # Save the processed images to the upload folder
        processed_image_path = os.path.join(upload_folder, 'processed_image.png')
        cv2.imwrite(processed_image_path, processed_image)

        # Save the buffer image
        buffer_image_path = os.path.join(upload_folder, 'buffer_image.png')
        with open(buffer_image_path, 'wb') as f:
            f.write(buffer_image.getbuffer())

        # Render the template with processed images
        return render_template('optimal_path.html',
                            processed_image=url_for('UPLOADS', filename='processed_image.png'),
                            buffer_image=url_for('UPLOADS', filename='buffer_image.png'))



@main.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({'error': 'City parameter is required'}), 400

    api_url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?unitGroup=us&key=NBRQYJ66AF3C6NLHLBJZ3SDYT&contentType=json"

    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an error for bad status codes (e.g., 404, 500)
        data = response.json()
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Failed to fetch data: {str(e)}'}), 500