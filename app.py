from flask import Flask, render_template, request, jsonify, session
import random
import string

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Generate a random CAPTCHA text
def generate_captcha_text():
    captcha_length = 5
    characters = string.ascii_letters + string.digits
    captcha_text = ''.join(random.choice(characters) for _ in range(captcha_length))
    return captcha_text

# Store the CAPTCHA text in session for verification
@app.route('/')
def index():
    captcha_text = generate_captcha_text()
    session['captcha_text'] = captcha_text
    return render_template('index.html', captcha_text=captcha_text)

# Handle the CAPTCHA verification logic
@app.route('/verify', methods=['POST'])
def verify():
    captcha_input = request.form.get('captcha_input')
    stored_captcha = session.get('captcha_text')

    if captcha_input == stored_captcha:
        response = {'status': 'success', 'message': 'CAPTCHA verification successful!'}
        new_captcha_text = generate_captcha_text()
        session['captcha_text'] = new_captcha_text
        response['new_captcha_text'] = new_captcha_text
    else:
        response = {'status': 'error', 'message': 'CAPTCHA verification failed!'}

    return jsonify(response)

# Regenerate a new CAPTCHA text 
@app.route('/regenerate', methods=['GET'])
def regenerate():
    new_captcha_text = generate_captcha_text()
    session['captcha_text'] = new_captcha_text
    return jsonify({'new_captcha_text': new_captcha_text})

if __name__ == '__main__':
    app.run(debug=True)
