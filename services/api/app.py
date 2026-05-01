from flask import Flask, request, jsonify
import redis, hashlib, os

app = Flask(__name__)
r = redis.Redis(
    host=os.getenv('REDIS_HOST', 'redis'),
    port=6379, decode_responses=True
)

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'version': 'v2', 'author': 'kunal'})

@app.route('/shorten', methods=['POST'])
def shorten():
    url = request.json['url']
    code = hashlib.md5(url.encode()).hexdigest()[:6]
    r.set(code, url)
    return jsonify({'short_code': code, 'url': f'/r/{code}'})

@app.route('/r/<code>')
def resolve(code):
    url = r.get(code)
    if url:
        return jsonify({'original_url': url})
    return jsonify({'error': 'not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
