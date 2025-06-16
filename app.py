from flask import Flask, request, jsonify, redirect, render_template
import hashlib

app = Flask(__name__)
url_db = {}

def generate_short_code(url):
    return hashlib.sha256(url.encode()).hexdigest()[:6]

@app.route('/', methods=['GET', 'POST'])
def home():
    short_url = None
    error = None

    if request.method == 'POST':
        long_url = request.form.get('url')
        if not long_url:
            error = "Campo de URL está vazio."
        else:
            short_code = generate_short_code(long_url)
            url_db[short_code] = long_url
            short_url = request.host_url + short_code  # <-- Aqui

    # Geração dinâmica no histórico também
    history = [
        {'short_code': code, 'long_url': url, 'short_url': request.host_url + code}
        for code, url in url_db.items()
    ]

    return render_template('index.html', short_url=short_url, error=error, history=history)

@app.route('/<short_code>', methods=['GET'])
def redirect_short_url(short_code):
    if short_code in url_db:
        return redirect(url_db[short_code], code=302)
    return "URL not found", 404

@app.route('/delete/<short_code>', methods=['POST'])
def delete_short_url(short_code):
    if short_code in url_db:
        del url_db[short_code]
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)