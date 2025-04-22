import os
import secrets
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import replicate
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['RESULT_FOLDER'] = 'static/results'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# Create directories if they don't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if a file was uploaded
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    
    # If the user does not select a file, the browser submits an empty file
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Generate filename and path for the result
        result_filename = f"result_{filename}"
        result_path = os.path.join(app.config['RESULT_FOLDER'], result_filename)
        # Process and save the AI-generated headshot
        try:
            process_image(filepath, result_path)
            return render_template('result.html',
                                   original=url_for('static', filename=f'uploads/{filename}'),
                                   result=url_for('static', filename=f'results/{result_filename}'))
        except Exception as e:
            flash(f'Error processing image: {str(e)}')
            return redirect(url_for('index'))
    
    flash('Invalid file type. Please upload a PNG or JPEG image.')
    return redirect(url_for('index'))

def process_image(input_path, output_path):
    """
    Process the uploaded image using Replicate API to generate a professional headshot
    """
    # Call the Replicate API to generate the headshot
    output = replicate.run(
        "catacolabs/headshot-fine-tuned:9aa09f993ddc95d22faca0e64a71c3c9392c6a3cc3e14bf292f6cee08506978d",
        input={
            "image": open(input_path, "rb"),
            "mode": "professional",
            "num_samples": 1
        }
    )
    # Determine the result URL from the Replicate output
    image_url = output[0] if isinstance(output, list) else output
    # Download the generated image and save to the output path
    response = requests.get(image_url)
    response.raise_for_status()
    with open(output_path, "wb") as f:
        f.write(response.content)
    return output_path

if __name__ == '__main__':
    app.run(debug=True) 