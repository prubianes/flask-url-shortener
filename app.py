
from hashids import Hashids
from flask import Flask, render_template, request, flash, redirect, url_for

from dbutils import insertURL, updateClick, getStats

app = Flask(__name__, template_folder='templates')

app.config['SECRET_KEY'] = 'No one will know' # This should be a secret string
hashids = Hashids(min_length=4, salt=app.config['SECRET_KEY'])

@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        url = request.form['url']
        
        if not url:
            flash('You need to enter an URL!')
            return redirect(url_for('index'))
        
        #In order for the redirect to work it need the http in the begining of the string
        if url.find('https://') != 0 or url.find('http://') != 0:
            url = "http://" + url
        
        url_data = insertURL(url)

        url_id = url_data.lastrowid
        hashid = hashids.encode(url_id)
        short_url = request.host_url + hashid

        return render_template('index.html', short_url=short_url)
    
    return render_template('index.html')

@app.route('/<id>')
def url_redirect(id):
    original_id = hashids.decode(id)
    if original_id:
        original_url = updateClick(original_id)
        return redirect(original_url)
    else:
        flash('Not a Valid URL')
        return redirect(url_for('index'))

    
@app.route('/stats')
def stats():
    urls = getStats(request, hashids)
    return render_template('stats.html', urls=urls)