import sqlite3
import requests
from io import BytesIO

url = 'http://192.168.2.32:8000/image.png'

response = requests.get(url)

if response.status_code == 200:
    image_data = response.content
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO images (image) VALUES (?)',
                   (sqlite3.Binary(image_data),))
    conn.commit()
    conn.close()

# f = open("image2.png", "rb")
# img = f.read()
# f.close()


# conn = sqlite3.connect('database.db')
# cursor = conn.cursor()
# cursor.execute('INSERT INTO images (image) VALUES (?)', (sqlite3.Binary(img),))
# conn.commit()
# conn.close()
