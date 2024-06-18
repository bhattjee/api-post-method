from flask import Flask, request, render_template, send_from_directory
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Set the upload folder
UPLOAD_FOLDER = '/static/uploads'  # Folder path for uploads #BUG TACKER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # Create folder if not exists

# Route to serve uploaded files
@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)  # Serve uploaded file

@app.route('/')
def index():
    return render_template('index.html')  # Render the main form

@app.route('/order', methods=['POST'])
def place_order():
    data = request.form
    if not data:
        return render_template('index.html', error='No data provided')  # Handle no data

    # Extract form data
    pizza_type = data.get('pizza_type')
    size = data.get('size')
    toppings = data.getlist('toppings')
    address = data.get('address')
    phone = data.get('phone')

    # Handle file upload
    image = request.files['image']
    if image.filename == '':
        return render_template('index.html', error='No image selected')  # Handle no image

    # Save the uploaded image to the upload folder
    filename = secure_filename(image.filename)  # Secure the filename
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  # Save file

    # For demonstration, return the image filename along with other form data
    response = {
        'pizza_type': pizza_type,
        'size': size,
        'toppings': toppings,
        'address': address,
        'phone': phone,
        'image_filename': filename,
        'message': 'Order received successfully'
    }
    return render_template('index.html', response=response)  # Render response

if __name__ == '__main__':
    app.run(debug=True)  # Run the app in debug mode
