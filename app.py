from flask import Flask, request, jsonify, redirect, render_template
from url_store import URLStore
import os

app = Flask(__name__)
store = URLStore()

# Configuração básica
app.config['BASE_URL'] = os.environ.get('BASE_URL', 'https://urlshortener-sldd.onrender.com/')

@app.route('/', methods=['GET'])
def index():
    """Rota principal que serve o frontend"""
    return render_template('index.html', base_url=app.config['BASE_URL'])

@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    """API para encurtar URLs"""
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'Missing URL parameter'}), 400
    
    long_url = data['url']
    if not long_url.startswith(('http://', 'https://')):
        return jsonify({'error': 'Invalid URL - must start with http:// or https://'}), 400
    
    key = store.add_url(long_url)
    short_url = f"{app.config['BASE_URL']}/{key}"
    
    return jsonify({
        'key': key,
        'long_url': long_url,
        'short_url': short_url
    }), 201

@app.route('/<key>', methods=['GET'])
def redirect_to_long_url(key):
    """Redireciona para a URL original"""
    long_url = store.get_url(key)
    if long_url:
        return redirect(long_url, code=302)
    return jsonify({'error': 'URL not found'}), 404

@app.route('/api/url/<key>', methods=['DELETE'])
def delete_url(key):
    """Remove uma URL encurtada"""
    if store.delete_url(key):
        return '', 200
    return jsonify({'error': 'URL not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
