from flask import Flask, render_template, request, jsonify
import requests
import sqlite3

app = Flask(__name__)

API_KEY = 'KHZ9nMOb8Ukyp7vnwwYuszqsG4jePJzQ'
GIPHY_URL = 'https://api.giphy.com/v1/gifs/search'

def init_db():
    conn = sqlite3.connect('gifs.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS gif_interactions
                 (id TEXT PRIMARY KEY, title TEXT, url TEXT, views INTEGER, clicks INTEGER)''')
    conn.commit()
    conn.close()

def track_interaction(gif_id, title, url, interaction_type):
    conn = sqlite3.connect('gifs.db')
    c = conn.cursor()
    c.execute('SELECT * FROM gif_interactions WHERE id = ?', (gif_id,))
    gif = c.fetchone()

    if gif:
        if interaction_type == 'view':
            c.execute('UPDATE gif_interactions SET views = views + 1 WHERE id = ?', (gif_id,))
        elif interaction_type == 'click':
            c.execute('UPDATE gif_interactions SET clicks = clicks + 1 WHERE id = ?', (gif_id,))
    else:
        c.execute('INSERT INTO gif_interactions (id, title, url, views, clicks) VALUES (?, ?, ?, ?, ?)',
                  (gif_id, title, url, 1 if interaction_type == 'view' else 0, 1 if interaction_type == 'click' else 0))
    
    conn.commit()
    conn.close()

def fetch_gifs(query):
    params = {
        'q': query,
        'api_key': API_KEY,
        'limit': 12
    }
    response = requests.get(GIPHY_URL, params=params)
    gifs = response.json().get('data', [])

    conn = sqlite3.connect('gifs.db')
    c = conn.cursor()

    for gif in gifs:
        gif_id = gif.get('id')
        title = gif.get('title', '')
        url = gif.get('images', {}).get('downsized', {}).get('url', '')
        track_interaction(gif_id, title, url, 'view')

    c.execute('SELECT * FROM gif_interactions ORDER BY views DESC, clicks DESC')
    ranked_gifs = c.fetchall()
    conn.close()

    ranked_gifs_with_rank = []
    for rank, gif in enumerate(ranked_gifs, start=1):
        ranked_gifs_with_rank.append({
            'rank': rank,
            'id': gif[0],
            'title': gif[1],
            'url': gif[2],
            'views': gif[3],
            'clicks': gif[4]
        })

    return ranked_gifs_with_rank

@app.route('/', methods=['GET', 'POST'])
def index():
    gifs = []
    if request.method == 'POST':
        query = request.form['query']
        gifs = fetch_gifs(query)
    return render_template('index.html', gifs=gifs)

@app.route('/click/<gif_id>')
def click(gif_id):
    conn = sqlite3.connect('gifs.db')
    c = conn.cursor()
    c.execute('SELECT * FROM gif_interactions WHERE id = ?', (gif_id,))
    gif = c.fetchone()
    if gif:
        track_interaction(gif_id, gif[1], gif[2], 'click')
    conn.close()
    return 'GIF clicked!'

@app.route('/search', methods=['GET'])
def search_gifs():
    search_term = request.args.get('q', '')
    if not search_term:
        return jsonify({'error': 'Search term is required'}), 400

    params = {
        'q': search_term,
        'api_key': API_KEY,
        'limit': 24
    }
    try:
        response = requests.get(GIPHY_URL, params=params)
        response.raise_for_status()
        gifs = response.json().get('data', [])

        if not gifs:
            return jsonify({'message': 'No GIFs found'}), 404

        sorted_gifs = sorted(gifs, key=lambda x: (x.get('views', 0), x.get('clicks', 0)), reverse=True)
        return jsonify({'gifs': sorted_gifs})
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
