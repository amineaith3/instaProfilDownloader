from flask import Flask, request, render_template, url_for
import instaloader
import os
from datetime import datetime

app = Flask(__name__)

def download_profile_picture(username):
    try:
        loader = instaloader.Instaloader()
        profile = instaloader.Profile.from_username(loader.context, username)
        image_url = profile.profile_pic_url
        username = 'jpg/' + username
        image_path = os.path.join('static', username)
        loader.download_pic(image_path, image_url, mtime=datetime.now())
        return username
    except instaloader.exceptions.ProfileNotExistsException:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    image_filename = None
    if request.method == 'POST':
        username = request.form['username']
        image_filename = download_profile_picture(username)
        if image_filename:
            image_url = url_for('static', filename=image_filename) + '.jpg'
        else:
            image_url = None
    else:
        image_url = None

    return render_template('index.html', image_url=image_url)


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

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html'), 500


TEMP_DIR = 'static/jpg'

@app.before_request
def cleanup():
    if request.method == 'POST':
        if not os.path.exists(TEMP_DIR):
            os.makedirs(TEMP_DIR)
        # Delete all images in the temp directory before each GET request
        for filename in os.listdir(TEMP_DIR):
            file_path = os.path.join(TEMP_DIR, filename)
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")



if __name__ == '__main__':
    if not os.path.exists('static'):
        os.makedirs('static')
    app.run(debug=True)
