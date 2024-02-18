import sqlite3

def get_db_connection():
    """
    Establishes a connection to the database and sets the row_factory to sqlite3.Row. 
    Returns the connection object.
    """
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    return conn


def insert_url(original_url):
    """
    Inserts a new URL into the database.

    Args:
        original_url: The original URL to be inserted.

    Returns:
        int: The ID of the newly inserted URL.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO urls (original_url) VALUES (?)', (original_url,))
        conn.commit()
        return cursor.lastrowid


def update_click(original_id):
    """
    Updates the click count for the given original_id in the database and returns the original URL.

    Parameters:
    original_id (int): The original ID for which the click count needs to be updated.

    Returns:
    str: The original URL corresponding to the given original_id.
    """
    conn = get_db_connection()
    original_id = original_id[0]
    url_data = conn.execute('SELECT original_url, clicks FROM urls WHERE id = ?', (original_id,)).fetchone()
    original_url, clicks = url_data

    conn.execute('UPDATE urls SET clicks = ? WHERE id = ?', (clicks+1, original_id))
    conn.commit()
    conn.close()
    return original_url


def get_stats(request, hashids):
    """
    Retrieves statistics from the database based on the request and hashids, and returns a list of URLs with additional data.
    Parameters:
    - request: the request object containing information about the HTTP request
    - hashids: the hashids object used to encode the URL IDs
    Returns:
    - urls: a list of dictionaries representing the URLs with additional data
    """
    with get_db_connection() as db_connection:
        urls_data = db_connection.execute('SELECT id, created, original_url, clicks FROM urls').fetchall()
    urls = [dict(url, short_url=request.host_url + hashids.encode(url['id'])) for url in urls_data]
    return urls
