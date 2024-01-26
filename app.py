import sqlite3
from hashids import Hashids
from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'No one will know' # This should be a secret string


def get_db_connection():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    return conn

hashids = Hashids(min_length=4, salt=app.config['SECRET_KEY'])

@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        url = request.form['url']
        conn = get_db_connection()

        if not url:
            flash('You need to enter an URL!')
            return redirect(url_for('index'))
        
        #In order for the redirect to work it need the http in the begining of the string
        if url.find('https://') != 0 or url.find('http://') != 0:
            url = "http://" + url
        
        url_data = conn.execute('INSERT into urls (original_url) values (?)', (url,))
        conn.commit()
        conn.close()

        url_id = url_data.lastrowid
        hashid = hashids.encode(url_id)
        short_url = request.host_url + hashid

        return render_template('index.html', short_url=short_url)
    
    return render_template('index.html')

@app.route('/<id>')
def url_redirect(id):
    conn = get_db_connection()

    original_id = hashids.decode(id)
    if original_id:
        original_id = original_id[0]
        url_data = conn.execute('SELECT original_url, clicks FROM urls WHERE id = (?)', (original_id,)).fetchone()
        original_url = url_data['original_url']
        clicks = url_data['clicks']

        conn.execute('UPDATE urls SET clicks = ? WHERE id = ?',(clicks+1, original_id))
        conn.commit()
        conn.close()
        return redirect(original_url)
    else:
        flash('Not a Valid URL')
        return redirect(url_for('index'))

    
@app.route('/stats')
def stats():
    conn = get_db_connection()
    db_urls = conn.execute('SELECT id, created, original_url, clicks FROM urls').fetchall()
    conn.close()
    urls = []
    for url in db_urls:
        url = dict(url)
        url['short_url'] = request.host_url + hashids.encode(url['id'])
        urls.append(url)
    return render_template('stats.html', urls=urls)