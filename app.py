from flask import Flask, request, render_template, url_for
import instaloader
import base64
from io import BytesIO
from datetime import datetime
from PIL import Image
from instaloader.exceptions import ProfileNotExistsException, ConnectionException
import requests

app = Flask(__name__)

def download_profile_picture(username):
    try:
        loader = instaloader.Instaloader()
        profile = instaloader.Profile.from_username(loader.context, username)
        image_url = profile.profile_pic_url
        
        # Download the image
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
        
        # Convert the image to a base64 string
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return img_str
    except ProfileNotExistsException:
        return None
    except ConnectionException:
        return "Connection error"

@app.route('/', methods=['GET', 'POST'])
def index():
    image_data = None
    error_message = None  # Variable to store error messages
    if request.method == 'POST':
        username = request.form['username']
        image_data = download_profile_picture(username)
        if image_data == "Connection error":
            error_message = "Could not connect to Instagram. Please try again later."
            image_data = None
        elif image_data is None:
            error_message = "The specified username does not exist."
    return render_template('index.html', image_data=image_data, error_message=error_message)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# Error handler for 500 Internal Server Error
@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html'), 500

# Error handler for ConnectionException
@app.errorhandler(ConnectionException)
def handle_connection_exception(error):
    return render_template('error.html', message="Connection error. Please try again later."), 500

if __name__ == '__main__':
    app.run(debug=True)
