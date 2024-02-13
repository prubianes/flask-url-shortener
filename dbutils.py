import sqlite3

def get_db_connection():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    return conn


def insertURL(url):
    conn = get_db_connection()

    url_data = conn.execute('INSERT into urls (original_url) values (?)', (url,))
    conn.commit()
    conn.close()

    return url_data

def updateClick(original_id):
    conn = get_db_connection()
    original_id = original_id[0]
    url_data = conn.execute('SELECT original_url, clicks FROM urls WHERE id = (?)', (original_id,)).fetchone()
    original_url = url_data['original_url']
    clicks = url_data['clicks']

    conn.execute('UPDATE urls SET clicks = ? WHERE id = ?',(clicks+1, original_id))
    conn.commit()
    conn.close()
    return original_url

def getStats(request, hashids):
    conn = get_db_connection()
    db_urls = conn.execute('SELECT id, created, original_url, clicks FROM urls').fetchall()
    conn.close()
    urls = []
    for url in db_urls:
        url = dict(url)
        url['short_url'] = request.host_url + hashids.encode(url['id'])
        urls.append(url)
    
    return urls
