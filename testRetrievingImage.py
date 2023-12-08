import sqlite3
import base64

# Connect to the SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Query the image data from the database
cursor.execute('SELECT image FROM images ORDER BY id DESC LIMIT 1')
image_data = cursor.fetchone()

# Close the database connection
conn.close()

# Check if the image data was found
if image_data:
    image_data = image_data[0]
    a = 2

    # Convert binary image data to base64
    base64_data = base64.b64encode(image_data).decode('utf-8')

    # Convert base64 data to binary
    binary_data = base64.b64decode(base64_data)

    # Save the binary data to a PNG file
    with open('output_image.png', 'wb') as file:
        file.write(binary_data)

    print('Image saved successfully!')
else:
    print('Image not found in the database.')
