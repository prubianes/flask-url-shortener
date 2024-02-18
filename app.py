
from hashids import Hashids
from flask import Flask, render_template, request, flash, redirect, url_for

from dbutils import insert_url, update_click, get_stats

app = Flask(__name__, template_folder='templates')

app.config['SECRET_KEY'] = 'No one will know' # This should be a secret string
hashids = Hashids(min_length=4, salt=app.config['SECRET_KEY'])

@app.route('/', methods=('GET', 'POST'))
def index():
    """
    A function to handle GET and POST requests for the index route.

    Parameters:
    None

    Returns:
    Renders the index.html template with the short URL if a POST request is made, otherwise renders the index.html template.
    """
    if request.method == 'POST':
        url = request.form['url']
        
        if not url:
            flash('You need to enter a URL!')
            return redirect(url_for('index'))
        
        if not url.startswith(('http://', 'https://')):
            url = "http://" + url
        
        url_id = insert_url(url)
        hashid = hashids.encode(url_id)
        short_url = request.host_url + hashid

        return render_template('index.html', short_url=short_url)
    
    return render_template('index.html')

@app.route('/<id>')
def url_redirect(id):
    """
    Redirects to the original URL associated with the given ID after decoding it using hashids. 
    If the ID is not valid, it flashes a message and redirects to the index.
    """
    decoded_id = hashids.decode(id)
    if decoded_id:
        original_url = update_click(decoded_id)
        return redirect(original_url)
    else:
        flash('Not a valid URL')
        return redirect(url_for('index'))

    
@app.route('/stats')
def stats():
    """
    A function to retrieve statistics and render the stats.html template with the retrieved URLs.
    """
    urls = get_stats(request, hashids)
    return render_template('stats.html', urls=urls)