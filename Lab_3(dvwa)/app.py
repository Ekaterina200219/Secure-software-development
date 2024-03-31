from flask import Flask, request, render_template, session, redirect, url_for
from captcha.image import ImageCaptcha
import random
import string
import base64
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'secretkey'

base = {
    'user1': 'password1',
    'user2': 'password2'
}

def generate_captcha():
    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    image = ImageCaptcha()
    data = BytesIO()
    image.write(captcha_text, data)
    data.seek(0)
    return captcha_text, base64.b64encode(data.getvalue()).decode('utf-8')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_captcha = request.form['captcha']

        if username in base and base[username] == password and user_captcha == session['captcha']:
            return redirect(url_for('success', message='Авторизация успешна'))
        else:
            return redirect(url_for('login', message='Неправильный логин, пароль или капча'))
    else:
        captcha_text, captcha_image = generate_captcha()
        session['captcha'] = captcha_text
        message = request.args.get('message', '')
        return render_template('site.html', captcha_text=captcha_text, captcha_image=captcha_image, message=message)


@app.route('/success')
def success():
    message = request.args.get('message', '')  
    return render_template('success.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)
